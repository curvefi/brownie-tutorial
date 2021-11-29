import pytest
from brownie import ZERO_ADDRESS, Contract
from brownie.test import given, strategy
from hypothesis import settings


@pytest.mark.skip()
@given(
    pool_id=strategy("uint", min_value=0, max_value=41, exclude=[3, 4, 9, 16, 17, 21])
)
def test_stake_contract_dai(stake, dai, alice, registry, pool_id):
    pool = Contract(registry.pool_list(pool_id))
    _coins = registry.get_coins(pool)
    _underlying = registry.get_underlying_coins(pool)
    coin_list = _coins + _underlying

    if dai.address not in coin_list:
        return

    dai.transfer(stake, dai.balanceOf(alice), {"from": alice})
    stake.ape(dai, pool, {"from": alice})
    assert dai.balanceOf(stake) == 0


@settings(max_examples=100)
@given(pool_id=strategy("uint", min_value=0, max_value=66, exclude=[53]))
def test_stake_factory_dai(stake, dai, alice, registry, pool_id):
    factory = Contract(stake.factory())
    pool = Contract(factory.pool_list(pool_id))

    # Is our target coin (dai) in the pool?
    if factory.is_meta(pool):
        coin_list = factory.get_underlying_coins(pool)
    else:
        coin_list = factory.get_coins(pool)

    # If DAI is not in the list, return
    if dai.address not in coin_list:
        return

    # If the Factory pool is low, return
    if pool.totalSupply() == 0:
        return

    if is_pool_low(factory, pool, dai.balanceOf(alice)):
        return

    dai.transfer(stake, dai.balanceOf(alice), {"from": alice})
    stake.ape(dai, pool, {"from": alice})
    assert dai.balanceOf(stake) == 0


# Calculate if the pool assets are low
def is_pool_low(factory, pool, val):
    total_bal = 0

    # Grabbing number of coins usually easy
    coin_count = factory.get_n_coins(pool)
    if coin_count == 0:
        coin_count = retrieve_coin_count(pool)

    # Append coin balance
    for c in range(coin_count):
        _decimals = Contract(pool.coins(c)).decimals()
        total_bal += pool.balances(c) / 10 ** _decimals

    # Finally, skip test if balance low
    if val > total_bal:
        return True
    else:
        return False


# Manually fetch coin count if fails directly
def retrieve_coin_count(pool):
    coin_count = 0
    for i in range(8):
        try:
            if pool.coins(i) != ZERO_ADDRESS:
                coin_count += 1
        except:
            pass
    return coin_count
