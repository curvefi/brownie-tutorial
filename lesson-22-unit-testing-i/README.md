# Unit Testing I

## [🎥 Video 22: Unit Testing I 🎬](https://youtu.be/AzAEw9ZzqZo)

Brownie utilizes the pytest framework for unit testing. Pytest is a mature, feature-rich test framework. It lets you write small tests with minimal code, scales well for large projects, and is highly extendable.

The next several units review unit testing for a hypothetical contract to be deployed to the blockchain.

The [Stake.vy contract](margarita/contracts/Stake.vy) at present allows users to stake its balance directly into Curve 3pool rewards, but there are many issues with it at the moment, so it's certainly not recommended for deployment.  Although the contract is written in Vyper, the tutorial will mostly focus on the brownie unit tests.

A few [unit tests have been created](margarita/tests) and reviewed in the video.  Upcoming units will focus more on how to create robust tests in tandem with contract development.
