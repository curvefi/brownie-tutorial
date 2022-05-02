# CRVFunder 4: Deployment

## [🎥 Video 4: Testing 🎬](https://youtu.be/GiT1InNaExo)

The CRVFunder series is a short series exploring using Brownie at an application level.  Specifically, we'll be looking at how Brownie was used to help rapidly prototype the CRVFunder application.  CRVFunder launched a new fundraising gauge type to divert CRV inflation to any cause as voted on by the Curve DAO.

Throughout this series we'll be pointing to snapshots of the code in development.  The actual repository is available at [@vefunder/crvfunder](https://github.com/vefunder/crvfunder/).  The code contained here in the crvfunder directory shows the application snapshot as it existed at [63b4041](https://github.com/vefunder/crvfunder/commit/63b4041ff06ff6ea943a7d69ae233719c4411bbd)


## BROWNIE ACCOUNTS IMPORT
On the console, store an account by private key

    brownie accounts new <id>

To import from a keystore file

    brownie accounts import <id> <path>
 
Running pytest will return one of the following exit codes

## BROWNIE ACCOUNTS LOAD
Once an accounts has been saved, you can import it into your script

    accounts.load(id)


## PRIORITY FEE
Set a tip to be added to the base transaction fee to push your transaction faster.

    from brownie.network import priority_fee
    priority_fee("2 gwei")             # Set globally
    tx({"priority_fee": "2 gwei"})     # Per transaction


## LOADING DEPLOYED CONTRACTS
Any ContractContainer can load an implementation deployed to a specific address using the built-in "at" method

    my_contract = ContractContainer.at(<address>)
