# Parametrized Testing

## [🎥 Video 10: Parametrized Testing 🎬](https://youtu.be/Ogomm9Up0cA)

Brownie utilizes Pytest, which has advanced testing capabilities.  Pytest's parametrization capabilities allow you to execute your tests against a variety of inputs.

## BROWNIE + PYTEST

### Test Structure
Parametrized tests are slow, so they are often stored in a different directory and run separately.

	$ brownie test test/unitary       # Non-Parametrized Tests
	$ brownie test test/integrative   # Parametrized Tests


### Parametrization Decoration
Pass parameters to your tests by calling the decorator

	> @pytest.mark.parametrize('i', <strategy>)
	> def test_parametrized(i):
	> 	# Your Test Here
 	>	...

## CURVE REGISTRY FUNCTIONS

### Get Coin Swap Complement
Return the pool at offset **i** from all Curve pools using a particular coin

	> registry.get_coin_swap_complement(<coin>, <i>)

### Find Pool For Coins
Find the corresponding Curve pool for two coins.

	> registry.find_pool_for_coins(<coin1>, <coin2>)


### Get N Coins
Get the number of coins in a Curve pool

	> registry.get_n_coins(<curve_pool_addr>)

### Get Coin Indices
Find the coin index within a Curve pool

	> registry.get_coin_indices(<curve_pool>, <first_coin>, <second_coin>)



