from brownie import *


# Check underlying balances of TriCrypto
def main():
    tri = Contract("tricrypto2")
    tri_lp = Contract("tricrypto2_lp")
    total_price = 0
    for i in range(3):
        price = tri.price_oracle(i - 1) / 10 ** 18 if i > 0 else 1
        decimals = Contract(tri.coins(i)).decimals()
        symbol = Contract(tri.coins(i)).symbol()
        spot_price = tri.balances(i) * price / 10 ** decimals
        total_price += spot_price
        print(symbol, spot_price)

    lp_tokens = tri_lp.totalSupply() / 10 ** 18
    print(total_price / lp_tokens) #* (tri.virtual_price() / 10 ** 18))

