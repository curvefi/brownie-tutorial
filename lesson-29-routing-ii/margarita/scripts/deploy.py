from brownie import *
from brownie_tokens import *

def main():
    t = MintableForkToken('dai')
    pool = Contract('3pool')
    t._mint_for_testing(accounts[0], 100000 * 10 ** t.decimals())

    s = Stake.deploy(Contract('address_provider'), {'from': accounts[0]})
    t.transfer(s, t.balanceOf(accounts[0]), {'from': accounts[0]})

    print(s.show_balance(t).return_value)
    
    
