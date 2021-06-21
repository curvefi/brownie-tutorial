from brownie import *

from brownie_tokens import MintableForkToken

# Script to calculates the actual number of $CRV rewards staking a fixed amount would earn after 24 hours (assuming no changes).
# This is incomplete and will not run, next unit will finalize the script.

def load_contract(c):
    if c == ZERO_ADDRESS:
        return None
    try:
        return Contract(c)
    except:
        return Contract.from_explorer(c)


# Some globals
whale = accounts[0]
registry = load_contract("0x90E00ACe148ca3b23Ac1bC8C240C2a7Dd9c2d7f5")
minter = load_contract("0xd061D61a4d941c39E5453435B6345Dc261C2fcE0")
crv = load_contract(minter.token())


def main():
    # At Initial Time
    strategy = {}
    init_value = calc_cur_value()
    strategy["init"] = init_value
    print(f"Initially {init_value}")

    # Assign DAI
    tripool = add_tripool_liquidity()
    tripool_lp = registry.get_lp_token(tripool)

    # Loop through pools
    for i in range(registry.pool_count()):

        _pool_addr = registry.pool_list(i)
        _pool = load_contract(_pool_addr)

        for _pool_index in range(registry.get_n_coins(_pool)[0]):
            if tripool_lp == _pool.coins(_pool_index):
                # Take a snapshot
                chain.snapshot()

                # Ape into pool
                ape(_pool_addr, load_contract(tripool_lp), _pool_index)

                # Skip Forward A Day
                chain.mine(timedelta=60 * 60 * 24)

                # Store CRV
                _val = calc_cur_value()
                _name = registry.get_pool_name(_pool)
                strategy[_name] = _val
                print(f"{_name}: {_val}")

                # Revert
                chain.revert()

    # Print strategy summary
    for key, value in sorted(strategy.items(), key=lambda item: -item[1]):
        print(key, value)


def add_tripool_liquidity():
    dai_addr = "0x6B175474E89094C44Da98b954EedeAC495271d0F"
    usdc_addr = "0xA0b86991c6218b36c1d19D4a2e9Eb0cE3606eB48"

    amount = 100_000 * 10 ** 18
    dai = MintableForkToken(dai_addr)
    dai._mint_for_testing(accounts[0], amount)

    pool_addr = registry.find_pool_for_coins(dai_addr, usdc_addr)
    pool = load_contract(pool_addr)

    dai.approve(pool_addr, amount, {"from": accounts[0]})
    pool.add_liquidity([amount, 0, 0], 0, {"from": accounts[0]})

    return pool

# XXX To be completed in Part 2

def ape(pool, tripool_lp, pool_index):

    # Approve Deposit from Tripool to Metapool

    # Add Liquidity

    # Check if Pool Has Gauge

    # Create Approval For Rewards

    # Deposit

    return


def calc_cur_value():
    # Get Initial Value

    # Drain CRV

        # Check Gauge Exists

        # Add Gauge to Claim

    # Mint Many

    # Calculate Balance

    # Undo Mint Many


def calc_balance():
    # Convert CRV balance to readable form
