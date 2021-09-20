import json
from datetime import datetime

import brownie
from brownie import *

from scripts.helpers.utils import coin_price, load_contract

registry = Contract("registry")

crv_price = coin_price("curve-dao-token")


def main():
    start_time = datetime.now().timestamp()
    pools = load_pools_cached()

    data = load_rewards_multicall(pools)
    sorted_data = dict(sorted(data.items(), key=lambda x: -x[1]))
    i = 1
    for k, v in sorted_data.items():
        if i <= 10:
            print(i, k, v)
        i += 1
    final_timestamp = datetime.now().timestamp() - start_time
    print(f"Completed in {final_timestamp:.2f} seconds")


# Retrieve Curve addresses from a cache file or create
def load_pools_cached():
    contracts = read_file("./curve_pool_addrs.json")
    if contracts is None:
        with brownie.multicall:
            pool_count = registry.pool_count.call()
            pools = [registry.pool_list(i) for i in range(pool_count)]
            lps = [registry.get_lp_token(pool) for pool in pools]
            gauges = [registry.get_gauges(pool) for pool in pools]
            names = [registry.get_pool_name(pool) for pool in pools]
        contracts = {}
        for i in range(pool_count):
            if gauges[i][0][0] != ZERO_ADDRESS:
                pool = str(pools[i])
                lp = str(lps[i])
                gauge = str(gauges[i][0][0])
                contracts[str(names[i])] = {"pool": pool, "lp": lp, "gauge": gauge}
        write_file("./curve_pool_addrs.json", contracts)

    return contracts


# Pull Curve pool tAPY as multicall
def load_rewards_multicall(pools):
    inflation_rate = Contract("crv").rate() / 10 ** 18
    gc = Contract("gauge_controller")

    with brownie.multicall:
        weights = [
            gc.gauge_relative_weight(v["gauge"]) / 10 ** 18 for v in pools.values()
        ]
        supplies = [
            Contract(v["gauge"]).working_supply() / 10 ** 18 for v in pools.values()
        ]
        prices = [
            Contract(v["pool"]).get_virtual_price() / 10 ** 18 for v in pools.values()
        ]

    i = 0
    ret = {}
    for k, v in pools.items():
        calc = (
            (crv_price * inflation_rate * weights[i] * 12614400)
            / (supplies[i] * calc_asset_price(v["pool"]) * prices[i])
            * 100
        )
        ret[k] = calc
        i += 1
    return ret


# Calculate asset price based on pool
def calc_asset_price(pool):
    asset_type = Contract("registry").get_pool_asset_type(pool)

    # Hardcoded TriCrypto v2, not set in registry
    if asset_type == 4 or pool == "0xD51a44d3FaE010294C616388b506AcdA1bfAAE46":
        tri = Contract(pool)
        tether_decimals = Contract(tri.coins(0)).decimals()
        lp_val = tri.calc_token_amount([10 ** tether_decimals, 0, 0], True)

        return 1 / (lp_val / 10 ** 18)

    # Euro coins miscategorized in registry
    if "0xD71eCFF9342A5Ced620049e616c5035F1dB98620" in Contract("registry").get_coins(
        pool
    ):
        return coin_price("seur")

    coins = ["usd", "ethereum", "bitcoin", "chainlink"]

    if asset_type > 0:
        return coin_price(coins[asset_type])
    else:
        return 1


# HELPER FUNCTIONS

# Read a file into a json object
def read_file(filename):
    try:
        with open(filename, "r") as openfile:
            json_object = json.load(openfile)
    except:
        json_object = None
    return json_object


# Write a file into a json object
def write_file(filename, data):
    json_data = json.dumps(data, indent=4)
    with open(filename, "w") as outfile:
        outfile.write(json_data)
