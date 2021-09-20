# Multicall 

## [🎥 Video 20: Multicall 🎬](https://youtu.be/Mtj8Vw2OviM)
  
Multicall is the process of batching several smart contract calls and routing a single call through a smart contract.   When running gas-consuming transactions, this can result in gas savings.   Even when running read-only transactions, it can be useful to retrieve results from the same block, rather than fetching data over multiple blocks.

If running on a development environment, this will deploy a Multicall contract used to process batch transactions. On live networks, Brownie routes through pre-defined or custom addresses.

Multicall is supported in Brownie as of 1.15.0.  For advanced options consult the [full documentation](https://eth-brownie.readthedocs.io/en/stable/api-network.html#brownie-network-multicall).

### UPDATE BROWNIE
Users who installed brownie using pipx can upgrade easily

	> pipx upgrade-all 

### INSTANTIATE MULTICALL
All relevant calls in the indented block are processed using Multicall

	> with brownie.multicall:
	...     # Calls to be batched

