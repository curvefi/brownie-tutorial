def test_alice_is_not_bob(
        alice, bob
    ):
    assert alice != bob

def test_tripool_initially_unfunded(
        tripool_lp_token, alice
    ):
    assert tripool_lp_token.balanceOf(alice) == 0


def test_tripool_funded(
        tripool_lp_token, alice, tripool_funded
    ):
    assert tripool_lp_token.balanceOf(alice) > 0
