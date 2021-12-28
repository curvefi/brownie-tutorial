# Handling Raw Ethereum

## [🎥 Video 27: Raw ETH 🎬](https://youtu.be/TvaZ8o_xKdk)

Handling raw Ethereum is somewhat different from handling ERC20 tokens in Brownie and when programming smart contracts in Solidity and Vyper

# BROWNIE

## ACCOUNT BALANCE
For any unlocked account, the balance function returns the ETH balance in Wei

	> account.balance()

## ACCOUNT TRANSFER
Send an amount of raw ETH (or the equivalent output from the Wei function)

	> account.transfer(target, 10 ** 18)
	> account.transfer(target, "1 ether")

## TRANSACTION PARAMETERS
Brownie transaction executions can include a dictionary of parameters, commonly including the 'from' account.  The 'value' parameter is used to wire ETH to payable endpoints in Wei.

	> Contract.function({'from': account, 'value': 10 ** 18})


# FALLBACK FUNCTIONS
If your smart contract is intended to receive raw transfers, it must have an appropriate fallback function.

## SOLIDITY
As of Solidity 0.6.x, the fallback function got forked to receive() for accepting raw ether, and fallback() for other cases.

	> receive() external payable {
	> 	...
	> }


## VYPER
The Vyper fallback is handled by the `__default__` function.  It must be marked `@external` and may be marked @payable to receive ETH. 

	> @external
	> @payable
	> def __default__():
	>	...


# EVM PAYABLE FUNCTION CALLS
Send and receive Ethereum through a raw contract call within a smart contract

## SOLIDITY

	> Contract().function{_integer_}(...);


## VYPER

	> Contract().function(..., value=_integer_)


