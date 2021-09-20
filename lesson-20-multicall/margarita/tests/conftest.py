#!/usr/bin/python3

import pytest
from brownie import Contract
from brownie_tokens import MintableForkToken
from helpers.utils import *


@pytest.fixture(scope="function", autouse=True)
def isolate(fn_isolation):
    # perform a chain rewind after completing each test, to ensure proper isolation
    # https://eth-brownie.readthedocs.io/en/v1.10.3/tests-pytest-intro.html#isolation-fixtures
    pass


@pytest.fixture(scope="module")
def margarita(Token, accounts):
    return Token.deploy("Margarita", "MARG", 18, 1e21, {"from": accounts[0]})


@pytest.fixture(scope="module")
def alice(accounts):
    return accounts[0]


@pytest.fixture(scope="module")
def bob(accounts):
    return accounts[1]


@pytest.fixture(scope="module")
def registry():
    return load_registry()


@pytest.fixture(scope="module")
def tripool(registry):
    return load_contract(registry.pool_list(0))


@pytest.fixture(scope="module")
def tripool_lp_token(registry, tripool):
    return load_contract(registry.get_lp_token(tripool))


@pytest.fixture(scope="module")
def tripool_funded(registry, alice, tripool):
    dai_addr = registry.get_coins(tripool)[0]
    dai = MintableForkToken(dai_addr)
    amount = 100000 * 10 ** dai.decimals()
    dai.approve(tripool, amount, {"from": alice})
    dai._mint_for_testing(alice, amount)

    amounts = [amount, 0, 0]
    tripool.add_liquidity(amounts, 0, {"from": alice})
    return tripool


@pytest.fixture(scope="module")
def tripool_rewards(alice, tripool_funded):
    return stake_into_rewards(tripool_funded, alice)

@pytest.fixture(scope="module")
def tricrypto():
    return Contract('tricrypto')

@pytest.fixture(scope="module")
def tricrypto_lp():
    return Contract('tricrypto_lp')



@pytest.fixture(scope="module")
def tether():
    return MintableForkToken('tether')

@pytest.fixture(scope="module")
def weth():
    return MintableForkToken('weth')

@pytest.fixture(scope="module")
def sushi():
    return Contract('sushi_router')

