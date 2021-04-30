import brownie


def test_withdraw_has_no_ticket(GrandCentral, unlockedRoute, accounts):
    with brownie.reverts("Address does not have a ticket."):
        GrandCentral.withdraw(unlockedRoute, {"from": accounts[1]})


def test_withdraw_success(GrandCentral, unlockedRoute, accounts):
    # arrange
    riderOneAmount = 10 ** 18 - 1
    riderTwoAmount = 5
    startingRiderOneBalance = accounts[1].balance()
    startingRiderTwoBalance = accounts[2].balance()

    # act
    GrandCentral.buyBusTicket(
        unlockedRoute, {"from": accounts[1], "amount": riderOneAmount}
    )
    GrandCentral.buyBusTicket(
        unlockedRoute, {"from": accounts[2], "amount": riderTwoAmount}
    )
    GrandCentral.withdraw(unlockedRoute, {"from": accounts[1]})
    GrandCentral.withdraw(unlockedRoute, {"from": accounts[2]})

    # assert
    assert GrandCentral.routeValue(unlockedRoute) == 0
    assert accounts[1].balance() == startingRiderOneBalance
    assert accounts[2].balance() == startingRiderTwoBalance


def test_withdraw_can_not_withdraw_twice(GrandCentral, unlockedRoute, accounts):
    # arrange
    riderOneAmount = 10 ** 18 - 1

    # act
    GrandCentral.buyBusTicket(
        unlockedRoute, {"from": accounts[1], "amount": riderOneAmount}
    )
    GrandCentral.withdraw(unlockedRoute, {"from": accounts[1]})

    with brownie.reverts("Address does not have a ticket."):
        GrandCentral.withdraw(unlockedRoute, {"from": accounts[1]})


def test_withdraw_only_depositers_can_withdraw(GrandCentral, unlockedRoute, accounts):
    # arrange
    riderOneAmount = 10 ** 18 - 1

    # act
    GrandCentral.buyBusTicket(
        unlockedRoute, {"from": accounts[1], "amount": riderOneAmount}
    )

    with brownie.reverts("Address does not have a ticket."):
        GrandCentral.withdraw(unlockedRoute, {"from": accounts[2]})


def test_cannot_withdraw_after_bus_departs(GrandCentral, departedBus, accounts):
    with brownie.reverts("Bus has already left."):
        GrandCentral.withdraw(departedBus, {"from": accounts[1]})
