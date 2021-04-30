def test_mint(accounts, token):
    assert token.balanceOf(accounts[0]) == 1e21


def test_name(accounts, token):
    assert token.symbol() == "MARG"
