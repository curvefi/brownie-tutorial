import pytest
from conftest import load_contract


@pytest.mark.parametrize("i", range(10))
def test_3pool_redeposit(alice, registry, tripool_funded, tripool_lp_token, i):
    # Load Pool for a particular value i offset
    _complement = registry.get_coin_swap_complement(tripool_lp_token, i)
    _pool_addr = registry.find_pool_for_coins(tripool_lp_token, _complement)
    _pool = load_contract(_pool_addr)

    # Approve transfer
    _amount = 1e20
    tripool_lp_token.approve(_pool, _amount, {"from": alice})

    # Make the transfer, require [0, 1e20]
    amounts = [0] * (registry.get_n_coins(_pool)[0])
    _offsets = registry.get_coin_indices(_pool, tripool_lp_token, _complement)
    amounts[_offsets[0]] = _amount
    _pool.add_liquidity(amounts, 0, {"from": alice})

    # Verify the transfer, by looking at Alice's lp_token balance
    _pool_lq = load_contract(registry.get_lp_token(_pool))
    assert _pool_lq.balanceOf(alice) > 0
