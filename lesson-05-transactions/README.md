# Transactions

## [🎥 Video 5: Transactions 🎬](https://www.youtube.com/watch?v=4n-wvaO-21o)


The [TransactionReceipt](https://eth-brownie.readthedocs.io/en/stable/core-transactions.html) object provides information about a transaction, as well as various methods to aid in debugging.


## ERC20 approve()
Authorize a transfer between two wallets

	>>> token.approve(<to_wallet>, amount, {'from': <to_wallet>})


## ERC20 transferFrom()
Prebuilt function to move tokens between two wallets.  Will fail without approval.

	>>> token.transferFrom(
        	   <from_wallet>, 
	           <to_wallet>, 
	           <amount> 
	           {'from': <to_wallet>})


## BROWNIE INTERACTIVE MODE
When a test fails, open a console to allow interactive debugging.

	$ brownie test --interactive


## HISTORY
The _history_ variable provides a list of every transaction made in the current session

	>>> history
	[ <tx1>, <tx2>, ... ]


## LOAD TRANSACTION
Create a TransactionReceipt object from a transaction hash

	>>> chain.get_transaction(<txhash>)
