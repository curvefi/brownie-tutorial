#!/usr/bin/python3

import brownie.network as network
from brownie import Margarita, accounts
from brownie.network import max_fee, priority_fee


def main():
    if network.show_active() in ["mainnet", "mainnet-fork", "rinkeby"]:
        if network.show_active() == "mainnet":
            priority_fee("2 gwei")
            max_fee("25 gwei")
            account_name = "minnow"
        else:
            account_name = "husky"

        if network.show_active() == "mainnet-fork":
            publish = False
        else:
            publish = False
        deployer = accounts.load(account_name)

    else:
        deployer = accounts[0]
        publish = False

    beneficiary_address = deployer
    return Margarita.deploy(
        "MARGARITA",
        "MARG",
        18,
        0,
        beneficiary_address,
        {"from": deployer},
        publish_source=publish,
    )
