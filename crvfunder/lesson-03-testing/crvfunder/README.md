# veFunder - CRV Fundraising via Emissions

The Curve DAO currently subsidises liquidity pools in exchange for fees. There's some bribing action happening, where external protocols influence veCRV voters in favor of their gauge, but largely the gauge is focussed on AMMs. This is because it's the current paradigm.

With the new generalised cross-chain gauge architecture, Curve inflation can be directed to any arbitrary ERC20 on a sidechain, with any arbitrary on-chain logic (subject to DAO approval). This has the potential to fund more than just subsidised liquidity pools. This product aims to showcase exactly this: a DAO approved crowdfunding endeavor. This also has the potential to position Curve DAO as a decentralised public goods funding source: provided it adds value to the Curve ecosystem.

## Overview

- [`FundraisingGaugeV1`](./contracts/FundraisingGaugeV1.vy): the implementation used for fundraising gauges
- [`GaugeFactoryV1`](./contracts/GaugeFactoryV1.vy): permissionless gauge factory for deploying fundraising gauges

### Dependencies

* [python3](https://www.python.org/downloads/release/python-368/) version 3.6 or greater, python3-dev
* [brownie](https://github.com/eth-brownie/brownie) - tested with version [1.18.1](https://github.com/eth-brownie/brownie/releases/tag/v1.17.2)
* [ganache-cli](https://github.com/trufflesuite/ganache-cli) - tested with version [6.12.1](https://github.com/trufflesuite/ganache-cli/releases/tag/v6.12.1)

### Testing

To run the unit tests:

```bash
$ brownie test -x
```

### Deployment

To deploy first edit the [`scripts/deploy.py`](./scripts/deploy.py) file to unlock the appropriate account, then run the following:

```bash
$ brownie run deploy --network mainnet
```

### Deployment Addresses

- `FundraisingGaugeV1`: [`0xCED78da2c749236309774d7415236B7090B3bF27`](https://etherscan.io/address/0xCED78da2c749236309774d7415236B7090B3bF27)
- `GaugeFactoryV1`: [`0x696B5D296a8AeF7482B726FCf0616E32fe72A53d`](https://etherscan.io/address/0x696B5D296a8AeF7482B726FCf0616E32fe72A53d)

### [`Gauge Factory V1`](./contracts/GaugeFactoryV1.vy) Spec

Below is a list of callable methods on the Gauge Factory V1 contract.

1. `deploy_gauge(_receiver: address, _max_emissions: uint256) -> address: nonpayable`: Deploy a new fundraising gauge

```python
>>> tx = factory.deploy_gauge(alice, 200 * 10 ** 18, {"from": alice, "priority_fee": "2 gwei"})
Transaction sent: 0xaa0af656794ef7bf25ae986b82ccf91c148c5af70869f9cdf7f23ab5cbcb35e6
  Gas price: 0.0 gwei   Gas limit: 9007199254740991   Nonce: 4
  GaugeFactoryV1.deploy_gauge confirmed   Block: 14376787   Gas used: 193770 (85.00%)
>>> tx.events["NewGauge"]
OrderedDict([('_instance', '0x521629cbe068e58b43f1aEaB73E47fC43231E67C'), ('_receiver', '0x66aB6D9362d4F35596279692F0251Db635165871'), ('_max_emissions', 200000000000000000000))])
```

Note: A gauge does not automatically receive emissions, it must be voted in by the Curve DAO and then veCRV voters must allocate voting power to change the gauge weight.

2. `implementation() -> address: view`: Get the implementation address used for creating proxies. This address is fixed at deployment and non-upgradeable

```python
>>> factory.implementation()
0xE7eD6747FaC5360f88a2EFC03E00d25789F69291
```

3. `get_gauge_count() -> uint256: view`: Get the total number of gauges deployed (these aren't necessarily voted in by the DAO

```python
>>> factory.get_gauge_count()
1
```

4. `get_gauge_by_idx(_idx: uint256) -> address: view`: Get the address of the gauge deployed at index `_idx`. This function returns `ZERO_ADDRESS` for indexes past `get_gauge_count()`

```python
>>> [factory.get_gauge_by_idx(i) for i in range(factory.get_gauge_count())]
["0x521629cbe068e58b43f1aEaB73E47fC43231E67C"]
```

### [`Fundraising Gauge V1`](./contracts/FundraisingGaugeV1.vy) Spec

After a gauge is deployed, voted in by the DAO, and receiving emissions, the `receiver` must call the [`Minter`](https://curve.readthedocs.io/dao-gauges.html#minting-crv) to collect their accumulated CRV.

1. `receiver() -> address: view`: The account which receives emissions from this gauge.

```python
>>> gauge.receiver()
'0x66aB6D9362d4F35596279692F0251Db635165871'
```

2. `max_emissions() -> uint256: view`: The maximum amount of emissions `receiver()` will receive, afterwards emissions will not accrue (akin to a supply burn)

```python
>>> gauge.max_emissions()
200000000000000000000
```

3. `claimable_tokens_write(_user: address) -> uint256: nonpayable`: The amount of CRV currently claimable by `_user`. This is a write method, but should be changed in the ABI to be a view method and called via `eth_call`.

```python
>>> gauge.claimable_tokens_write.call(alice)
1180591620717411303424
```

### License

(c) Curve.Fi, 2020 - [All rights reserved](LICENSE).

### Links

[Discord Link](https://discord.gg/PsNJQenbHm)
