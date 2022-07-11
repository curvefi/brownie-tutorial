import random

from brownie import *
from brownie_tokens import MintableForkToken
from scripts.helpers.router import CurveRouter 

YOUR_ADDR = "0xBEA37e65138eF4e439c96Cd6B06240ca17750A62"
registry = Contract("registry")

def factory_main():
    #registry = Contract('crypto_registry')
    #registry = Contract('registry')
    factory = Contract('factory')
    
    alice = accounts[0]
    amount = 5000
    vals = {}
    chain.snapshot()
    for j in range(factory.pool_count()):
            _pool = Contract(factory.pool_list(j))
            for _ci in range(8):
                try:
                    _coin = Contract(_pool.coins(_ci))
                except:
                    continue
 #               _coin = Contract('0xC02aaA39b223FE8D0A0e5C4F27eAD9083C756Cc2')  # WETH
                if _coin.address in vals:
                    continue
                TokenMinter().mint(alice, amount, _coin.address)
                try:
                    _bal = _coin.balanceOf(alice)
                except:
                    _bal = None
                vals[_coin.address] = _bal
                chain.revert()
    for i, j in vals.items():
        try:
            print(i, Contract(i).symbol(), j)
        except:
            print(i, j)
    return


def main():
    #registry = Contract('crypto_registry')
    registry = Contract('registry')
    #registry = Contract('factory')
    
    alice = accounts[0]
    amount = 5000
    vals = {}
    chain.snapshot()
    for j in range(registry.coin_count()):
        i = j 
        #i = 6
        if prune_coins(i) is True:
            coin = registry.get_coin(i)
            print(f"Coin {i}")
            TokenMinter().mint(alice, amount, coin)
            try:
                _bal = Contract(coin).balanceOf(alice)
            except:
                _bal = None
            vals[i] = _bal
            #print(Contract(coin).name())
            #print(Contract(coin).balanceOf(alice))
           # assert False
           # break

            chain.revert()
    for i, j in vals.items():
        try:
            print(i, Contract(registry.get_coin(i)).symbol(), j)
        except:
            print(i, registry.get_coin(i), j)
    return


def prune_coins(_i):
    if _i == 31 or _i == 52:
        return False
    return True
    registry = Contract('registry')
        # Trouble with sEUR
    if _i in [15, 22, 23, 29, 40, 51]:
        return False

    target = registry.get_coin(_i)
    if target in registry.get_coins('0xDeBF20617708857ebe4F679508E7b7863a8A8EeE'):
        return False 

    if target in registry.get_coins('0x79a8C46DeA5aDa233ABaFFD40F3A0A2B1e5A4F27'):
        return False

    if target in registry.get_coins('0xA2B47E3D5c44877cca798226B7B8118F9BFb7A56'):
        return False

    # Something Yearn
    if target in registry.get_coins('0x2dded6Da1BF5DBdF597C45fcFaa3194e53EcfeAF'):
        return False
    # Another Something Yearn
    if target in registry.get_coins('0x06364f10B501e868329afBc005b3492902d6C763'):
        return False
    # Another yDAI, how many?
    if target in registry.get_coins('0x45F783CCE6B7FF23B2ab2D70e416cdb7D6055f51'):
        return False

    # Skip Ether for now
    if target == '0xEeeeeEeeeEeEeeEeEeEeeEEEeeeeEeeeeeeeEEeE':
        return False

    return True

