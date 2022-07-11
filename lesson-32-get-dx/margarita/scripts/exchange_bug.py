from brownie import *
from brownie_tokens import MintableForkToken

def main():
    alice = accounts[0]
    tether = MintableForkToken('0xdAC17F958D2ee523a2206206994597C13D831ec7') 
    exchange = Contract('0xc64F268BD8075B3222A508d7869E9C600bE7c47F')
    weth = Contract('0xC02aaA39b223FE8D0A0e5C4F27eAD9083C756Cc2')
    tricrypto_old = Contract('0x80466c64868E1ab14a1Ddf27A676C3fcBE638Fe5')

    #tricrypto_old = Contract('tricrypto') 
    tether._mint_for_testing(alice, 5000 * 10 ** tether.decimals())
    _bal = tether.balanceOf(alice)
    assert _bal > 0

    tether.approve(exchange, _bal, {'from': alice})

    tether_exchange_init = tether.balanceOf(exchange)
    weth_exchange_init = weth.balanceOf(exchange)

    exchange.exchange(tricrypto_old, tether, weth, _bal, 0, {'from': alice})

    print("Final WETH",weth.balanceOf(alice))
    tether_exchange_bal_change = tether.balanceOf(exchange) - tether_exchange_init
    if(tether_exchange_bal_change > 0):
        print("Exchange balance increased", tether_exchange_bal_change)
