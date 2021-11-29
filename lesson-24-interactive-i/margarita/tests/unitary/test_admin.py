import brownie

def test_only_admin_can_claim(staked_3pool, dai, accounts):
    with brownie.reverts("dev: Only Owner"):
        staked_3pool.claim_erc20(dai, {'from': accounts[1]})
