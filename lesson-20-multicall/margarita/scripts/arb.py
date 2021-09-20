from brownie import *
from brownie_tokens import MintableForkToken

from scripts.tri_nuke import nuke, reverse_nuke


# Check arbitrage strategies between Curve and Sushi
def main():
    nuke_val = 1_000_000
    arb_val = 1_000_000

    print("\n=========\nNuking\n=========\n")
    nuke_total = nuke(nuke_val, 100)
    initial_val = nuke_total + arb_val
    check_arb(arb_val)
    return
    # run_arb(arb_val)

    print("\n=========\nUnnuking\n=========\n")
    reverse_nuke(100)

    tri = Contract("tricrypto")
    coin = Contract(tri.coins(0))
    final_val = coin.balanceOf(accounts[0]) / 10 ** coin.decimals()
    print(f"Difference: {final_val - initial_val:,.2f}")


# Execute Arbitrage Strategy 2
def run_arb(amt):
    tri = Contract("tricrypto")
    coins = []
    for c in range(3):
        coins.append(MintableForkToken(tri.coins(c)))

    fqamt = amt * 10 ** coins[0].decimals()
    coins[0]._mint_for_testing(accounts[0], fqamt)
    ape_strat_2(coins, 0, 2, accounts[0])


# Test both arbitrage strategies and display the result
def check_arb(initial_val=40000):
    ninja = accounts[0]
    tri = Contract("tricrypto")
    coins = []
    for c in range(3):
        coins.append(MintableForkToken(tri.coins(c)))

    amount = initial_val * 10 ** coins[0].decimals()
    c1 = 0
    c2 = 2

    coins[c1]._mint_for_testing(ninja, amount)

    chain.snapshot()

    # One Direction
    _val = ape_strat_1(coins, c1, c2, ninja)
    print(f"Difference: {_val - initial_val:,.2f}")
    chain.revert()

    _val = ape_strat_2(coins, c1, c2, ninja)
    print(f"Difference: {_val - initial_val:,.2f}")
    chain.revert()


# Arbitrage Strategy 1: TriCrypto Through Sushi
def ape_strat_1(coins, c1, c2, ninja):
    tri = Contract("tricrypto")
    sushi = Contract("sushi_router")
    coins[c1].approve(tri, coins[c1].balanceOf(ninja), {"from": ninja})
    tri.exchange(c1, c2, coins[c1].balanceOf(ninja), 0, {"from": ninja})
    print(f"=============\nArbitrage Strategy 1\n=============")
    print(
        f"TriCrypto yielded {coins[c2].balanceOf(ninja) / 10 ** coins[c2].decimals():,.2f} {coins[c2].symbol()}"
    )

    # Other Direction
    coins[c2].approve(sushi, coins[c2].balanceOf(ninja), {"from": ninja})

    sushi.swapExactTokensForTokens(
        coins[c2].balanceOf(ninja),
        0,
        [coins[c2], coins[c1]],
        ninja,
        chain.time() + 24 * 60 * 60,
        {"from": ninja},
    )

    final_val = coins[c1].balanceOf(ninja) / 10 ** coins[c1].decimals()
    print(f"Back through Sushi yielded {final_val:,.2f} {coins[c1].symbol()}")
    return final_val


# Arbitrage Strategy 2: Sushi through TriCrypto
def ape_strat_2(coins, c1, c2, ninja):
    tri = Contract("tricrypto")
    sushi = Contract("sushi_router")
    print(f"\n=============\nArbitrage Strategy 2\n=============")

    # First Move
    coins[c1].approve(sushi, coins[c1].balanceOf(ninja), {"from": ninja})

    sushi.swapExactTokensForTokens(
        coins[c1].balanceOf(ninja),
        0,
        [coins[c1], coins[c2]],
        ninja,
        chain.time() + 24 * 60 * 60,
        {"from": ninja},
    )

    partial_val = coins[c2].balanceOf(ninja) / 10 ** coins[c2].decimals()
    print(f"Sushi yielded {partial_val:,.2f} {coins[c2].symbol()}")

    # And Back
    coins[c2].approve(tri, coins[c2].balanceOf(ninja), {"from": ninja})
    tri.exchange(c2, c1, coins[c2].balanceOf(ninja), 0, {"from": ninja})
    final_val = coins[c1].balanceOf(ninja) / 10 ** coins[c1].decimals()
    print(f"Back through TriCrypto yielded {final_val:,.2f} {coins[c1].symbol()}")
    return final_val
