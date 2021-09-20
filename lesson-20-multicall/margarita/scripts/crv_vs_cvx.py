from brownie import *

from scripts.compare_crv_to_cvx import compare_crv_to_cvx
from scripts.helpers.utils import *


# Loop through all pools and compare Curve vs Convex rewards
def main():
    registry = load_registry()
    final = {}

    for pool_id in range(registry.pool_count()):
        crv_val, cvx_val = compare_crv_to_cvx(pool_id, False)

        if crv_val > 0 or cvx_val > 0:
            final[pool_id] = [crv_val, cvx_val]

    for i, j in final.items():
        print(i, j)
