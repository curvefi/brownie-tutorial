def get_iter_est(pool, i, j, target):
    _dy = pool.get_dy(i, j, target)
    min_val = None
    max_val = None

    if _dy > target:
        max_val = target
        iter_val = 0.1
    else:
        min_val = target
        iter_val = 10
    loops = 0

    _val = target

    while dx_solved(pool, i, j, _val, target, min_val, max_val) is False:
        loops += 1

        min_val, max_val, _val = run_loop(
            min_val, max_val, iter_val, _val, target, pool, i, j
        )
        # print(loops, _val, min_val, max_val)

        if loops > 100:
            assert False

    return _val


def run_loop(min_val, max_val, iter_val, _val, target, pool, i, j):
    # Set bounds first
    if min_val is None or max_val is None:
        _val *= iter_val
    else:
        # Large integer math
        adder = int((max_val - min_val) / 2)
        _val = int(min_val + adder)

    # Higher or lower?
    _out = pool.get_dy(i, j, int(_val))
    if _out < target:
        min_val = int(_val)
    elif _out > target:
        max_val = int(_val)

    # Return valus
    return min_val, max_val, _val


def dx_solved(pool, i, j, dx, target_dy, min_val, max_val):
    if min_val is None or max_val is None:
        return False

    # Did we nail it?
    _dy = pool.get_dy(i, j, dx)
    if _dy == target_dy:
        return True

    # Did we find the closest possible without going over?
    _dy_1 = pool.get_dy(i, j, dx + 1)
    if _dy < target_dy and _dy_1 > target_dy:
        return True

    return False
