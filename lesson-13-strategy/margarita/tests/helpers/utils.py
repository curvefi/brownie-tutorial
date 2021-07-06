from brownie import *

# Useful contracts


def load_contract(addr):
    try:
        cont = Contract(addr)
    except ValueError:
        cont = Contract.from_explorer(addr)
    return cont


def load_registry():
    return load_contract("0x90E00ACe148ca3b23Ac1bC8C240C2a7Dd9c2d7f5")


def load_minter():
    return load_contract("0xd061D61a4d941c39E5453435B6345Dc261C2fcE0")


def load_crv():
    return load_contract(load_minter().token())


# Rewards Calculations

# Pad target pools with empty addresses for rewards list
def set_pools_array(pools):
    return_array = [ZERO_ADDRESS] * 8
    i = 0
    for _p in pools:
        if i < 8:
            return_array[i] = _p
            i += 1
    return return_array


# Claim CRV rewards and return value
def calc_cur_rewards(acct, pools):
    # Get Initial Value
    init_val = calc_crv_balance(acct)

    # Set Array
    formatted_pools = set_pools_array(pools)

    # Mint Many
    load_minter().mint_many(formatted_pools, {"from": acct})

    # Calculate Balance
    final_val = calc_crv_balance(acct)

    # Undo Mint Many
    chain.undo()

    # Return Final Balance
    crv_val = final_val - init_val
    return crv_val


# Make CRV balance human readable
def calc_crv_balance(acct):
    crv = load_crv()
    return crv.balanceOf(acct) / 10 ** crv.decimals()


# Deposit Functions

# Redeposit from 3pool to a metapool
def tripool_to_meta(target, acct, tripool_rewards):
    registry = load_registry()
    tripool_lp = load_contract(tripool_rewards.lp_token())

    # Can we Ape?
    can_ape = False
    for _c in range(registry.get_n_coins(target)[0]):
        if target.coins(_c) == tripool_lp:
            coin_index = _c
            can_ape = True
    if can_ape == False:
        return

    # Withdraw
    tripool_rewards.withdraw(tripool_rewards.balanceOf(acct), {"from": acct})
    assert tripool_lp.balanceOf(acct) > 0

    # Ape
    tripool_bal = tripool_lp.balanceOf(acct)
    tripool_lp.approve(target, tripool_bal, {"from": acct})
    amount_array = [0] * registry.get_n_coins(target)[0]
    amount_array[coin_index] = tripool_bal
    target.add_liquidity(amount_array, 0, {"from": acct})
    target_lp = load_contract(registry.get_lp_token(target))

    # Stake Into Rewards
    rewards = stake_into_rewards(registry.get_pool_from_lp_token(target_lp), acct)
    if rewards == None:
        return
    return rewards


# Stake from any pool into rewards gauge
def stake_into_rewards(pool, acct):
    # Load Pool LP Token
    registry = load_registry()
    _lp = load_contract(registry.get_lp_token(pool))

    # Load Gauge
    _gauge = load_contract(registry.get_gauges(pool)[0][0])
    if _gauge == None:
        return None

    # Create Approval
    _bal = _lp.balanceOf(acct)
    _lp.approve(_gauge, _bal, {"from": acct})

    # Deposit
    _gauge.deposit(_bal, {"from": acct})

    return _gauge
