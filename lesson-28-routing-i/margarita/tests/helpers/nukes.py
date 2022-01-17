from brownie import *
from brownie_tokens import MintableForkToken


# Deposit Tether into TriPool to artificial pump other asset prices
def nuke(
    tri, coin, test_addr, nuke_amt=100_000, trials=100, coin_id=0,
):

    coin_amt = nuke_amt * 10 ** coin.decimals()
    total_minted = 0

    for j in range(trials):
        try:
            coin._mint_for_testing(test_addr, coin_amt)
            _bal = coin.balanceOf(test_addr)
            safe_approve(coin, tri, _bal, test_addr)
            arr = [0, 0, 0]
            arr[coin_id] = _bal
            actual = tri.add_liquidity(arr, 0, {"from": test_addr})
            total_minted += _bal

        except Exception as e:
            pass

    # print(f"Minted and Deposited {total_minted / 10 ** coin.decimals():.2f}")
    return total_minted / 10 ** coin.decimals()


# Reverse the Nuke function back to initial state
def reverse_nuke(tri, tri_lp, coin, test_addr, trials=100, coin_id=0):
    lp_bal = tri_lp.balanceOf(test_addr)
    withdraw_amt = int(lp_bal / trials)
    for j in range(trials):
        try:
            tri.remove_liquidity_one_coin(withdraw_amt, coin_id, 0, {"from": test_addr})
        except:
            pass

    # Get remainder
    if tri_lp.balanceOf(test_addr) > 0:
        tri.remove_liquidity_one_coin(
            tri_lp.balanceOf(test_addr), coin_id, 0, {"from": test_addr}
        )

    return coin.balanceOf(test_addr) / 10 ** coin.decimals()


# Test aping first through TriCrypto then back through Sushi
def ape_strat_1(coins, c1, c2, ninja):
    tri = Contract("tricrypto")
    sushi = Contract("sushi_router")
    coins[c1].approve(tri, coins[c1].balanceOf(ninja), {"from": ninja})
    tri.exchange(c1, c2, coins[c1].balanceOf(ninja), 0, {"from": ninja})
    print(f"=============\nFirst Strategy\n=============")
    print(
        f"TriCrypto yielded {coins[c2].balanceOf(ninja) / 10 ** coins[c2].decimals():.2f} {coins[c2].symbol()}"
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
    print(f"Back through Sushi yielded {final_val:.2f} {coins[c1].symbol()}")
    print(f"Difference: {final_val - initial_val:.2f}")


# Test aping first through Sushi then back through TriCrypto
def ape_strat_2(c1, c2, i1, i2, ninja, tri, sushi):

    # First Move
    c1.approve(sushi, c1.balanceOf(ninja), {"from": ninja})

    sushi.swapExactTokensForTokens(
        c1.balanceOf(ninja),
        0,
        [c1, c2],
        ninja,
        chain.time() + 24 * 60 * 60,
        {"from": ninja},
    )

    partial_val = c2.balanceOf(ninja) / 10 ** c2.decimals()

    # And Back
    c2.approve(tri, c2.balanceOf(ninja), {"from": ninja})
    tri.exchange(i2, i1, c2.balanceOf(ninja), 0, {"from": ninja})
    final_val = c1.balanceOf(ninja) / 10 ** c1.decimals()


# Run the arbitrage (using strategy 2)
def run_arb(amt, tri, sushi, tether, weth, test_addr):
    fqamt = amt * 10 ** tether.decimals()
    tether._mint_for_testing(test_addr, fqamt)
    ape_strat_2(tether, weth, 0, 2, test_addr, tri, sushi)


# Approve, but don't fail if already approved
def safe_approve(origin, target, bal, addr):
    existing_allowance = origin.allowance(addr, target)

    try:
        if bal > existing_allowance:
            origin.approve(target, bal - existing_allowance, {"from": addr})
    except:
        print(f"Could not approve {origin} {target} {bal} {addr}")
        pass