class TokenMinter:
    registry = Contract('registry')
    verbose = True
    use_token_tester = True
    use_routing = True
    x = None
    ether = '0xEeeeeEeeeEeEeeEeEeEeeEEEeeeeEeeeeeeeEEeE'
    weth = '0xC02aaA39b223FE8D0A0e5C4F27eAD9083C756Cc2'
    tripool_lp = '0x6c3F90f043a72FA612cbac8115EE7e52BDe6E490'

    def __init__(self):
        self.x = Contract(Contract('0x0000000022d53366457f9d5e68ec105046fc4383').get_address(2))

    def mint(self, alice, usd_val, target):
        if self.mint_using_token_tester(alice, usd_val, target):
            return
        self.route_from_dai(alice, usd_val, target)

    # Use Brownie Token Tester to mint quickly
    def mint_using_token_tester(self, alice, usd_val, target):
        if self.use_token_tester is False:
            return False

        try:
            token = MintableForkToken(target)
            token._mint_for_testing(alice, usd_val * 10 ** token.decimals())
            assert token.balanceOf(alice) > 0

            self.vprint("Minted Easily")
            return True

        except Exception as e:
            return False
        

    # Mint DAI and then move tokens
    def route_from_dai(self, alice, usd_val, target):
        if self.use_routing is False:
            return False

        dai = MintableForkToken("dai")
        dai._mint_for_testing(alice, usd_val * 10 ** dai.decimals())
        if target == dai:
            return
         
        try:
            self.vprint(f"--- {Contract(target).symbol()} {target} ---")
        except:
            self.vprint(f"--- {target} ---")
            

        _bal = None
        path = TokenMinter().run_overall_path(dai.address, target, accounts[0])
        return

    #print(val_arr)
    # path = Router().find_crypto_path(dai, target)
    # print(path)

    # Run a complex route between any two coins
    def run_overall_path(self, addr1, addr2, alice):

        # Is there a direct path?
        direct_path = self.get_direct_path(addr1, addr2, alice)
        if direct_path != ZERO_ADDRESS:
            self.run_like_path(addr1, addr2, alice)
            return f"Direct {direct_path}"
        
        # Nope, take the more complicated way through crypto pools
        else:
            return self.run_crypto_path(addr1, addr2, alice)


    # Run any path that can be sent through the exchange 
    def run_route(self, _pool, _from, _to, alice, _balance = None):
        self.vprint(f"Running {_pool} {_from} to {_to}")
        if _pool == ZERO_ADDRESS:
            return
        x = self.x


        # What if the from coin is DAI, USDC, USDT and pool contains 3pool
        if _from in self.load_pool_coins(registry.get_pool_from_lp_token(self.tripool_lp)) and self.tripool_lp in self.load_pool_coins(_pool):
            tri = Contract('3pool')
            Contract(_from).approve(tri, Contract(_from).balanceOf(alice), {'from': a[0]})
            liqarr = self.build_liq_arr(tri, alice)
            tri.add_liquidity(liqarr, 0, {'from': alice})
            _from = self.tripool_lp

        if _from == self.ether:
            x.exchange(_pool, _from, _to, _balance, 0, {'from': alice, 'value': _balance})
            return

        _from_coin = Contract(_from)
        if _balance is None:
            _balance = _from_coin.balanceOf(alice)
        print(f"{_from_coin} bal {_balance}")

        #assert(_balance > 0)


        if _to == self.tripool_lp:
            tri = Contract('3pool')
            _from_coin.approve(tri, _balance, {'from': alice})
            liqarr = self.build_liq_arr(tri, alice)
            tri.add_liquidity(liqarr, 0, {'from': alice}) 

            assert Contract(self.tripool_lp).balanceOf(alice) > 0

        
        else:
            # See if coin is in exchange
            #try:
                #_from_coin.approve(_pool, _balance, {'from': alice})    
                #_pool_contract = Contract(_pool)

                #_pool_contract.exchange(
                        #_pool, 
                #        self.pool_index(_pool_contract, _from), 
                #        self.pool_index(_pool_contract, _to), 
                #        _balance, 
                #        0, 
                #        {'from': alice}
                #    )
                #assert Contract(_to).balanceOf(alice) > 0
                #return True
            #except Exception as e:
            #    print("Direct Route Failed for pool", _pool)
            #    print(e)
            #    pass


            try:
                _from_coin.approve(x, _balance, {'from': alice})    

                x.exchange(
                        _pool, 
                        _from, 
                        _to, 
                        _balance, 
                        0, 
                        {'from': alice}
                    )
                assert Contract(_to).balanceOf(alice) > 0
                return True
            except Exception as e:
                print("Exchange Routing Failed for pool", _pool)
                print(e)
                #assert False
                pass



            # Coin is not in exchange
            try:
                _from_coin.approve(_pool, _balance, {'from': alice})
                _from_index = None
                _to_index = None
                _p = Contract(_pool)
                _i = 0
                _coinlist = self.load_pool_coins(_pool)
                for _coinaddr in _coinlist:
                    if _coinaddr == _from: 
                        _from_index = _i
                    if _coinaddr == _to:
                        _to_index = _i
                    _i += 1

                if _from_index is not None and _to_index is not None:
                    _p.exchange(_from_index, _to_index, _balance,0, {'from': alice})
                    return True
                else:
                    self.vprint("Bugg")
                    print(_from_index)
                    print(_to_index)
                    assert False
                    return False
            except Exception as e:
                self.vprint(e)
                pass 
            self.vprint("Could not exchange")
            return False
        return
    def safe_bal(self, pool, addr):
        if pool == self.ether:
            return addr.balance()
        else:
            return Contract(pool).balanceOf(addr)

    def build_liq_arr(self, tri, alice):
        liqarr = []
        for _c in range(3):
            liqarr.append(Contract(tri.coins(_c)).balanceOf(alice))
        return liqarr

    def load_pool_coins(self, pool):
        retdata = []
        i = 0
        while i < 8:
            try:
                pool_contract = Contract(pool)
                _coinaddr = pool_contract.coins(i)
                retdata.append(_coinaddr)
            except Exception as e:
                pass
            i += 1
        return retdata


    # See if a direct path exists
    def get_direct_path(self, addr1, addr2, alice):
        path = self.x.get_best_rate(addr1, addr2, Contract(addr1).balanceOf(addr1))
        return path[0]

    def load_v2_coins(self):
        if self.v2_coins is not None:
            return self.v2_coins

        ret_arr = []
        cr = Contract("registry")
        for _i in range(cr.pool_count()):
            for coin in cr.get_coins(cr.pool_list(_i)):
                if coin not in ret_arr and coin != ZERO_ADDRESS:
                    ret_arr.append(coin)

        self.v2_coins = ret_arr
        return ret_arr

    def is_hub_token(self, coin):
        if coin in self.load_v2_coins():
            return True
        else:
            return False



    # Find the nearest hubs for a token
    def get_crypto_destination(self, _addr):
        cr = Contract('0x4AacF35761d06Aa7142B9326612A42A2b9170E33')
        ret = []
        for _i in range(cr.coin_count()):
            # Search Crypto Registry
            _coin = cr.get_coin(_i)
            if _addr == _coin:
                print("Found", _addr, " in CR")
                return [[(_addr, ZERO_ADDRESS)]]
                ret.append([(_addr, ZERO_ADDRESS)])

            # Search Regular Registry
            _pool = self.registry.find_pool_for_coins(_addr, _coin)

            # XXX Tricrypto passed to the exchange has a weird bug
            if _pool != ZERO_ADDRESS: # and _pool != '0x80466c64868E1ab14a1Ddf27A676C3fcBE638Fe5':
                ret.append([(_coin, _pool)])

            # Search Factory
            _pool = Contract('factory').find_pool_for_coins(_addr, _coin)
            if _pool != ZERO_ADDRESS:
                ret.append([(_coin, _pool)])

        _pool = self.registry.find_pool_for_coins(_addr, self.ether)
        if _pool != ZERO_ADDRESS:
            ret.append([(self.ether, _pool)])

        return ret

    def get_crypto_factory_destination(self, _addr):
            ret = []
            # Check one factory hop
            factory = Contract('factory')
            # Get the factory pools that contain the target coin
            pools = factory.find_pool_for_coins(_addr, ZERO_ADDRESS)
            # Which coins exist in the pool
            pool_coins = self.load_pool_coins(pools)
            # Is there a crypto destination one hop away?
            for p in pool_coins:
                # Skip the coin we're looking for
                if p == _addr:
                    continue
                # What is the crypto destination for other coins in the factory pool?
                _dest = self.get_crypto_destination(p)
                # Is there any destinations?
                if len(_dest):
                   for d in _dest:
                        ret.append([d[0], (p, pools)] )
            return(ret)

    def run_eth_safe_crypto_path(self, addr, crypto_destination, alice):
        # Run Crypto Route
        cr = CurveRouter(addr)
        if crypto_destination == self.ether:
            route = cr.routes[self.weth]
        else:
            route = cr.routes[crypto_destination]

        _addr = addr
        for _p in route:
            self.run_route(_p[0], _addr, _p[1], alice)
            assert Contract(_p[1]).balanceOf(alice) > 0, "stuck"
            _addr = _p[1]

        # If we're dealing with ETH, unwrap WETH
        if crypto_destination == self.ether:
            weth = Contract(self.weth)
            weth_bal = weth.balanceOf(alice)
            weth.withdraw(weth_bal, {'from': alice})
            #path = self.x.get_best_rate(self.ether, crypto_destination, weth_bal)[0]
            #self.x.exchange(path, self.ether, crypto_destination, weth_bal, 0, {'from': alice, 'value': weth_bal})
            return


    def run_crypto_path(self, addr, addr2, alice):
        # Get to the nearest v2 hub
        crypto_destination_array = self.get_crypto_destination(addr2)

        # What if there is no immediate path?  Need to go one more step...
        extra_juice = True

        # No immediate path, maybe there's a factory routing
        if len(crypto_destination_array) == 0:
            # Work backwards from the target
            if addr2 == self.ether:
                crypto_destination_array = self.get_crypto_factory_destination(self.weth)
            else:
                crypto_destination_array = self.get_crypto_factory_destination(addr2)
            extra_juice = True

        if len(crypto_destination_array) == 0:
            self.vprint("No crypto path")
            return

        # Just take the first path, could require more complex selection
        _hop_id = 0
        _last_dest = None
        _last_pool = None 
        self.vprint("Good stop point to check crypto destination array")
        print(crypto_destination_array)
        #assert False
        for _crypto_routes in crypto_destination_array[0]:

            _last_bal = self.safe_bal(_crypto_routes[0], alice)
            if _hop_id == 0:
                self.run_eth_safe_crypto_path(addr, _crypto_routes[0],  alice)
                _last_dest = _crypto_routes[0]
                _last_pool = _crypto_routes[1]
            else:
                self.run_route(_last_pool, _last_dest, _crypto_routes[0], alice)
                _last_dest= _crypto_routes[0]
                _last_pool= _crypto_routes[1]
            
            _bal_diff= self.safe_bal(_crypto_routes[0], alice)- _last_bal 
            _hop_id += 1
        print("EJ")
        if extra_juice:
            print("Juicy")
            #assert(False)
            try:
                self.run_route(_last_pool, _last_dest, addr2, alice, _bal_diff)
            except Exception as e:
                print(e)
                self.vprint("NO GO")
                assert False
            return

        # If ETH, then we're there
        if _crypto_routes[0] == self.ether:
            return

        # No more moves needed, we're here
        if addr2 == _last_dest:
            return

        # No moves, we're here
        try:
            if Contract(addr2).balanceOf(alice) > 0:
                return
        except Exception as e:
            self.vprint(e)
            pass

        # Close enough to run a basic exchange
        final_bal = Contract(addr).balanceOf(alice)
        final_path = self.x.get_best_rate(
            _last_dest, addr2, final_bal
        )

        # Run Route
        self.run_route(final_path[0], _last_dest, addr2, alice)
 

    # Run a direct path 
    def run_like_path(self, addr1, addr2, alice):
        self.vprint("Shortcut")
        self.vprint(addr1)
        self.vprint(addr2)
        final_path = self.x.get_best_rate(addr1, addr2, Contract(addr1).balanceOf(alice))
        self.vprint(f"Best Rate {final_path}")
        if final_path[0] != ZERO_ADDRESS:
            self.vprint("Running")
            self.run_route(final_path[0], addr1, addr2, alice)
        else:
            self.vprint("No Route")

        try:
            self.vprint(f"Final Bal {(Contract(addr2).balanceOf(alice))}")
        except:
            self.vprint("Pass")



    # XXX Delete
    def vprint(self, ex):
        try:
            if self.verbose:
                print(ex)
        except Exception as e:
            print(e)
            print("Failed Printing")

    def pool_index(self, _pool, _coin):
        for i in range(8):
            try:
                if _pool.coins(i) == _coin:
                    return i
            except:
                pass
        print("NO COIN")
        assert False
