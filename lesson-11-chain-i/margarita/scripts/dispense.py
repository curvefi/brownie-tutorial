from brownie import *

def main():
    for i in range(10):
        shot(i)

def shot(i):
    return Token.deploy(
            'Margarita',
            'MARG',
            18,
            1e21,
            {'from': accounts[i]}
            )
