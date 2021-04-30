import pytest
from brownie import Contract

@pytest.fixture(scope="session")
def dai():
    yield Contract.from_explorer("0x6B175474E89094C44Da98b954EedeAC495271d0F")

@pytest.fixture(scope="session")
def uniswap_dai_exchange():
    yield Contract.from_explorer("0x2a1530C4C41db0B0b2bB646CB5Eb1A67b7158667")

@pytest.fixture(scope="session", autouse=True)
def buy_dai(accounts, dai, uniswap_dai_exchange):
    uniswap_dai_exchange.ethToTokenSwapInput(
        1,  # minimum amount of tokens to purchase
        9999999999,  # timestamp
        {
            "from": accounts[0],
            "value": "10 ether"
        }
    )

def test_buy_dai(accounts, dai):
    assert dai.balanceOf(accounts[0]) > 0

