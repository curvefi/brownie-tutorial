import json

import requests
from brownie import *


def load_contract(addr):
    if addr == ZERO_ADDRESS:
        return None
    try:
        cont = Contract(addr)
    except ValueError:
        cont = Contract.from_explorer(addr)
    return cont


def load_crv_positions(target_addr):
    registry = load_registry()
    crv_pools = [ZERO_ADDRESS] * 8
    j = 0
    for i in range(registry.pool_count()):
        # Check if Gauge exists
        _addr = registry.get_gauges(registry.pool_list(i))[0][0]
        if _addr == ZERO_ADDRESS:
            continue

        # Add gauge to claim if balance
        _gauge = load_contract(_addr)
        if _gauge.balanceOf(target_addr) > 0 and j < 8:
            crv_pools[j] = _addr
            j = j + 1
    return crv_pools


def load_minter():
    return load_contract("0xd061D61a4d941c39E5453435B6345Dc261C2fcE0")


def load_crv():
    return load_contract(load_minter().token())


def calc_cur_value(user, crv_pools=None):
    # Get Initial Value
    init_val = calc_balance(user)

    # Set CRV claim array
    if crv_pools is None:
        crv_pools = load_crv_positions(user)
        print(f"Slow load of {crv_pools}")

    # Mint Many
    minter = load_minter()
    minter.mint_many(crv_pools, {"from": user})

    # Calculate our Balance
    final_val = calc_balance(user)

    # Undo Mint Many
    chain.undo()
    return final_val - init_val


def calc_balance(whale):
    crv = load_crv()
    return crv.balanceOf(whale) / 10 ** crv.decimals()


def load_registry():
    addr_provider = load_contract("0x0000000022d53366457f9d5e68ec105046fc4383")
    return load_contract(addr_provider.get_registry())


def coin_price(price_type):
    url = f"https://api.coingecko.com/api/v3/simple/price?ids={price_type}&vs_currencies=usd"
    data = requests.get(url)
    json_data = json.loads(data.content)
    price = json_data.get(price_type).get("usd")
    return price


def load_pool_from_index(index):
    reg = load_registry()
    pool = load_contract(reg.pool_list(index))
    return pool


def load_gauge(addr):
    reg = load_registry()
    pool = load_contract(reg.get_gauges(addr)[0][0])
    return pool


def deposit_to_eth_pool(eth_pool, user, amount):
    eth_pool.add_liquidity([amount, 0], 0, {"from": user, "value": amount})
    eth_lp = load_contract(load_registry().get_lp_token(eth_pool))
    bal = eth_lp.balanceOf(user)

    eth_gauge = load_gauge(eth_pool)
    eth_lp.approve(eth_gauge, bal, {"from": user})
    eth_gauge.deposit(bal, {"from": user})
    return eth_gauge.address


def redeposit_eth_pool(user, old_pool, new_pool):
    init_bal = user.balance()

    registry = load_registry()
    old_gauge = load_gauge(old_pool)
    bal = old_gauge.balanceOf(user)
    old_gauge.withdraw(bal, {"from": user})
    old_pool.remove_liquidity_one_coin(bal, 0, 0, {"from": user})
    old_lp = registry.get_lp_token(old_pool)

    # Confirm no ETH left in first pool
    assert old_gauge.balanceOf(user) == 0
    assert load_contract(old_lp).balanceOf(user) == 0

    new_bal = user.balance()
    redeposit_amount = new_bal - init_bal

    new_rewards = deposit_to_eth_pool(new_pool, user, redeposit_amount)
    return new_rewards, redeposit_amount


def pool_name_from_lp(lp):
    r = load_registry()
    pool_addr = r.get_pool_from_lp_token(lp)
    return r.get_pool_name(pool_addr)

