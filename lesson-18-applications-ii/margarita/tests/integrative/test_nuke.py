import pytest
from brownie.test import given, strategy
from brownie_tokens import MintableForkToken
from helpers.nukes import nuke, reverse_nuke, run_arb
from helpers.utils import *


# Fail if script successfully exploits arbitrage opportunity in Curve TriCrypto
@given(
    nuke_amt=strategy("uint", min_value=1000, max_value=50_000_000),
    arb_amt=strategy("uint", min_value=1000, max_value=50_000_000),
    nuke_trials=strategy("uint", min_value=250, max_value=1000),
    unnuke_trials=strategy("uint", min_value=250, max_value=1000),
)
def test_arb(
    nuke_amt,
    arb_amt,
    nuke_trials,
    unnuke_trials,
    tricrypto,
    tether,
    weth,
    sushi,
    tricrypto_lp,
):

    nuke_val = nuke(tricrypto, tether, accounts[0], nuke_amt, nuke_trials, 0)
    assert nuke_val == nuke_amt * nuke_trials
    run_arb(arb_amt, tricrypto, sushi, tether, weth, accounts[0])
    reverse_nuke(tricrypto, tricrypto_lp, tether, accounts[0], unnuke_trials)
    final_amt = tether.balanceOf(accounts[0]) / 10 ** tether.decimals()

    assert final_amt < (nuke_val + arb_amt)
