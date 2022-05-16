import csv

from brownie import *


def main():
    tricrypto = Contract("0xD51a44d3FaE010294C616388b506AcdA1bfAAE46")
    block = 12900000
    bal = 30 * 10 ** 18
    coin = ["usd", "btc", "eth"]
    suffices = ["_price", "_amt"]

    data = [["block"] + [_c + _s for _c in coin for _s in suffices]]

    while block < chain.height:
        print(block)
        _row = [block]
        for i in range(3):
            _dec = 10 ** Contract(tricrypto.coins(i)).decimals()
            if i > 0:
                _price = (
                    tricrypto.price_oracle(i - 1, block_identifier=block) / 10 ** 18
                )
            else:
                _price = 1
            _amt = (
                tricrypto.calc_withdraw_one_coin(bal, i, block_identifier=block) / _dec
            )
            _row += [_price, _amt]

        data.append(_row)
        block += 100000

    with open("tricrypto.csv", mode="w") as output_file:
        writer = csv.writer(output_file)
        for d in data:
            writer.writerow(d)
