# Networks

## [🎥 Video 14b: Polygon 🎬](https://www.youtube.com/watch?v=toqMi41c-l4)

Additional Setup Instructions for Connecting Brownie with Polygon

## NETWORKS

* [Polygon](https://polygon.technology) ([$MATIC](https://www.coingecko.com/en/coins/polygon)) previously known as the Matic Network, is a platform for Ethereum scaling and infrastructure development. 

## LIST NETWORKS
Show all currently configured Brownie networks

	> brownie networks list

## ADD NETWORK

	> brownie networks add <environment> <id> host=<host> chainid=<chainid> explorer=<explorer> name=<name>

## REMOVE NETWORK

	> brownie networks delete <id>

## VIEW NETWORK PROPERTIES
Show full properties of all configured networks

	> brownie networks list true

## CONFIGURATION FILE
Configuration stored by default in your home directory at .brownie/network-config.yaml

## LAUNCH NETWORK

	> brownie console --network <id>

## POLYGON ENVIRONMENT VARIABLES
Set environment variables so your environment works smoothly.  Register free API keys at Alchemy and Polygonscan

	> export WEB3_ALCHEMY_PROJECT_ID=<api_key>
	> export POLYGONSCAN_TOKEN=<token>

## NETWORK COMMANDS
The network object contains some basic commands

	> network.is_connected()
	> network.show_active()

## CURVE ADDRESS PROVIDER
On all chains, the Curve registry and other useful contracts
can be loaded from the permanent Address Provider

	> address_provider = Contract('0x0000000022d53366457f9d5e68ec105046fc4383')

