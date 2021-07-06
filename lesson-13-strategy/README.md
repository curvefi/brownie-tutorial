# Strategy

## [🎥 Video 13: Strategy 🎬](https://youtu.be/XYJW0PgU7Vw)

The key object in every test is a strategy. A strategy is a recipe for describing the sort of data you want to generate. Brownie provides a strategy method that generates strategies for any given ABI type.


## PARAMETRIZED TESTING PROCESS

1. Fixtures executed 
2. Before each test a chain.snapshot() is created
3. Generate values from strategy
4. Test is executed
5. Chain reverted to snapshot
6. Repeat 50 times or until failure
7. Teardown of fixtures


## RUNNING STRATEGIES

        from brownie.test import given, strategy
        
        @given(my_var=strategy(<strategy type>, <parameters>))
        def test_basic_example(my_var):
                ...


## DEFAULTS
By default Brownie will execute 50 strategies per test, can be changed in brownie-config.yaml or by applying a `@settings` decorator

        @settings(max_examples=500)
        @given(strategy(...))
        def test_larger_example(...):
                ...
        

You can exclude a directory from being executed by pytest by creating a `setup.cfg` file

        [tool:pytest]
        norecursedirs=<dir>

## STRATEGY TYPES

Brownie can generate strategies based on multiple ABI types.  More details at the [Brownie documentation](https://eth-brownie.readthedocs.io/en/stable/tests-hypothesis-property.html#hypothesis-strategies)

* [Address](https://eth-brownie.readthedocs.io/en/stable/tests-hypothesis-property.html#address)
* [Boolean](https://eth-brownie.readthedocs.io/en/stable/tests-hypothesis-property.html#bool)
* [Bytes](https://eth-brownie.readthedocs.io/en/stable/tests-hypothesis-property.html#bytes)
* [Decimal](https://eth-brownie.readthedocs.io/en/stable/tests-hypothesis-property.html#decimal)
* [Integer](https://eth-brownie.readthedocs.io/en/stable/tests-hypothesis-property.html#integer)
* [String](https://eth-brownie.readthedocs.io/en/stable/tests-hypothesis-property.html#string) 
* [Array](https://hypothesis.readthedocs.io/en/latest/data.html#hypothesis.strategies.lists)
* [Tuple](https://eth-brownie.readthedocs.io/en/stable/tests-hypothesis-property.html#tuple)
* [Contract](https://eth-brownie.readthedocs.io/en/stable/tests-hypothesis-property.html#contract-strategies)

