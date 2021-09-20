from brownie import *
from brownie_tokens import MintableForkToken

tri = Contract("tricrypto")
tri_lp = Contract("tricrypto_lp")
tri_rewards = Contract("tricrypto_rewards")
test_addr = accounts[0]

coin_id = 0
coin = MintableForkToken(tri.coins(coin_id))

# Rapidly deposit to Curve TriCrypto to test effect on price
def main():
    print("\n==Beginning==\n")
    current_state()

    nuke()
    print("\n==After Nuke==\n")
    current_state()

    reverse_nuke()
    print("\n==Reverse the Nuke==\n")
    current_state()
    portfolio_state(accounts[0])


# Current state of TriCrypto
def current_state():
    balances = []
    total_balance = 0
    print("Current state of TriCrypto")
    for b in range(3):
        _coin = Contract(tri.coins(b))
        decimals = _coin.decimals()
        if b - 1 >= 0:
            price = tri.price_oracle(b - 1) / 10 ** 18
            price_scale = tri.price_scale(b - 1) / 10 ** 18
        else:
            price = 1
            price_scale = 1
        _bal = (tri.balances(b) * price) / 10 ** decimals
        print(
            f"{_coin.symbol()} ({_bal:,.0f}): Price ${price:.2f}, Scale: ${price_scale:.2f}"
        )
        balances.append(_bal)
        total_balance += _bal
    return total_balance


# Current state of a user portfolio
def portfolio_state(test_addr):
    print("\nPortfolio State")
    for i in range(3):
        _coin = Contract(tri.coins(i))
        _bal = _coin.balanceOf(test_addr) / 10 ** _coin.decimals()
        if i - 1 >= 0:
            price = tri.price_oracle(i - 1) / 10 ** 18
        else:
            price = 1
        print(f"{_coin.symbol()}: {_bal:,.2f} @ {price:.2f} = {_bal * price:,.2f}  ")


# Deposit Tether into TriPool to artificial pump other asset prices
def nuke(nuke_amt=1_000_000, trials=200):
    coin_amt = nuke_amt * 10 ** coin.decimals()
    tri_lp = Contract("tricrypto_lp")

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
            print(e)
            pass

    print(
        f"Minted and Deposited {trials} @ {nuke_amt:,.2f} = {total_minted / 10 ** coin.decimals():,.2f}"
    )
    return total_minted / 10 ** coin.decimals()


# Undo the Nuke function back to an initial state
def reverse_nuke(trials=200):
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


# Approve, but don't fail if already approved
def safe_approve(origin, target, bal, addr):
    existing_allowance = origin.allowance(addr, target)

    try:
        if bal > existing_allowance:
            origin.approve(target, bal - existing_allowance, {"from": addr})
    except:
        print(f"Could not approve {origin} {target} {bal} {addr}")
        pass
