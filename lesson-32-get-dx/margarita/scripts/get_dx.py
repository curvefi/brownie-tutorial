from brownie_tokens import MintableForkToken

from brownie import Contract, a
from scripts.helpers.iter import get_iter_est

calc = Contract("0xc1DB00a8E5Ef7bfa476395cdbcc98235477cDE4E")
exchange = Contract("exchange")
tripool = Contract("3pool")
registry = Contract("registry")


def main():
    get_dx(tripool, 0, 1, 25_000)


def get_dx(pool, i, j, dy):
    dx_coin = MintableForkToken(pool.coins(i))
    dy_coin = Contract(pool.coins(j))
    target = dy * 10 ** dy_coin.decimals()

    # Iterative Estimate
    iter_est = get_iter_est(pool, i, j, target)
    print(f"Iter Est: {iter_est} yields {pool.get_dy(i, j, iter_est)} ")

    # Calculator Estimate
    params = get_params(pool, i, j, target, False)
    calc_dx = calc.get_dx(*params)
    print(f"Calc Est: {calc_dx} yields {pool.get_dy(i, j, calc_dx)}")

    # Actual Value
    dx_coin._mint_for_testing(a[0], calc_dx)
    dx_coin.approve(exchange, calc_dx, {"from": a[0]})
    exchange.exchange(pool, pool.coins(i), pool.coins(j), calc_dx, 0, {"from": a[0]})
    final_bal = Contract(pool.coins(j)).balanceOf(a[0])

    print(f"Target:   {target}")
    print(f"Real Bal: {final_bal}")
    print(final_bal == target)


def get_dy(pool, i, j, dx, use_funds=True):

    dx_coin = MintableForkToken(pool.coins(i))
    balance = dx * 10 ** dx_coin.decimals()

    # Pool Estimate
    pool_dy = pool.get_dy(i, j, balance)

    # Calculator Estimate
    params = get_params(pool, i, j, balance)
    calc_dy = calc.get_dy(*params)[0]

    print(f"Calc Est: {calc_dy}")
    print(f"Pool Est: {pool_dy}")

    # Actual Value
    if use_funds:
        dx_coin._mint_for_testing(a[0], balance)
        dx_coin.approve(exchange, balance, {"from": a[0]})
        exchange.exchange(
            pool, pool.coins(i), pool.coins(j), balance, 0, {"from": a[0]}
        )
        final_bal = Contract(pool.coins(j)).balanceOf(a[0])

    print(f"Real Bal: {final_bal}")
    print(calc_dy == pool_dy)


def get_params(pool, i, j, balance, as_array=True):
    n_coins = registry.get_n_coins(pool)[0]
    cap = 8
    balances = [0] * cap
    precisions = [0] * cap
    rates = registry.get_rates(pool)
    trade = [0] * 100

    for _coin in range(n_coins):
        _dec = 10 ** Contract(pool.coins(_coin)).decimals()
        balances[_coin] = pool.balances(_coin)
        precisions[_coin] = (10**18) / _dec

    trade[0] = balance
    if as_array is False:
        trade = balance

    return [
        n_coins,  # N Coins
        balances,  # Balances
        pool.A(),  # A
        pool.fee(),  # Fee
        rates,  # Rates
        precisions,  # Precisions
        False,  # Underlying  
        i,  # i
        j,  # j
        trade,  # dx
    ]
