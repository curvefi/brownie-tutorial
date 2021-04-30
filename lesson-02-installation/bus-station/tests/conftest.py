#!/usr/bin/python3

import pytest


@pytest.fixture(scope="function", autouse=True)
def isolate(fn_isolation):
    # perform a chain rewind after completing each test, to ensure proper isolation
    # https://eth-brownie.readthedocs.io/en/stable/tests-pytest-intro.html#isolation-fixtures
    pass


@pytest.fixture(scope="module")
def GrandCentral(BusStation, accounts):
    return BusStation.deploy({"from": accounts[0]})


@pytest.fixture(scope="module")
def lockedRoute(GrandCentral, accounts):
    etherInWei = 10 ** 18
    return GrandCentral.deployRoute(
        accounts[0], 0, 10 ** 20, etherInWei, 5 * 60 * 60 * 24, {"from": accounts[1]}
    ).return_value


@pytest.fixture(scope="module")
def unlockedRoute(GrandCentral, accounts, chain):
    min_eth_in_wei = 10 ** 18
    sleep_time = 5 * 60 * 60 * 24
    route_id = GrandCentral.deployRoute(
        accounts[0], 0, 10 ** 20, min_eth_in_wei, sleep_time, {"from": accounts[1]}
    ).return_value
    chain.sleep(sleep_time)
    return route_id


@pytest.fixture(scope="module")
def discountRoute(GrandCentral, accounts, chain):
    min_eth_in_wei = 10 ** 10
    sleep_time = 5 * 60 * 60 * 24
    route_id = GrandCentral.deployRoute(
        accounts[0], 0, 10 ** 10, min_eth_in_wei, sleep_time, {"from": accounts[1]}
    ).return_value
    return route_id


@pytest.fixture(scope="module")
def departedBus(GrandCentral, accounts, chain):
    etherInWei = 10 ** 18
    sleep_time = 5 * 60 * 60 * 24
    deployed = GrandCentral.deployRoute(
        accounts[0], 0, 10 ** 20, etherInWei, sleep_time, {"from": accounts[1]}
    ).return_value

    # arrange
    riderOneAmount = 10 ** 18 - 1
    riderTwoAmount = 5

    # act
    GrandCentral.buyBusTicket(deployed, {"from": accounts[1], "amount": riderOneAmount})
    GrandCentral.buyBusTicket(deployed, {"from": accounts[2], "amount": riderTwoAmount})
    chain.sleep(sleep_time)
    GrandCentral.triggerBusRide(deployed)
    return deployed
