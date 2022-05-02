import brownie


def test_admin_can_kill(alice, admin_proxy, funder):
    assert funder.admin() == admin_proxy
    assert funder.inflation_rate() != 0

    funder.set_killed(True, {"from": admin_proxy})
    assert funder.inflation_rate() == 0
    assert funder.is_killed() is True


def test_nonowner_cannot_kill(funder, bob):
    with brownie.reverts():
        funder.set_killed(True, {"from": bob})


def test_deploys_with_inflation(funder, alice):
    assert funder.inflation_rate() > 0


def test_killing_ends_inflation(funder, admin_proxy):
    funder.set_killed(True, {"from": admin_proxy})
    assert funder.inflation_rate() == 0
