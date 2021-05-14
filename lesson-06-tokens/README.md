# Tokens

## [🎥 Video 6: Tokens 🎬](https://youtu.be/0JrDbvBClEA)


Use the brownie forked-mainnet feature to interact with live contracts and test basic token transactions.

## BROWNIE MAINNET FORK
Run brownie in mainnet fork to interact with contracts deployed to the live blockchain.  Requires an [Infura](https://infuria.io/) API key.

        $ export WEB3_INFURA_PROJECT_ID=<your_infura_key>
        $ brownie console --network mainnet-fork


## INSTALL BROWNIE TOKEN TESTER
[Brownie Token Tester](https://pypi.org/project/brownie-token-tester/) provides helper objects for generating ERC20s while testing a Brownie project.

        $ pipx inject eth-brownie brownie-token-tester


Mint tokens at will for common ERC20 tokens (ie USDC, DAI...)

        > from brownie_tokens import MintableForkToken
        > amount = <value> * <token_decimals>
        > token = MintableForkToken(<token_address>)
        > token._mint_for_testing(<target_address>, amount)


## BROWNIE CONTRACT OBJECT
Interact with a deployed contract that is not part of your project

        > from brownie import Contract
        > contract_object = Contract(<address>)        


## BROWNIE ACCOUNTS
Provides ten funded and unlocked accounts to interact with in Brownie.

        > from brownie import accounts


## CURVE FINANCE
**👑 King of DeFi 👑**
* [Website](https://curve.fi/)
* [Documentation](https://curve.readthedocs.io/)

The [Curve registry](https://curve.readthedocs.io/registry-overview.html) is a smart contract used to locate all active Curve contracts and perform high level interactions.  The active address may change and can be retrieved from [0x0000000022d53366457f9d5e68ec105046fc4383](https://etherscan.io/address/0x0000000022d53366457f9d5e68ec105046fc4383)

### Find Pool

Find a pool that allows for transactions between \<from\> and \<to\>. 
You can optionally include the offset \<i\> to get the i-th pool when multiple pools exist for the given pairing.

        > registry = Contract(<registry_address>)
        > pool_addr = registry.find_pool_for_coins(<from>, <to>, <i>)


### Add Liquidity
Deposit coins into a Curve pool as a [liquidity provider](https://curve.readthedocs.io/exchange-pools.html#liquidity-plain-pools) to earn yield.  Accepts an ordered list of \<coin_i_amount\> values for each coin the pool accepts. Reverts if return amount generated is less than \<min_amount\>.

        > pool = Contract(<pool_addr>)
        > amounts = [<coin_1_amount>, <coin_2_amount>, ...]
        > pool.add_liquidity(amounts, <min_amount>)


## DAI 
Dai is a decentralized stablecoin by [MakerDao](https://makerdao.com/) currently pegged to the value of the US dollar.  
* [Contract](https://etherscan.io/token/0x6B175474E89094C44Da98b954EedeAC495271d0F)


## USDC
A stablecoin pegged to the US dollar launched by [Centre](https://www.centre.io/), a collaboration of Circle and Coinbase.  
* [Contract](https://etherscan.io/token/0xA0b86991c6218b36c1d19D4a2e9Eb0cE3606eB48)

