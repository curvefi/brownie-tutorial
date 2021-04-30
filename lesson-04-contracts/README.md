# Contracts and Basic Interaction

## [🎥 Video 4: Contracts 🎬](https://www.youtube.com/watch?v=mN73VcjELp4&list=PLVOHzVzbg7bFUaOGwN0NOgkTItUAVyBBQ)

## Basic Interaction

Three primary ways of interacting with a smart contract using Brownie

1. Scripts
2. Console
3. Tests


## CREATE NEW TOKEN

        $ brownie bake token

## USING SCRIPTS

Requires only the script name (i.e. filename excluding .py) if the script contains a “main” function

        $ brownie run <script_name>


## SCRIPT IMPORTS
Relevant brownie libraries must always be imported when writing scripts

        from brownie import *

## TOKEN DEPLOYMENT SYNTAX

        Token.deploy(<name>, <symbol>, <decimals>, <amount>, {‘from’: <owner>}) 

## RUNNING SCRIPTS
Also include the function name if you are not calling the “main” function

        $ brownie run <script_name> <function_name>


## CONSOLE SCRIPT ACCESS
Execute a script from the brownie console

        >>> run(<script_name>)

## TEST FIXTURES
tests/conftest.py contains testing fixtures used in  other tests.  This will be covered in future tutorials.

## BASIC TESTS
Include test_ as prefix in filename and function name i.e. tests/test_mint.py

        def test_<testname>(<fixtures>):
        	assert <condition>

## RUNNING TESTS

        $ brownie test <filepath>

