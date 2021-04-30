import brownie
from brownie.test import given, strategy


@given(amount=strategy("uint", max_value=10 ** 19, min_value=1))
def test_buy_bus_ticket_success(GrandCentral, unlockedRoute, accounts, amount):
    GrandCentral.buyBusTicket(
        unlockedRoute, {"from": accounts[3], "amount": amount}
    )
    assert GrandCentral.routeValue(unlockedRoute) == amount


@given(amount=strategy("uint", min_value=10 ** 10 + 1, max_value=10 ** 18))
def test_cannot_overpay(GrandCentral, discountRoute, accounts, amount):
    with brownie.reverts("Cannot exceed max ticket value."):
        GrandCentral.buyBusTicket(
            discountRoute, {"from": accounts[3], "amount": amount}
        )


@given(amount=strategy("uint", max_value=10 ** 18, min_value=1))
def test_can_double_ticket(GrandCentral, unlockedRoute, accounts, amount):
    GrandCentral.buyBusTicket(
        unlockedRoute, {"from": accounts[3], "amount": amount}
    )
    GrandCentral.buyBusTicket(
        unlockedRoute, {"from": accounts[3], "amount": amount}
    )
    assert GrandCentral.routeValue(unlockedRoute) == amount * 2


def test_second_purchase_cannot_overpay(GrandCentral, discountRoute, accounts):
    amount = 10 ** 10 - 100000
    GrandCentral.buyBusTicket(
        discountRoute, {"from": accounts[3], "amount": amount}
    )
    with brownie.reverts("Cannot exceed max ticket value."):
        tx = GrandCentral.buyBusTicket(
            discountRoute, {"from": accounts[3], "amount": amount}
        )


def test_buy_bus_ticket_no_money_sent(GrandCentral, unlockedRoute, accounts):
    with brownie.reverts("Need to pay more for ticket."):
        GrandCentral.buyBusTicket(unlockedRoute, {"from": accounts[3], "amount": 0})


def test_buy_bus_ticket_bus_already_left(GrandCentral, unlockedRoute, accounts):
    riderOneAmount = 10 ** 18 - 1
    riderTwoAmount = 5
    GrandCentral.buyBusTicket(
        unlockedRoute, {"from": accounts[1], "amount": riderOneAmount}
    )
    GrandCentral.buyBusTicket(
        unlockedRoute, {"from": accounts[2], "amount": riderTwoAmount}
    )
    GrandCentral.triggerBusRide(unlockedRoute)

    with brownie.reverts("The bus already left."):
        GrandCentral.buyBusTicket(unlockedRoute, {"from": accounts[3], "amount": 1})
