def test_mint(accounts, margarita):
    assert margarita.balanceOf(accounts[0]) == 1e21


def test_name(accounts, margarita):
    assert margarita.symbol() == "MARG"


def test_stealable(accounts, margarita):
    margarita.approve(accounts[1], 1e21, {"from": accounts[0]})
    margarita.transferFrom(accounts[0], accounts[1], 1e21, {"from": accounts[1]})
    assert margarita.balanceOf(accounts[1]) == 1e21
