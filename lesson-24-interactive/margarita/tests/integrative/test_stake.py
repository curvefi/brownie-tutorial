import pytest
from brownie import Contract
from brownie.test import given, strategy


@given(pool_id=strategy("uint", min_value=0, max_value=41, exclude=[4, 9, 16, 17, 21]))
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
