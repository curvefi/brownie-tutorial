# Networks

## [🎥 Video 14: Networks 🎬](https://youtu.be/S8gBMZtdsVM)

Brownie can easily be configured to work with many blockchains.  This lesson explores setting up Fantom and Polygon.

## NETWORKS

* [Fantom](https://fantom.foundation/) ([$FTM](https://www.coingecko.com/en/coins/fantom)) is a directed acyclic graph smart contract platform
* [Polygon](https://polygon.technology) ([$MATIC](https://www.coingecko.com/en/coins/polygon)) previously known as the Matic Network, is a platform for Ethereum scaling and infrastructure development. 

## LIST NETWORKS
Show all currently configured Brownie networks

	> brownie networks list

## ADD NETWORK

	> brownie networks add <environment> <id> host=<host> chainid=<chainid> explorer=<explorer> name=<name>

## VIEW NETWORK PROPERTIES
Show full properties of all configured networks

	> brownie networks list true

## CONFIGURATION FILE
Configuration stored by default in your home directory at .brownie/network-config.yaml


## LAUNCH NETWORK

	> brownie console --network <id>

## NETWORK COMMANDS
The network object contains some basic commands

	> network.is_connected()
	> network.show_active()

