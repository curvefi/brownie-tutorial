# @version 0.3.1
"""
@title veFunder Factory
@license MIT
"""


interface Funder:
    def initialize(_receiver: address, _deadline: uint256, _max_emissions: uint256): nonpayable


event UpdateImplementation:
    _old_implementation: address
    _new_implementation: address

event UpdateFallbackReceiver:
    _old_fallback: address
    _new_fallback: address

event TransferOwnership:
    _old_owner: address
    _new_owner: address

event NewFunder:
    _receiver: indexed(address)
    _deadline: uint256
    _max_emissions: uint256
    _funder_instance: address


implementation: public(address)
fallback_receiver: public(address)

owner: public(address)
future_owner: public(address)

get_funders_count: public(uint256)
funders: public(address[1000000])


@external
def __init__(_fallback_receiver: address):
    self.owner = msg.sender
    self.fallback_receiver = _fallback_receiver

    log TransferOwnership(ZERO_ADDRESS, msg.sender)
    log UpdateFallbackReceiver(ZERO_ADDRESS, _fallback_receiver)


@external
def deploy(_receiver: address, _deadline: uint256, _max_emissions: uint256) -> address:
    funder: address = create_forwarder_to(self.implementation)
    Funder(funder).initialize(_receiver, _deadline, _max_emissions)

    # update for easy enumeration
    funders_count: uint256 = self.get_funders_count
    self.funders[funders_count] = funder
    self.get_funders_count = funders_count + 1

    log NewFunder(_receiver, _deadline, _max_emissions, funder)
    return funder


@external
def set_implementation(_implementation: address):
    assert msg.sender == self.owner

    log UpdateImplementation(self.implementation, _implementation)
    self.implementation = _implementation


@external
def set_fallback_receiver(_fallback_receiver: address):
    assert msg.sender == self.owner

    log UpdateFallbackReceiver(self.fallback_receiver, _fallback_receiver)
    self.fallback_receiver = _fallback_receiver


@external
def commit_transfer_ownership(_future_owner: address):
    assert msg.sender == self.owner

    self.future_owner = _future_owner


@external
def accept_transfer_ownership():
    assert msg.sender == self.future_owner

    log TransferOwnership(self.owner, msg.sender)
    self.owner = msg.sender
