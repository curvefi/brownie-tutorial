#!/usr/bin/python3

import pytest
from brownie import Contract, Stake
from brownie_tokens import MintableForkToken
from helpers.utils import load_registry


@pytest.fixture(scope="function", autouse=True)
def isolate(fn_isolation):
    # perform a chain rewind after completing each test, to ensure proper isolation
    # https://eth-brownie.readthedocs.io/en/v1.10.3/tests-pytest-intro.html#isolation-fixtures
    pass


@pytest.fixture(scope="module")
def margarita(Token, accounts):
    return Token.deploy("Margarita", "MARG", 18, 1e21, {"from": accounts[0]})


@pytest.fixture(scope="module")
def tripool():
    return Contract("3pool")


@pytest.fixture(scope="module")
def tripool_lp():
    return Contract("3pool_lp")


@pytest.fixture(scope="module")
def tripool_rewards():
    return Contract("3pool_rewards")


@pytest.fixture(scope="module")
def alice(accounts):
    return accounts[0]


@pytest.fixture(scope="module")
def registry():
    return load_registry()


@pytest.fixture(scope="module")
def dai(alice):
    dai = MintableForkToken("dai")
    dai._mint_for_testing(alice, 5_000 * 10 ** dai.decimals())
    return dai


@pytest.fixture(scope="module")
def usdc(alice, dai):
    usdc = MintableForkToken("usdc")
    dai.approve(Contract("3pool"), dai.balanceOf(alice), {"from": alice})
    Contract("3pool").exchange(0, 1, dai.balanceOf(alice), 0, {"from": alice})
    return usdc


@pytest.fixture(scope="module")
def stake(alice):
    return Stake.deploy(Contract("address_provider"), {"from": alice})


@pytest.fixture(scope="module")
def staked_3pool(registry, alice, stake, dai, tripool):
    dai.transfer(stake, dai.balanceOf(alice), {"from": alice})
    stake.ape(dai, tripool, {"from": alice})
    return stake
