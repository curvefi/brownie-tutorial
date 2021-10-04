# Deployment

## [🎥 Video 21: Deployment 🎬](https://youtu.be/u5eLhpGKtbM)
 
A deployment script can help you quickly push your contract to various chains when ready.  This lesson covers some deployment basics to make sure any contract you develop will work well on your local blockchain, testnets, and when you're ready, the mainnet.

## ACCOUNTS
You may need funded accounts to deploy to testnets and the live blockchain.  Storing your accounts into brownie will store the account's sensitive details in a password protected keystore.

### IMPORT ACCOUNT FROM PRIVATE KEY
Provide Brownie a private key and password for encryption.
Your account will be permanently accessible from this id.

	> brownie accounts new <id>

### UNLOCKING ACCOUNTS
Unlock an encrypted account for use in live or testing environments.
This account will be added to the Accounts list on success.

	> brownie load <id>


## GAS
When deploying to mainnet you may want to adjust the default gas prices.  Some updated functions help with gas after EIP-1559:

### PRIORITY FEE
Set a tip to be added to the base transaction fee to push your transaction faster.

	> from brownie.network import priority_fee
	> priority_fee("2 gwei")

### MAX FEE
Cap the total fee you are willing to pay for your transaction.

	> from brownie.network import max_fee
	> max_fee("50 gwei")


## PUBLISHING SOURCE
When your source is published to Etherscan, anybody can review the contract, pull the ABI, and interact directly on Etherscan.

### DEPLOY AND PUBLISH SOURCE
During deployment, verify your source code on Etherscan.

	> MyContract.deploy(*args, {'from': your_acct}, publish_source=True)

### LOAD CONTRACT
Create a ContractContainer object from a known deployment address by using any ContractInterface loaded to Brownie.

	> contract_object = ContractInterface.at(<address>)

### PUBLISH SOURCE AFTER DEPLOYMENT
If you failed to publish source at deployment, you can publish retroactively.

	> ContractInterface.publish_source(contract_object)

