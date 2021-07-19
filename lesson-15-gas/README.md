# Gas Optimization

## [🎥 Video 15: Gas 🎬](https://youtu.be/cBYvRLKO6bE)

To date our contracts have been tested in a gas free environment.  This lesson demonstrates basic gas techniques using Brownie.


## GAS FUNCTIONS

### GASNOW STRATEGIES
Execute at the current gas price reported via the [GasNow](https://www.gasnow.org/) API.  Available strategies: ['rapid', 'fast', 'standard', 'slow']

	> from brownie.network.gas.strategies import GasNowStrategy
	> GasNowStrategy(<strategy>) 

### GLOBAL GAS STRATEGY
Set default gas strategy for all transactions

	> from brownie.network import gas_price
	> gas_price(<gas_strategy>)

### CALL_TRACE
Inspect the full trace details of a transaction, including gas usage

	> tx.call_trace()

## BROWNIE RUNTIME CONFIGURATION

### SILENT MODE
Run scripts without displaying full transaction details.

	$ brownie run --silent

### BROWNIE DEFAULT NETWORK
Run your scripts without typing the --network flag.  Update brownie-config.yaml to set a default network to 

	> networks:
	>       default: <network_id>


## CURVE NOTES

### ETHEREUM POOLS
Ethereum is not an ERC-20 token, so adding liquidity to an Ethereum denominated pool requires passing funds at the transaction level.

	> eth_pool.add_liquidity([amount_in_wei, amount_other_tokens], min_mint, {'from': account, 'value': amount_in_wei})
