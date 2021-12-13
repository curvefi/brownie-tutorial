from brownie import *


# Dynamically set multiple Curve contract aliases
def main():
    # Pull Address Provider to Retrieve Dynamically
    # https://curve.readthedocs.io/ref-addresses.html
    address_provider = "0x0000000022D53366457F9d5E68Ec105046FC4383"
    ap = set_alias(address_provider, "address_provider")

    # Set Provider Contracts
    registry = set_alias(ap.get_registry(), "registry")
    pool_info = set_alias(ap.get_address(1), "pool_info")
    exchange = set_alias(ap.get_address(2), "registry_exchange")
    factory = set_alias(ap.get_address(3), "factory")
    distributor = set_alias(ap.get_address(4), "fee_distributor")

    controller = set_alias(registry.gauge_controller(), "gauge_controller")

    # CRV + veCRV
    crv = set_alias(controller.token(), "crv")
    vecrv = set_alias(controller.voting_escrow(), "vecrv")

    # Set pool, lp, and rewadrs alias for each pool
    for index in range(registry.pool_count()):
        # Set Pool Alias
        pool_addr = registry.pool_list(index)
        name = registry.get_pool_name(pool_addr)
        pool = set_alias(pool_addr, name)

        # Set LP Token Alias
        lp = set_alias(registry.get_lp_token(pool), f"{name}_lp")

        # Set Rewards Alias
        rewards_addr = registry.get_gauges(pool)[0][0]
        rewards_alias = f"{name}_rewards"
        pool_rewards = set_alias(rewards_addr, rewards_alias)

    # Useful tokens
    tri = Contract("3pool")
    dai = set_alias(tri.coins(0), "dai")
    usdc = set_alias(tri.coins(1), "usdc")
    tether = set_alias(tri.coins(2), "tether")

    # Convex
    # https://docs.convexfinance.com/convexfinance/faq/contract-addresses
    cvx = set_alias("0x4e3FBD56CD56c3e72c1403e103b45Db9da5B9D2B", "cvx")
    cvxcrv = set_alias("0x62B9c7356A2Dc64a1969e19C23e4f579F9810Aa7", "cvxcrv")
    booster = set_alias("0xF403C135812408BFbE8713b5A23a04b3D48AAE31", "cvx_booster")
    staker = set_alias("0xCF50b810E57Ac33B91dCF525C6ddd9881B139332", "cvx_staker")


def load_contract(addr):
    try:
        c = Contract(addr)
    except:
        c = Contract.from_explorer(addr)
    return c


# Set alias, removing existing alias if necessary
def set_alias(addr, name):
    if addr == ZERO_ADDRESS:
        return

    print(f"Setting {name} as {addr}")
    c = load_contract(addr)

    try:
        c.set_alias(name)
    except Exception as e:
        print(e)
        old = load_contract(name)
        print(f"Unsetting {name} for {old.address}")
        old.set_alias(None)
        c.set_alias(name)

    return c
