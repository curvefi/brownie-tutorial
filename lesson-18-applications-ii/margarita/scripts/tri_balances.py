from brownie import *


# Check underlying balances of TriCrypto
def main():
    tri = Contract("tricrypto")
    for i in range(3):
        # Can substitute price_oracle with price_scale for closer balances
        price = tri.price_oracle(i - 1) / 10 ** 18 if i > 0 else 1
        decimals = Contract(tri.coins(i)).decimals()
        symbol = Contract(tri.coins(i)).symbol()
        print(symbol, tri.balances(i) * price / 10 ** decimals)
