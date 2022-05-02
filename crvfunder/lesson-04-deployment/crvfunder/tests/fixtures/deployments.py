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
def admin_proxy(accounts):
    return accounts[-1]


@pytest.fixture(scope="module")
def CRVFunderLocal(charlie, FundraisingGaugeV1, crv20, gauge_controller, minter):
    src = FundraisingGaugeV1._build["source"]
    addrs = [
        "0xD533a949740bb3306d119CC777fa900bA034cd52",  # CRV
        "0x2F50D538606Fa9EDD2B11E2446BEb18C9D5846bB",  # Gauge Controller
        "0xd061D61a4d941c39E5453435B6345Dc261C2fcE0",  # Minter
    ]
    for old, new in zip(
        addrs, [crv20.address, gauge_controller.address, charlie.address, minter.address]
    ):
        src = src.replace(old, new, 1)

    return compile_source(src, vyper_version="0.3.1").Vyper


@pytest.fixture(scope="module")
def implementation(alice, admin_proxy, CRVFunderLocal):
    return CRVFunderLocal.deploy(admin_proxy, {"from": alice})


@pytest.fixture(scope="module")
def factory(alice, GaugeFactoryV1, implementation):
    return GaugeFactoryV1.deploy(implementation, {"from": alice})


@pytest.fixture(scope="module")
def funder(alice, factory, CRVFunderLocal):
    return CRVFunderLocal.at(
        factory.deploy_gauge(alice, 2**256 - 1, {"from": alice}).return_value
    )
