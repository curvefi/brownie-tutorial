# Chain

## [🎥 Video 11: Chain 🎬](https://www.youtube.com/watch?v=3iywQibYDHw)

The Brownie chain object allows you to travel forwards and backwards through your local blockchain.  In these two units we use the chain to build a script that calculates the actual number of $CRV rewards staking the same amount would earn after 24 hours (assuming no changes).


## ZERO_ADDRESS
A variable in the brownie environment representing an empty address frequently returned when the parameter is empty.

        > ZERO_ADDRESS == '0x0000000000000000000000000000000000000000'

## CURVE MINTER
[Curve contract](https://etherscan.io/address/0xd061D61a4d941c39E5453435B6345Dc261C2fcE0) responsible for minting accumulated rewards and distributing them to the user.
