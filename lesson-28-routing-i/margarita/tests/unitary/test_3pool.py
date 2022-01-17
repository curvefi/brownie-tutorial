from brownie import Contract, chain


def test_initially_no_balance(stake, tripool_rewards):
    assert tripool_rewards.balanceOf(stake) == 0


def test_stake_3pool(staked_3pool, tripool_rewards):
    assert tripool_rewards.balanceOf(staked_3pool) > 0


def test_dai_transfers(staked_3pool, tripool_rewards):
    assert Contract("dai").balanceOf(staked_3pool) == 0


def test_no_initial_balance(stake, tripool_rewards):
    crv = Contract("crv")
    assert crv.balanceOf(stake) == 0


def test_earns_rewards(staked_3pool, tripool_rewards):
    minter = Contract("minter")
    crv = Contract("crv")
    chain.mine(timedelta=60 * 60 * 24)
    minter.mint(tripool_rewards, {"from": staked_3pool})
    assert crv.balanceOf(staked_3pool) > 0


def test_can_withdraw(staked_3pool, tripool_rewards):
    dai = Contract("dai")
    staked_3pool.unape_balanced(Contract("3pool"))
    assert dai.balanceOf(staked_3pool) > 0


def test_can_claim(staked_3pool, tripool_rewards, alice):
    dai = Contract("dai")
    assert dai.balanceOf(alice) == 0

    staked_3pool.unape_balanced(Contract("3pool"))
    staked_3pool.claim_erc20(dai, {"from": alice})
    assert dai.balanceOf(alice) > 0


def test_can_claim_crv(staked_3pool, tripool_rewards, alice):
    crv = Contract("crv")
    minter = Contract("minter")
    assert crv.balanceOf(alice) == 0
    
    chain.mine(timedelta=60 * 60 * 24)
    minter.mint(tripool_rewards, {"from": staked_3pool})
    staked_3pool.unape_balanced(Contract("3pool"))
    staked_3pool.claim_erc20(crv, {"from": alice})
    assert crv.balanceOf(alice) > 0


