from brownie import ZERO_ADDRESS, Contract, accounts, chain
from brownie_tokens import MintableForkToken

from scripts.helpers.router import CurveRouter

registry = Contract("registry")


def main():
    alice = accounts[0]
    amount = 5000
    vals = {}
    chain.snapshot()
    for i in range(registry.coin_count()):
        coin = registry.get_coin(i)
        TokenMinter().mint(alice, amount, coin)
        try:
            _bal = Contract(coin).balanceOf(alice)
        except:
            _bal = None
        vals[i] = _bal
        chain.revert()

    for i, j in vals.items():
        try:
            print(i, Contract(registry.get_coin(i)).symbol(), j)
        except:
            print(i, registry.get_coin(i), j)
    return


class TokenMinter:
    registry = Contract("registry")
    verbose = True
    use_token_tester = True
    use_routing = True
    exchange = None

    ether = "0xEeeeeEeeeEeEeeEeEeEeeEEEeeeeEeeeeeeeEEeE"
    weth = "0xC02aaA39b223FE8D0A0e5C4F27eAD9083C756Cc2"
    tripool = "0xbEbc44782C7dB0a1A60Cb6fe97d0b483032FF1C7"
    tripool_lp = "0x6c3F90f043a72FA612cbac8115EE7e52BDe6E490"
    address_provider = "0x0000000022d53366457f9d5e68ec105046fc4383"
    crypto_registry = "0x4AacF35761d06Aa7142B9326612A42A2b9170E33"

    def __init__(self):
        ap = Contract(self.address_provider)
        self.exchange = Contract(ap.get_address(2))

    # Main Minting Function
    def mint(self, alice, usd_val, target):
        try:
            self.log_verbose(f"--- {Contract(target).symbol()} {target} ---")
        except:
            self.log_verbose(f"--- {target} ---")

        # Try using Token Tester
        if self.mint_using_token_tester(alice, usd_val, target):
            return

        # Try routing from DAI
        if self.use_routing is False:
            return False

        dai = self.mint_dai(alice, usd_val)
        if target == dai:
            return

        TokenMinter().run_overall_path(dai.address, target, alice)

    # Use Brownie Token Tester to mint quickly in most cases
    def mint_using_token_tester(self, alice, usd_val, target):
        if self.use_token_tester is False:
            return False

        try:
            token = MintableForkToken(target)
            token._mint_for_testing(alice, usd_val * 10 ** token.decimals())
            assert token.balanceOf(alice) > 0

            self.log_verbose("Minted Easily")
            return True

        except Exception as e:
            return False

    # Mint DAI and then route tokens to the target
    def mint_dai(self, alice, usd_val):
        dai = MintableForkToken("dai")
        dai._mint_for_testing(alice, usd_val * 10 ** dai.decimals())
        return dai

    # Run a complex route between any two coins
    def run_overall_path(self, addr1, addr2, alice):
        # Is there a direct path between DAI and the target
        direct_path = self.get_direct_path(addr1, addr2, alice)
        if direct_path != ZERO_ADDRESS:
            self.run_direct_path(addr1, addr2, alice)
            return f"Direct {direct_path}"

        # Nope, take the more complicated way through crypto pools
        else:
            return self.run_crypto_path(addr1, addr2, alice)

    # SIMPLE ROUTING
    # Run a direct path between two coins
    def run_direct_path(self, addr1, addr2, alice):
        final_path = self.exchange.get_best_rate(
            addr1, addr2, Contract(addr1).balanceOf(alice)
        )
        self.log_verbose(f"Taking Direct Route {addr1} to {addr2} via {final_path}")

        if final_path[0] != ZERO_ADDRESS:
            self.run_route(final_path[0], addr1, addr2, alice)
        else:
            pass

        try:
            self.log_verbose(f"Final Bal {(Contract(addr2).balanceOf(alice))}")
        except:
            self.log_verbose("Final Bal Could Not Be Determined")

    # COMPLEX ROUTING
    # Run any path that can be sent through the exchange
    def run_route(self, _pool, _from, _to, alice, _balance=None):
        self.log_verbose(f"Running {_pool} {_from} to {_to}")

        # Fail if a nonexistant pool was passed
        if _pool == ZERO_ADDRESS:
            return

        # First up, if the route comes from raw ETH some considerations
        # We need to pass the value instead of an ERC20 transfer
        # And we need to run this before we try to create a ContractContainer

        if _from == self.ether:
            self.exchange.exchange(
                _pool, _from, _to, _balance, 0, {"from": alice, "value": _balance}
            )
            return

        # What if the from coin is DAI, USDC, USDT and the route requires 3pool
        _from = self.wrap_to_3pool(_pool, _from, alice)
        from_contract = Contract(_from)

        # We may have passed a balance, otherwise use the current balance
        if _balance is None:
            _balance = from_contract.balanceOf(alice)

        self.log_verbose(f"Balance {_balance} in {from_contract}")

        # Special Case 2
        # Do we just need to wrap to 3pool?
        if _from in self.load_pool_coins(self.tripool) and _to == self.tripool_lp:
            self.add_curve_pool_liquidity(self.tripool, _from, alice)
            return

        # Main Path
        # First try and route through the exchange
        try:
            from_contract.approve(self.exchange, _balance, {"from": alice})
            self.exchange.exchange(_pool, _from, _to, _balance, 0, {"from": alice})
            assert Contract(_to).balanceOf(alice) > 0
            return
        except Exception as e:
            self.log_verbose(f"Exchange Routing Failed for pool {_pool} {e}")

        # If the coin is not in exchange
        try:
            from_contract.approve(_pool, _balance, {"from": alice})
            i = self.pool_index(_pool, _from)
            j = self.pool_index(_pool, _to)

            if i is not None and j is not None:
                Contract(_pool).exchange(i, j, _balance, 0, {"from": alice})
                return True
            else:
                self.log_verbose(f"Could not exchange within pool {i} {j}")
                return False
        except Exception as e:
            self.log_verbose(f"Failed to exchange {e}")

    # If we are in DAI/USDC/USDT and the pool contains 3pool, wrap accordingly
    def wrap_to_3pool(self, pool, coin, alice):
        tripool_coins = self.load_pool_coins(self.tripool)
        pool_coins = self.load_pool_coins(pool)

        if coin in tripool_coins and self.tripool_lp in pool_coins:
            self.add_curve_pool_liquidity(self.tripool, coin, alice)
            return self.tripool_lp
        else:
            return coin

    # The smart contract calls to add liquidity to 3pool
    def add_curve_pool_liquidity(self, pool_addr, coin_addr, alice):
        pool = Contract(pool_addr)
        coin = Contract(coin_addr)
        balance = coin.balanceOf(alice)
        liq_arr = self.build_liquidity_array(pool, alice)

        coin.approve(pool, balance, {"from": alice})
        pool.add_liquidity(liq_arr, 0, {"from": alice})

    # Retrieve balance without failing
    def safe_bal(self, pool, addr):
        if pool == self.ether:
            return addr.balance()
        else:
            return Contract(pool).balanceOf(addr)

    def build_liquidity_array(self, tri, alice):
        liqarr = []
        for _c in range(3):
            liqarr.append(Contract(tri.coins(_c)).balanceOf(alice))
        return liqarr

    # Retrieve all coins within a single pool
    def load_pool_coins(self, pool):
        retdata = []
        i = 0
        while i < 8:
            try:
                pool_contract = Contract(pool)
                _coin_addr = pool_contract.coins(i)
                retdata.append(_coin_addr)
            except Exception as e:
                pass
            i += 1
        return retdata

    # See if a direct path exists
    def get_direct_path(self, addr1, addr2, alice):
        path = self.exchange.get_best_rate(
            addr1, addr2, Contract(addr1).balanceOf(addr1)
        )
        return path[0]

    # Load all coins that are part of a v2 pool
    def load_v2_coins(self):
        if self.v2_coins is not None:
            return self.v2_coins

        ret_arr = []
        cr = Contract("crypto_registry")
        for _i in range(cr.pool_count()):
            for coin in cr.get_coins(cr.pool_list(_i)):
                if coin not in ret_arr and coin != ZERO_ADDRESS:
                    ret_arr.append(coin)

        self.v2_coins = ret_arr
        return ret_arr

    # If we have a path to any v2 token, we presume we can navigate among v2 pools
    def is_hub_token(self, coin):
        if coin in self.load_v2_coins():
            return True
        else:
            return False

    # CRYPTO REGISTRIES

    # Look through various registries to find the best routing
    def get_crypto_paths(self, addr):
        # First check if there's any crypto hubs
        ret_array = self.get_crypto_destination(addr)

        if len(ret_array) > 0:
            return ret_array

        # No immediate path, maybe there's a factory routing
        # This is slower to run, so only run if necessary
        # Start by working backwards from the target
        if addr == self.ether:
            ret_array = self.get_crypto_factory_destination(self.weth)
        elif registry.get_pool_from_lp_token(addr):
            ret_array = []
            for p in registry.get_coins(registry.get_pool_from_lp_token(addr)):
                if p != ZERO_ADDRESS:
                    _item = self.get_crypto_destination(p)
                    if len(_item):
                        ret_array = ret_array + _item
        else:
            ret_array = self.get_crypto_factory_destination(addr)

        return ret_array

    # Find the nearest hubs for a token
    def get_crypto_destination(self, _addr):
        cr = Contract(self.crypto_registry)
        ret = []

        # Look through every coin in the crypto registry for a possible route
        for _i in range(cr.coin_count()):

            # Search Crypto Registry, best case
            _coin = cr.get_coin(_i)
            if _addr == _coin:
                self.log_verbose(f"Found {_addr} in CR")
                return [[(_addr, ZERO_ADDRESS)]]
                ret.append([(_addr, ZERO_ADDRESS)])

            # Search Regular Registry
            _pool = self.registry.find_pool_for_coins(_addr, _coin)
            if _pool != ZERO_ADDRESS:
                ret.append([(_coin, _pool)])

            # Search Factory
            _pool = Contract("factory").find_pool_for_coins(_addr, _coin)
            if _pool != ZERO_ADDRESS:
                ret.append([(_coin, _pool)])

        _pool = self.registry.find_pool_for_coins(_addr, self.ether)
        if _pool != ZERO_ADDRESS:
            ret.append([(self.ether, _pool)])

        return ret

    # Look for destination within the Curve Factory
    def get_crypto_factory_destination(self, _addr):

        # Get the factory pools that contain the target coin
        factory = Contract("factory")
        pools = factory.find_pool_for_coins(_addr, ZERO_ADDRESS)
        pool_coins = self.load_pool_coins(pools)

        # Is there a crypto destination one hop away?
        ret = []
        for p in pool_coins:
            # Skip the coin we're looking for
            if p == _addr:
                continue

            # What is the crypto destination for other coins in the factory pool?
            _dest = self.get_crypto_destination(p)
            if len(_dest):
                for d in _dest:
                    ret.append([d[0], (p, pools)])

        return ret

    # Run route and unwrap to ETH
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
            weth.withdraw(weth_bal, {"from": alice})
            return

    # Run a Crypto Path
    def run_crypto_path(self, addr, addr2, alice):
        # What's the nearest hub to the endpoint?
        crypto_destination_array = self.get_crypto_paths(addr2)
        if len(crypto_destination_array) == 0:
            self.log_verbose("No crypto path")
            return
        if self.verbose:
            print(crypto_destination_array)

        # For now we just use the first route
        # We may require more complex selection as we expand this script
        _hop_id = 0
        _last_dest = addr
        _last_pool = None

        # Let's run through the full crypto path
        for _crypto_routes in crypto_destination_array[0]:
            _last_bal = self.safe_bal(_crypto_routes[0], alice)

            # Step one, run the complex crypto path to destination
            if _hop_id == 0:
                self.run_eth_safe_crypto_path(addr, _crypto_routes[0], alice)
                _last_dest = _crypto_routes[0]
                _last_pool = _crypto_routes[1]

            # For all subsequent hops, run a direct route
            else:
                self.run_route(_last_pool, _last_dest, _crypto_routes[0], alice)
                _last_dest = _crypto_routes[0]
                _last_pool = _crypto_routes[1]

            # Logic to calculate balance (safe for raw ETH)
            _bal_diff = self.safe_bal(_crypto_routes[0], alice) - _last_bal
            _hop_id += 1

        # Can we wrap our way to success?
        _lp_pool = registry.get_pool_from_lp_token(addr2)
        if _lp_pool != ZERO_ADDRESS and _last_dest in registry.get_coins(_lp_pool):
            self.add_curve_pool_liquidity(_lp_pool, _last_dest, alice)
            return

        # Last move
        try:
            self.run_route(_last_pool, _last_dest, addr2, alice, _bal_diff)
        except Exception as e:
            self.log_verbose(f"NO GO {e}")
            assert False

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
            self.log_verbose(e)
            pass

        # Close enough to run a basic exchange
        final_bal = Contract(addr).balanceOf(alice)
        final_path = self.exchange.get_best_rate(_last_dest, addr2, final_bal)

        # Run Route
        self.run_route(final_path[0], _last_dest, addr2, alice)

    # Find the coin index for a coin in a specific pool
    def pool_index(self, _pool, _coin):
        for i in range(8):
            try:
                if _pool.coins(i) == _coin:
                    return i
            except:
                pass
        self.log_verbose(f"No coin found for {_pool} {_coin}")
        return None

    # Debugging Output
    def log_verbose(self, ex):
        try:
            if self.verbose:
                print(ex)
        except Exception as e:
            print(f"Failed Printing {e}")
