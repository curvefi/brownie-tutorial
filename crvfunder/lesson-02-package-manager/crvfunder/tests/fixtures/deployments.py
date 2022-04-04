import pytest
from brownie import compile_source


@pytest.fixture(scope="module")
def curve_dao(pm):
    return pm("curvefi/curve-dao-contracts@1.3.0")


@pytest.fixture(scope="module")
def crv20(alice, chain, curve_dao):
    crv = curve_dao.ERC20CRV.deploy("Curve DAO Token", "CRV", 18, {"from": alice})
    chain.sleep(86400 * 14)  # let emissions begin
    crv.update_mining_parameters({"from": alice})
    return crv


@pytest.fixture(scope="module")
def voting_escrow(alice, crv20, curve_dao):
    return curve_dao.VotingEscrow.deploy(crv20, "Dummy VECRV", "veCRV", "v1", {"from": alice})


@pytest.fixture(scope="module")
def gauge_controller(alice, crv20, voting_escrow, curve_dao):
    return curve_dao.GaugeController.deploy(crv20, voting_escrow, {"from": alice})


@pytest.fixture(scope="module")
def minter(alice, crv20, gauge_controller, curve_dao):
    minter = curve_dao.Minter.deploy(crv20, gauge_controller, {"from": alice})
    crv20.set_minter(minter, {"from": alice})
    return minter


@pytest.fixture(scope="module")
def factory(alice, bob, Factory):
    return Factory.deploy(bob, {"from": alice})


@pytest.fixture(scope="module")
def CRVFunderLocal(alice, CRVFunder, crv20, gauge_controller):
    src = CRVFunder._build["source"]
    addrs = [
        "0xD533a949740bb3306d119CC777fa900bA034cd52",
        "0x2F50D538606Fa9EDD2B11E2446BEb18C9D5846bB",
    ]
    for old, new in zip(addrs, [crv20.address, gauge_controller.address]):
        src = src.replace(old, new, 1)

    return compile_source(src, vyper_version="0.3.1").Vyper


@pytest.fixture(scope="module")
def implementation(alice, CRVFunderLocal):
    return CRVFunderLocal.deploy({"from": alice})


@pytest.fixture(scope="module")
def funder(alice, factory, implementation, CRVFunderLocal):
    factory.set_implementation(implementation, {"from": alice})
    return CRVFunderLocal.at(
        factory.deploy(alice, 2**40 - 1, 2**128 - 1, {"from": alice}).return_value
    )
