# @version 0.3.1
"""
@title veFunder
@notice Custom gauge directing emissions to specified wallet
"""


interface CRV20:
    def rate() -> uint256: view
    def future_epoch_time_write() -> uint256: nonpayable

interface Factory:
    def owner() -> address: view
    def fallback_receiver() -> address: view

interface GaugeController:
    def checkpoint_gauge(_gauge: address): nonpayable
    def gauge_relative_weight(_gauge: address, _time: uint256) -> uint256: view


event Checkpoint:
    _timestamp: uint256
    _new_emissions: uint256

event TransferOwnership:
    _old_owner: indexed(address)
    _new_owner: indexed(address)


CRV: constant(address) = 0xD533a949740bb3306d119CC777fa900bA034cd52
GAUGE_CONTROLLER: constant(address) = 0x2F50D538606Fa9EDD2B11E2446BEb18C9D5846bB

WEEK: constant(uint256) = 604800
YEAR: constant(uint256) = 86400 * 365

# taken from CRV20 to allow calculating locally
RATE_DENOMINATOR: constant(uint256) = 10 ** 18
RATE_REDUCTION_COEFFICIENT: constant(uint256) = 1189207115002721024  # 2 ** (1/4) * 1e18
RATE_REDUCTION_TIME: constant(uint256) = YEAR

# [uint216 inflation_rate][uint40 future_epoch_time]
inflation_params: uint256

# _user => accumulated CRV
integrate_fraction: public(HashMap[address, uint256])
last_checkpoint: public(uint256)

receiver: public(address)
# [uint216 max_emissions][uint40 deadline]
receiver_data: uint256

factory: public(address)
cached_fallback_receiver: public(address)


@external
def __init__():
    # prevent initialization of the implementation contract
    self.factory = 0x000000000000000000000000000000000000dEaD


@external
def user_checkpoint(_user: address) -> bool:
    """
    @notice Checkpoint the gauge updating total emissions
    @param _user The user to checkpoint and update accumulated emissions for
    """
    # timestamp of the last checkpoint and start point for calculating new emissions
    prev_week_time: uint256 = self.last_checkpoint

    # if time has not advanced since the last checkpoint
    if block.timestamp == prev_week_time:
        return True

    # load and unpack inflation params
    inflation_params: uint256 = self.inflation_params
    rate: uint256 = shift(inflation_params, -40)
    future_epoch_time: uint256 = bitwise_and(inflation_params, 2 ** 40 - 1)

    # load the receiver
    receiver: address = self.receiver
    # load and unpack receiver data
    receiver_data: uint256 = self.receiver_data
    deadline: uint256 = bitwise_and(receiver_data, 2 ** 40 - 1)
    max_emissions: uint256 = shift(receiver_data, -40)

    # initialize emission tracking variables
    new_emissions: uint256 = 0
    multisig_emissions: uint256 = 0
    receiver_emissions: uint256 = self.integrate_fraction[receiver]

    # checkpoint the gauge filling in any missing gauge data across weeks
    GaugeController(GAUGE_CONTROLLER).checkpoint_gauge(self)

    # either the start of the next week or the current timestamp
    week_time: uint256 = min((prev_week_time + WEEK) / WEEK * WEEK, block.timestamp)

    # if the deadline is between our previous checkpoint and the end of the week
    # set the week_time var to our deadline, so we can calculate up to it only
    if prev_week_time < deadline and deadline < week_time:
        week_time = deadline

    # iterate 512 times at maximum
    for i in range(512):
        dt: uint256 = week_time - prev_week_time
        w: uint256 = GaugeController(GAUGE_CONTROLLER).gauge_relative_weight(self, prev_week_time / WEEK * WEEK)
        emissions: uint256 = 0

        # if we cross over an inflation epoch, calculate the emissions using old and new rate
        if prev_week_time <= future_epoch_time and future_epoch_time < week_time:
            # calculate up to the epoch using the old rate
            emissions = rate * w * (future_epoch_time - prev_week_time) / 10 ** 18
            # update the rate in memory
            rate = rate * RATE_DENOMINATOR / RATE_REDUCTION_COEFFICIENT
            # calculate using the new rate for the rest of the time period
            emissions += rate * w * (week_time - future_epoch_time) / 10 ** 18
            # update the new future epoch time
            future_epoch_time += RATE_REDUCTION_TIME
            # update storage
            self.inflation_params = shift(rate, 40) + future_epoch_time
        else:
            emissions = rate * w * dt / 10 ** 18

        new_emissions += emissions
        # if the time period we are calculating for ends before or at the deadline
        if week_time <= deadline:
            # if the receiver emissions + emissions from this period is greater than max_emissions
            if receiver_emissions + emissions > max_emissions:
                # the emissions from this period - amount given to receiver goes to multisig
                multisig_emissions += emissions - (max_emissions - receiver_emissions)
                # how much does the receiver get from this period
                receiver_emissions = max_emissions
            else:
                receiver_emissions += emissions
        else:
            multisig_emissions += emissions

        if week_time == block.timestamp:
            break

        # update timestamps for tracking timedelta
        prev_week_time = week_time
        week_time = min((week_time + WEEK) / WEEK * WEEK, block.timestamp)

        if prev_week_time < deadline and deadline < week_time:
            week_time = deadline


    # multisig has received emissions
    if multisig_emissions != 0:
        self.integrate_fraction[self.cached_fallback_receiver] += multisig_emissions

    # this will only be the case if receiver got emissions
    if multisig_emissions != new_emissions:
        self.integrate_fraction[receiver] = receiver_emissions

    self.last_checkpoint = block.timestamp

    log Checkpoint(block.timestamp, new_emissions)
    return True


