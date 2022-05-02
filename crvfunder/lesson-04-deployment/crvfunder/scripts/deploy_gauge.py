from brownie import ETH_ADDRESS, GaugeFactoryV1, accounts

CALLER = accounts.load("dev")
FACTORY_ADDR = ETH_ADDRESS  # TODO: change prior to running script

# account to receive emissions
RECEIVER = ETH_ADDRESS  # TODO: change prior to running script
# maximum amount of emissions to receiver (to the correct precision)
MAX_EMISSIONS = 200 * 10**18


def main():
    # change to be account
    factory = GaugeFactoryV1.at(FACTORY_ADDR)

    tx = factory.deploy_gauge(RECEIVER, MAX_EMISSIONS, {"from": CALLER, "priority_fee": "2 gwei"})
    print(f"Fundraising Gauge deployed at: {tx.events['NewGauge']['_funder_instance']}")
