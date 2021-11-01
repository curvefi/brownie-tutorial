import pytest
from brownie import Contract
from brownie.test import given, strategy

@given(pool_id=strategy("uint", min_value=0, max_value=41))
def test_stake_contract_dai(stake, dai, alice, registry, pool_id):
    pool = Contract(registry.pool_list(pool_id))
    coin_list = registry.get_coins(pool) + registry.get_underlying_coins(pool)
    if dai.address not in coin_list:
        return
    if registry.get_pool_asset_type(pool) > 0:
        return
    dai.transfer(stake, dai.balanceOf(alice), {'from': alice})
    stake.ape(dai, pool, {'from': alice})
    assert dai.balanceOf(stake) == 0
