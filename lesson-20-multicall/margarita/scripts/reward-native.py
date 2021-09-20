from brownie import *

from scripts.helpers.utils import coin_price


def main():
    pool = "3pool"
    contracts = {
        addr: Contract(addr)
        for addr in [pool, pool + "_rewards", "crv", "gauge_controller"]
    }

    crv_price = coin_price("curve-dao-token")
    inflation_rate = contracts["crv"].rate() / 10 ** 18
    relative_weight = (
        contracts["gauge_controller"].gauge_relative_weight(
            contracts[pool + "_rewards"]
        )
        / 10 ** 18
    )

    working_supply = contracts[pool + "_rewards"].working_supply() / 10 ** 18
    asset_price = calc_asset_price(contracts[pool])
    virtual_price = contracts[pool].get_virtual_price() / 10 ** 18

    print(
        (crv_price * inflation_rate * relative_weight * 12614400)
        / (working_supply * asset_price * virtual_price)
        * 100
    )


def calc_asset_price(pool):
    asset_type = Contract("registry").get_pool_asset_type(pool)
    coins = ["usd", "ethereum", "bitcoin", "chainlink"]

    if asset_type > 0:
        return coin_price(coins[asset_type])
    else:
        return 1
