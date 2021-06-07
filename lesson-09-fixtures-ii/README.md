# Fixtures

## [🎥 Video 9: Fixtures 2 🎬](https://youtu.be/fhPXJtQBF54)


Fixtures provide quick access to custom Brownie objects frequently used throughout testing.  Visit the [Brownie Documentation](https://eth-brownie.readthedocs.io/en/stable/tests-pytest-intro.html#fixtures) for more detail and the [PyTest Documentation]( https://docs.pytest.org/en/6.2.x/) for additional background.


## FIXTURES

PyTest fixtures are located in tests/conftest.py

Fixtures are created by prepending the function with the fixture decorator

	@pytest.fixture
	def my_fixture():
		...


## FIXTURE SCOPES
The scope of the fixture can be passed to determine when the fixture is destroyed.

	@pytest.fixture(scope=_scope_)
	def my_fixture():
		...

  * **function:** (default) fixture destroyed at end of test
  * **class:** fixture destroyed at last test in class
  * **module:** fixture destroyed at last test in module
  * **session:** fixture destroyed at end of test session


## BROWNIE CONTRACT PERSISTENCE
After being created once, Brownie stores a copy of contracts in a local database that persists between sessions


## CURVE REGISTRY
Contract used to locate all active Curve contracts and perform high level interactions.  More information at the [Documentation](https://curve.readthedocs.io/registry-overview.html).  The active address may change and can be retrieved from the permanent [Address Provider contract](https://etherscan.io/address/0x0000000022d53366457f9d5e68ec105046fc4383)


## CURVE TRIPOOL
Core [Curve pool](https://curve.fi/3pool) allowing staking and transactions among DAI, USDC, and Tether stablecoins.  [DAI](https://etherscan.io/token/0x6B175474E89094C44Da98b954EedeAC495271d0F) is a decentralized stablecoin currently pegged to the value of the US dollar created by [MakerDAO](https://makerdao.com/)

