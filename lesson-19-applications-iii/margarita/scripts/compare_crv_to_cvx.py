import time

from brownie import *
from brownie_tokens import MintableForkToken

from scripts.helpers.utils import *

# Globals
crv_price = coin_price("curve-dao-token")
cvx_price = coin_price("convex-finance")
registry = load_contract("registry")
cvx_pools = load_contract("0xF403C135812408BFbE8713b5A23a04b3D48AAE31")

whale = "0xfbd50c82ea05d0d8b6b302317880060bc3086866"  # Anonymous address, replace with yours to customize


def main():
    stake_pool = 10  # Which pool offset (CVX) to compare
    compare_crv_to_cvx(stake_pool, True)


# Compare Curve Rewards to Convex Rewards for the whale address in a single pool
# Returns [crv_val, cvx_val] in dollars
def compare_crv_to_cvx(stake_pool, verbose=True):
    # Simulation Variables
    hours = 24
    final_time = chain.time() + 60 * 60 * hours
    pool_name = load_pool_name(stake_pool)
    test_amt = 100_000

    # Skip if pool does not exist
    if pool_name is None:
        vprint(
            f"\n\n=======\nSkipping pools {stake_pool}\nNot presently on Convex",
            verbose,
        )
        return -1, -1

    # Mint DAI for testing
    coin = print_money(whale, test_amt, "dai")

    vprint(f"\n\n==================\nTesting pool {stake_pool} {pool_name}", verbose)
    vprint(
        f"Account: {whale}\nTesting ${test_amt} {coin.symbol()} for {hours} hours\n",
        verbose,
    )

    # Control group -- Mine forward to final time
    chain.snapshot()
    chain.mine(blocks=100, timestamp=final_time)
    target_block = chain.height
    vprint("\n===TESTING BASELINE: No Ape===", verbose)

    baseline = load_claimable_balance(whale, stake_pool, verbose)
    vprint(f"Baseline Claimable Balance: ${baseline:.2f}\n", verbose)
    chain.revert()

    # Test 1: Ape into Curve
    vprint("===TESTING STRATEGY 1: Ape into Curve===", verbose)
    vprint(f"Stake {test_amt} DAI in Curve {pool_name}", verbose)

    deposit_crv(whale, stake_pool, coin)
    advance_chain(target_block, final_time)
    crv_staked_amt = load_claimable_balance(whale, stake_pool, verbose)
    chain.revert()

    # Test 2: Ape into Convex
    vprint("\n===TESTING STRATEGY 2: Ape into Convex===", verbose)
    vprint(f"Stake {test_amt} DAI in Convex {pool_name}", verbose)

    deposit_cvx(whale, stake_pool)
    advance_chain(target_block, final_time)
    cvx_staked_amt = 0 + load_claimable_balance(whale, stake_pool, verbose)

    vprint("\n===FINAL===", verbose)
    vprint(f"STRATEGY 1 (CRV): ${crv_staked_amt - baseline:.2f}", verbose)
    vprint(f"STRATEGY 2 (CVX): ${cvx_staked_amt - baseline:.2f}", verbose)

    # Reset chain so next trial starts fresh
    chain.reset()
    return crv_staked_amt - baseline, cvx_staked_amt - baseline


# DEPOSIT FUNCTIONS

# Deposit funds into a CRV pool
def deposit_crv(addr, stake_pool, coin):
    # Load contracts
    target_pool, target_lp, target_reward = load_crv_contracts(stake_pool)

    # Add to CRV LP Pool
    crv_add(coin, target_pool, addr)

    # Stake in CRV rewards gauge
    target_lp_bal = target_lp.balanceOf(addr)
    safe_approve(target_lp, target_reward, target_lp_bal, addr)
    target_reward.deposit(target_lp_bal, {"from": addr})


# Deposit funds into a CVX pool
def deposit_cvx(addr, stake_pool):
    target_pool, target_lp, _rewards = load_crv_contracts(stake_pool)

    # Add to CRV LP Pool
    crv_add(load_contract("dai"), target_pool, addr)

    # Stake in CVX rewards gauge
    cvx_booster = load_contract("0xF403C135812408BFbE8713b5A23a04b3D48AAE31")
    target_bal = target_lp.balanceOf(addr)
    if target_bal == 0:
        return 0

    safe_approve(target_lp, cvx_booster, target_bal, addr)
    cvx_booster.deposit(stake_pool, target_bal, 1, {"from": addr})


# Call to add liquidity to a Curve pool or Curve metapool
def crv_add(coin, target, addr):
    if registry.is_meta(target):
        return _crv_add_meta(coin, target, addr)
    else:
        return _crv_add_liquidity(coin, target, addr)


# Add liquidity to Curve metapool with two add_liquidity calls
def _crv_add_meta(coin, target_pool, addr):
    pool_1_lp = target_pool.coins(1)
    pool_1 = load_contract(registry.get_pool_from_lp_token(pool_1_lp))
    pool_1_lp = load_contract(registry.get_lp_token(pool_1))

    val = _crv_add_liquidity(coin, pool_1, addr)
    if val == 0:
        return 0

    return _crv_add_liquidity(pool_1_lp, target_pool, addr)


# Base call to add liquidity to a CRV pool
def _crv_add_liquidity(coin, target_pool, addr):
    bal = coin.balanceOf(addr)
    safe_approve(coin, target_pool, bal, addr)

    array_length = registry.get_n_coins(target_pool)[0]
    coins = [0] * array_length
    aped = False
    for c in range(array_length):
        if target_pool.coins(c) == coin.address:
            coins[c] = coin.balanceOf(addr)
            aped = True

    if aped is False:
        return 0

    target_pool.add_liquidity(coins, 0, {"from": addr})
    return load_contract(registry.get_lp_token(target_pool)).balanceOf(addr)


