import brownie


def test_trigger_bus_ride_locked(accounts, GrandCentral, lockedRoute):
    with brownie.reverts("Function is timelocked."):
        GrandCentral.triggerBusRide(lockedRoute)


def test_trigger_bus_ride_unlocked_no_tickets(accounts, GrandCentral, unlockedRoute):
    with brownie.reverts("Not enough wei to leave."):
        GrandCentral.triggerBusRide(unlockedRoute)


def test_trigger_bus_ride_success(accounts, unlockedRoute, GrandCentral):
    # arrange
    riderOneAmount = 10 ** 18 - 1
    riderTwoAmount = 5
    startingDestinationBalance = accounts[0].balance()
    startingRiderOneBalance = accounts[1].balance()
    startingRiderTwoBalance = accounts[2].balance()

    # act
    GrandCentral.buyBusTicket(
        unlockedRoute, {"from": accounts[1], "amount": riderOneAmount}
    )
    GrandCentral.buyBusTicket(
        unlockedRoute, {"from": accounts[2], "amount": riderTwoAmount}
    )
    GrandCentral.triggerBusRide(unlockedRoute)

    # assert
    assert GrandCentral.hasBusLeft(unlockedRoute) is True
    assert GrandCentral.routeValue(unlockedRoute) == 0
    assert (
        accounts[0].balance()
        == startingDestinationBalance + riderOneAmount + riderTwoAmount
    )
    assert accounts[1].balance() == startingRiderOneBalance - riderOneAmount
    assert accounts[2].balance() == startingRiderTwoBalance - riderTwoAmount


def test_cannot_trigger_after_departure(GrandCentral, accounts, departedBus):
    with brownie.reverts("Bus is already gone."):
        GrandCentral.triggerBusRide(departedBus)