@external
def set_killed(_is_killed: bool):
    """
    @notice Set the gauge status
    @dev Inflation params are modified accordingly to disable/enable emissions
    """
    assert msg.sender == Factory(self.factory).owner()

    if _is_killed:
        self.inflation_params = 0
    else:
        self.inflation_params = shift(CRV20(CRV).rate(), 40) + CRV20(CRV).future_epoch_time_write()


@external
def update_cached_fallback_receiver():
    """
    @notice Update the cached fallback receiver
    """
    self.cached_fallback_receiver = Factory(self.factory).fallback_receiver()


@view
@external
def max_emissions() -> uint256:
    """
    @notice Get the maximum amount of emissions distributed to the receiver, afterwards
        emissions are diverted to the Grant Council Multisig
    """
    return shift(self.receiver_data, -40)


@view
@external
def deadline() -> uint256:
    """
    @notice Get the timestamp at which emissions are diverted to the Grant Council Multisig
    """
    return bitwise_and(self.receiver_data, 2 ** 40 - 1)


@view
@external
def inflation_rate() -> uint256:
    """
    @notice Get the locally stored inflation rate
    """
    return shift(self.inflation_params, -40)


@view
@external
def future_epoch_time() -> uint256:
    """
    @notice Get the locally stored timestamp of the inflation rate epoch end
    """
    return bitwise_and(self.inflation_params, 2 ** 40 - 1)


@external
def initialize(
    _receiver: address,
    _deadline: uint256,
    _max_emissions: uint256
):
    """
    @notice Proxy initializer method
    @dev Placed last in the source file to save some gas, this fn is called only once.
        Additional checks should be made by the DAO before voting in this gauge, specifically
        to make sure that `_fund_recipient` is capable of collecting emissions.
    @param _receiver The address which will receive CRV emissions
    @param _deadline The timestamp at which emissions will redirect to
        the Curve Grant Council Multisig
    @param _max_emissions The maximum amount of emissions which `_receiver` will
        receive
    """
    assert self.factory == ZERO_ADDRESS  # dev: already initialized

    assert _deadline < 2 ** 40  # dev: invalid deadline
    assert _max_emissions < 2 ** 216  # dev: invalid maximum emissions

    self.factory = msg.sender

    self.receiver = _receiver
    self.receiver_data = shift(_max_emissions, 40) + _deadline
    self.cached_fallback_receiver = Factory(msg.sender).fallback_receiver()

    self.inflation_params = shift(CRV20(CRV).rate(), 40) + CRV20(CRV).future_epoch_time_write()
    self.last_checkpoint = block.timestamp
