from brownie import *
from brownie_tokens import MintableForkToken
import json

def main():
    registry = Contract('0x7D86446dDb609eD0F5f8684AcF30380a356b2B4c')
    pool_addr = registry.find_pool_for_coins('0xEeeeeEeeeEeEeeEeEeEeeEEEeeeeEeeeeeeeEEeE', '0x5e74C9036fb86BD7eCdcb084a0673EFc32eA31cb');
    pool.add_liquidity([10e18,0],0,{'from': accounts[0], 'value': 10e18})

    gauge_addr = registry.get_gauges(pool_addr)
    gauge_contract = Contract(gauges[0][0])


    
def old_main():
        eth = '0xEeeeeEeeeEeEeeEeEeEeeEEEeeeeEeeeeeeeEEeE'
        target = '0x5e74C9036fb86BD7eCdcb084a0673EFc32eA31cb'
        ca = Contract.from_abi('CrossAsset', '0x58A3c68e2D3aAf316239c003779F71aCb870Ee47', load_abi('interfaces/crossasset.abi'))
        expected = ca.get_swap_into_synth_amount(eth, target, 10e10)
        run_swap = ca.swap_into_synth(eth, target, expected , 0, {'from': accounts[0], 'value': expected })

def load_abi(filename):
    with open(filename, 'r') as f:
        abi = json.load(f)
    return abi
