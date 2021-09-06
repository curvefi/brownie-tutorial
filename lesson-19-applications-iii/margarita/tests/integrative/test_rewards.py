from brownie.test import given, strategy
from brownie import *
from helpers.utils import *


@given(index=strategy("uint8", min_value=0, max_value=38))
def test_current_strategy_best(index, alice, registry, tripool_rewards):
    # Assumptions
    final_time = chain.time() + 60 * 60 * 24
    threshhold = 0
    init_strategy = 34

    # Execute initial strategy
    if index == init_strategy:
        return
    if init_strategy is not None:
        init_strat = load_contract(registry.pool_list(init_strategy))
        init_rewards = tripool_to_meta(init_strat, alice, tripool_rewards)
        rewards_arr = [tripool_rewards, init_rewards]
    else:
        rewards_arr = [tripool_rewards]

    # Test initial strategy rewards
    chain.mine(timestamp=final_time)
    old_rewards = calc_cur_rewards(alice, rewards_arr)
    chain.revert()

    # Skip if the new stategy is invalid
    target = load_contract(registry.pool_list(index))
    new_rewards = tripool_to_meta(target, alice, tripool_rewards)

    if new_rewards is None:
        return

    # Test new strategy rewards
    chain.mine(timestamp=final_time)
    new_rewards = calc_cur_rewards(alice, [tripool_rewards, new_rewards])

    # Assert the initial_strategy is better than new
    assert new_rewards < (old_rewards * (1 + threshhold))
