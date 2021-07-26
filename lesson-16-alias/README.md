# Alias

## [🎥 Video 16: Alias 🎬](https://youtu.be/eje3KiggxQA)

Brownie's Alias property makes it easy to find and refer to commonly used contracts across sessions.

For future tutorials we will refer to some contracts directly using aliases.  The brownie script [curve_alias.py](curve_alias.py) within this folder can be run to dynamically derive common aliases we will use going forward.  We also include [its output](aliases.txt).


## SET CONTRACT ALIAS
Store an alias to quickly reference a Contract.  Persists between sessions.

	> loaded_contract.set_alias(<alias>)

## LOAD CONTRACT FROM ALIAS
Quickly retrieve contract based on alias

	> Contract(<alias>)

## REMOVE AN ALIAS
Removing an alias can help manage any collisions.
Each contract can only have one alias, and each alias must be unique.

	> Contract.set_alias(None)

