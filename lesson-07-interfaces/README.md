# Interfaces

## [🎥 Video 7: Interfaces 🎬](https://youtu.be/jh9AuCfw6Ck)


The Brownie interfaces folder holds interface source files that may be referenced by contract sources, but which are not considered to be primary components of the project.


## INTERFACES

Stored in the brownie interfaces/ directory as any of the following filetypes
  * Solidity (.sol)
  * Vyper (.vy)
  * ABI (.json)

Generate a .vy interface or ABI .json file using Vyper:

	$ vyper -f external_interface <filename>
	$ vyper -f abi <filename>

Create a Brownie Contract object from an interface file in the interface directory:

	> from brownie import interface
	> contract = interface.<file_handle>(<contract_address>)

Generate a contract by fetching the contract's ABI directly from Etherscan:

	> Contract.from_explorer(<contract_address>)


## CURVE INTERACTIONS

Curve Registry function to retrieve reward gauge address

	> liquidity_gauge = registry.get_gauges(<curve_pool_addr>)


Retrieve the LP Token, an ERC-20 standard token issued for Curve liquidity pool providers.

	> liquidity_gauge.lp_token()

Deposit funds after approval

	> liquidity_gauge.deposit(<amount>)


Full sequence to stake into a rewards gauge:

	gauges = registry.get_gauges(pool_addr)
	gauge_addr = gauges[0][0]
	gauge_contract = interface.LiquidityGauge(gauge_addr)
	
	lp_token = MintableForkToken(
	    gauge_contract.lp_token()
	)

	lp_token.approve(gauge_addr, amount, {'from': accounts[0]})

	gauge_contract.deposit(lp_token.balanceOf(accounts[0]), {'from': accounts[0]})

