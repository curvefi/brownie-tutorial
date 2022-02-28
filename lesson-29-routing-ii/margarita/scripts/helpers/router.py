# ==================================
# Curve V2 Router
# Calculate routing between a coin and v2 pool endpoints
# ==================================

from brownie import ZERO_ADDRESS, Contract


class CurveRouter:

    # Registries to use for finding routes in order of priority
    registries = [
        Contract("crypto_registry"),
        Contract("registry"),
        Contract("factory"),
    ]

    # How Many Routes
    max_hops = 3

    # Special Routing
    tripool = Contract("3pool")
    tripool_lp = Contract("3pool_lp")
    weth = Contract("weth")
    eth = "0xEeeeeEeeeEeEeeEeEeEeeEEEeeeeEeeeeeeeEEeE"

    # ==================================
    # INITIALIZATION
    # Load some properties on initialization
    # ==================================

    # Set a single source coin on construction
    def __init__(self, source_coin, max_hops=3):
        """
        Set a single source coin and load all Curve v2 routing options

        :param source_coin: Any Curve coin with reasonable proximity to a v2 pool
        :param max_hops: Optionally override number of routing hops (3) before failing
        """

        self.source_coin = source_coin
        self.max_hops = max_hops
        self.open_ends = self.load_v2_coins()
        self.routes = self.find_crypto_paths()

    def load_v2_coins(self):
        """
        Load all coins used in the Curve v2 Crypto Router

        :return: List of all coin addresses
        """

        crypto_registry = self.registries[0]
        ret_arr = []
        for _i in range(crypto_registry.coin_count()):
            ret_arr.append(crypto_registry.get_coin(_i))

        return ret_arr

    def find_crypto_paths(self):
        """
        Main loop to crawl all possible routing to v2 coin endpoints.

        :return: Complete dictionary of all routing.  Key is target endpoint address, each tuple pair contains pool and coin route.
        """

        i = 0
        open_ends = self.open_ends
        found_routes = [self.source_coin]
        route_map = {}

        for i in range(self.max_hops):
            i += 1
            open_ends, found_routes, route_map = self.recurse(
                open_ends, found_routes, route_map
            )
            print(
                f"Hop {i} found {len(found_routes)} endpoints, {len(open_ends)} remaining"
            )

            if i > self.max_hops:
                print("Terminating", i)
                break

        self.open_ends = open_ends
        return route_map

    # ==================================
    # ROUTING FUNCTIONS
    # Find Routes between Curve pools
    # ==================================

    def fetch_route(self, addr1, addr2):
        """
        See if a viable Curve v2 path exists between two addresses

        :param addr1: First coin address
        :param addr2: Second coin address
        :return: True or False
        """

        for registry in self.registries:
            _route = registry.find_pool_for_coins(addr1, addr2)
            if _route != ZERO_ADDRESS:
                return _route

        # Test 3pool
        if self.can_route_3pool(addr1, addr2):
            return self.tripool.address

        # Test ETH/Wrapped ETH
        if self.can_route_weth(addr1, addr2):
            return self.weth.address

        return ZERO_ADDRESS

    def can_route_3pool(self, addr1, addr2):
        """
        Curve 3pool LP token doesn't show up in exchange routing but still a common v2 endpoint.

        :param addr1: First coin address
        :param addr2: Second coin address
        :return: True or False
        """

        if addr1 == self.tripool_lp:
            other_token = addr2
        elif addr2 == self.tripool_lp:
            other_token = addr1
        else:
            return False

        for _i in range(2):
            if self.tripool.coins(_i) == other_token:
                return True

        return False

    def can_route_weth(self, addr1, addr2):
        """
        Check if possible to route between ETH and WETH, despite no Curve pool existing between the two.

        :param addr1: First coin address
        :param addr2: Second coin address
        :return: True or False
        """
        if addr1 == self.weth and addr2 == self.eth:
            return True
        elif addr2 == self.weth and addr1 == self.eth:
            return True
        return False

    # ==================================
    # RECURSION FUNCTIONS
    # Recursive loops to search for routes
    # ==================================

    def recurse(self, missing_endpoints, starting_points, routes):
        """
        recurse() is the main loop to update the routing crawl at each hop

        :param missing_endpoints: All endpoints for which no route exists.  Should shrink each iteration.
        :param starting_points: List of all starting coins to crawl for a route
        :param routes: Complete dictionary of all routing.  Key is target endpoint address, each tuple pair contains pool and coin route.
        :return: Updated list of missing endpoints, next starting v2 tokens, and current routing dictionary
        """

        next_starting_points = []

        # Loop through every v2 token we've found a route to find the next path
        for starting_point in starting_points:

            # Look for missing route between current token and unrouted v2 tokens
            missing_endpoints, _found, local_routes = self.find_routes(
                missing_endpoints, starting_point
            )

            # Update the master routing dictionary
            for _end, _path in local_routes.items():
                if starting_point in routes:
                    routes[_end] = routes[starting_point] + [(_path, _end)]
                else:
                    routes[_end] = [(_path, _end)]

            # Found v2 tokens become the starting points for the next hop
            next_starting_points += _found

        return missing_endpoints, next_starting_points, routes

    def find_routes(self, missing_endpoints, starting_point):
        """
        find_routes() Within each recursive hop, loop through all missing tokens and look for routes

        :param missing_endpoints: All endpoints for which no route exists.  Should shrink each iteration.
        :param starting_point: Single coin to start from
        :return: Updated list of missing endpoints, any found coins, and local routing dictionary
        """

        # Initialize returns
        local_missing_endpoints = []
        local_found_endpoints = []
        local_routes = {}

        # Loop through all missing endpoints
        for missing_v2_token in missing_endpoints:

            # Skip if same
            if starting_point == missing_v2_token:
                continue

            # Does a route exist between the two addresses?
            fetched_route = self.fetch_route(starting_point, missing_v2_token)

            # Update found endpoints and routing info if located
            if fetched_route != ZERO_ADDRESS:
                local_found_endpoints.append(missing_v2_token)
                local_routes[missing_v2_token] = fetched_route

            # Endpoint is still missing
            else:
                local_missing_endpoints.append(missing_v2_token)

        return local_missing_endpoints, local_found_endpoints, local_routes

    # ==================================
    # DISPLAY FUNCTIONS
    # Format the output for humans
    # ==================================

    def nameOf(self, pool):
        """
        Get the name of a Curve pool across several registries

        :param pool: Address of pool to lookup.
        :return: Human readable symbol or name of pool
        """

        # Factory pools don't have a registry name lookup
        try:
            return Contract(pool).symbol()

        except:
            pass

        # Other registries have name functions
        for registry in self.registries:
            _name = registry.get_pool_name(pool)
            if _name != "":
                return _name

        return pool

    def summarize(self):
        """
        summarize() provides human readable summary of routing

        :return: Found routes and missing routes for all Curve v2 pool coins
        """

        for coin, route in self.routes.items():
            print(f"\n ✅ Found Route To {Contract(coin).symbol()} ")
            for path in route:
                print(
                    f"Hop to {Contract(path[1]).symbol()} using {self.nameOf(path[0])} ({path[0]})"
                )

        if self.open_ends != []:
            print(f"\nNo path in {self.max_hops} hops for:")
            for path in self.open_ends:
                print(" ❌", Contract(path).symbol())