# REWARDS CALCULATIONS

# Calculate the claimable balance within a pool on CRV/CVX
def load_claimable_balance(address, pool, verbose):
    # Amounts in CRV pools
    amt = scrape_crv_pools(address, pool, verbose)

    # Amounts in CVX pools
    amt += scrape_cvx_pools(address, pool, verbose)

    return amt


# Calculate CRV rewards for a pool
def scrape_crv_pools(address, pool, verbose):
    # Load CRV gauge from CVX pool
    # Returns [lp, token, gauge, crvRewards]
    _crv_gauge = load_contract(cvx_pools.poolInfo(pool)[2])
    total_usd = 0

    if _crv_gauge.balanceOf(address):
        _pool_name = pool_name_from_lp(cvx_pools.poolInfo(pool)[0])
        _crv_amt = get_claimable_crv_rewards(_crv_gauge, address)
        _bal = _crv_gauge.balanceOf(address) / 10 ** 18
        crv_earnings = _crv_amt

        vprint(
            f"Curve {_pool_name} balance {_bal:.2f}\n"
            + f"{crv_earnings:.2f} CRV @ ${crv_price} = ${crv_earnings * crv_price:.2f}\n",
            verbose,
        )

        total_usd = crv_earnings * crv_price

    return total_usd


# Calculate CVX rewards for a pool
def scrape_cvx_pools(address, pool, verbose):
    # Load CVX rewards address
    _addr = cvx_pools.poolInfo(pool)[3]
    _rewards = load_contract(_addr)

    # Skip if no rewards earned
    if _rewards.earned(address) == 0:
        return 0

    _crv_bal, _cvx_bal, _bal = get_claimable_cvx_rewards(_rewards, address)
    _earned = _crv_bal * crv_price + _cvx_bal * cvx_price

    if verbose:
        _pool_name = load_pool_name(pool)
        vprint(
            f"Convex {_pool_name} balance {_bal:.2f}\n"
            + f"{_crv_bal:.2f} CRV @ ${crv_price} + {_cvx_bal:.2f} CVX @ ${cvx_price} = ${_earned:.2f}\n",
            verbose,
        )

    return _earned


# Calculate claimable CRV rewards
def get_claimable_crv_rewards(gauge, addr):
    # Claim and undo as opposed to replicating math
    minter = load_minter()
    crv = load_crv()
    init_crv = crv.balanceOf(addr)
    minter.mint(gauge, {"from": addr})
    final_crv = crv.balanceOf(addr)
    chain.undo()
    return (final_crv - init_crv) / 10 ** crv.decimals()


# Calculate claimable CVX rewards
def get_claimable_cvx_rewards(_rewards, address):
    # Calculate CRV Rewards from Convex Endpoint
    _crv_bal = _rewards.earned(address)

    # Replicate Minting Math for CVX rewards
    _crv = load_contract(_rewards.rewardToken())
    _crv_dec = 10 ** _crv.decimals()
    _crv_adj = _crv_bal / _crv_dec

    _bal_token = load_contract(_rewards.stakingToken())
    _bal_dec = 10 ** _bal_token.decimals()
    _bal = _rewards.balanceOf(address) / _bal_dec

    #  Load CVX Data
    operator = load_contract(_rewards.operator())
    cvx = load_contract(operator.minter())
    cvx_dec = 10 ** cvx.decimals()

    # Replicate Minting Math
    cliff = cvx.totalSupply() / cvx.reductionPerCliff()
    total_cliffs = cvx.totalCliffs()
    _cvx_bal = 0
    if cliff < total_cliffs:
        reduction = total_cliffs - cliff
        _adj_bal = _crv_bal * reduction / total_cliffs
        _cvx_adj = _adj_bal / cvx_dec

    return _crv_adj, _cvx_adj, _bal


# HELPER FUNCTIONS

# Assign a balance for a MintableForkToken
def print_money(addr, amount, alias):
    coin = MintableForkToken(alias)
    coin._mint_for_testing(addr, amount * 10 ** coin.decimals())
    return coin


# Return the Curve pool, LP Token, and Rewards gauge for a CVX Pool ID
def load_crv_contracts(cvx_pool_id):
    try:
        _lp = load_contract(cvx_pools.poolInfo(cvx_pool_id)[0])
    except:
        return None, None, None
    _pool = load_contract(registry.get_pool_from_lp_token(_lp))
    try:
        _reward = load_contract(registry.get_gauges(_pool)[0][0])
    except:
        _reward = None
    return _pool, _lp, _reward


# Load a pool name by ID
def load_pool_name(_pool_id):
    _pool, _lp, _rewards = load_crv_contracts(_pool_id)
    if _pool is None:
        return None
    return registry.get_pool_name(_pool)


# Mine forward in time a set number of blocks
def advance_chain(target_block, final_time):
    blocks = target_block - chain.height
    chain.mine(blocks=blocks, timestamp=final_time)


# Approve, but don't fail if already approved
def safe_approve(origin, target, bal, addr):
    existing_allowance = origin.allowance(addr, target)

    try:
        if bal > existing_allowance:
            origin.approve(target, bal - existing_allowance, {"from": addr})
    except:
        print(f"Could not approve {origin} {target} {bal} {addr}")
        pass


# Print if verbose flag is set
def vprint(string, verbose):
    if verbose:
        print(string)
