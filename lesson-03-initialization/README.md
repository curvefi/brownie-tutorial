# Initialization and Basic Structure

## [🎥 Video 3: Initialization 🎬](https://www.youtube.com/watch?v=8k7M8zq28So&list=PLVOHzVzbg7bFUaOGwN0NOgkTItUAVyBBQ)


## Project Initialization

        $ brownie init

## Brownie Structure
 * /contracts
 * /interfaces
 * /scripts
 * /tests

## Brownie Mixes

        $ brownie bake token

## Basic Console

        $ brownie console
        >>> my_token = Token.deploy("Test", "TST", 18, 10e21, {'from': accounts[0]})
        >>> my_token.transfer(accounts[1], 1e10, {'from': accounts[0]})

