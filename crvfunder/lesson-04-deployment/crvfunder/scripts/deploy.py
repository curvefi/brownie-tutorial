from brownie import FundraisingGaugeV1, GaugeFactoryV1, accounts


def main():
    # load an account to use for deployment
    deployer = accounts.load("dev")

    # https://curve.readthedocs.io/ref-addresses.html#ownership-proxies
    admin_proxy = "0x519AFB566c05E00cfB9af73496D00217A630e4D5"

    # deploy the implementation
    implementation = FundraisingGaugeV1.deploy(
        admin_proxy, {"from": deployer, "priority_fee": "2 gwei"}
    )

    # deploy the factory
    GaugeFactoryV1.deploy(implementation, {"from": deployer, "priority_fee": "2 gwei"})
