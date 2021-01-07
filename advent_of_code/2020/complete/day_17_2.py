import pandas

test_state = pandas.read_csv(r"/2020/complete/day_17_test.csv",
                             header=None)
run_state = pandas.read_csv(r"/2020/complete/day_17.csv", header=None)


def t_add(t1, t2):
    """
    >>> t_add((1,2,3), (5,4,3))
    (6, 6, 6)
    """
    return tuple(map(sum, zip(t1, t2)))


def neighbours(coords):
    unit_neighs = [(x1, y1, z1, w1) for x1 in [-1, 0, 1] for y1 in [-1, 0, 1] for z1 in [-1, 0, 1] for w1 in [-1, 0, 1]]
    return [t_add(unit_t, coords) for unit_t in unit_neighs if unit_t != (0, 0, 0, 0)]


def load_t0(df, cache):
    cache[0] = {}
    for ind, row in df.iterrows():
        for x in range(len(row)):
            cache[0][(x, ind, 0, 0)] = 1 if row.loc[x] == "#" else 0


def determine_cube(val, neighbouring_values):
    if val == 1:
        if sum(neighbouring_values) in (2, 3):
            return 1
        return 0
    if sum(neighbouring_values) == 3:
        return 1
    return 0


def evolve_cache(cache):
    last_t = max(cache.keys())
    next_t = last_t + 1
    cache[next_t] = {}
    last_keys = cache[last_t].keys()
    x_r = range(min([t[0] for t in last_keys]) - 1, max([t[0] for t in last_keys]) + 2)
    y_r = range(min([t[1] for t in last_keys]) - 1, max([t[1] for t in last_keys]) + 2)
    z_r = range(min([t[2] for t in last_keys]) - 1, max([t[2] for t in last_keys]) + 2)
    w_r = range(min([t[3] for t in last_keys]) - 1, max([t[3] for t in last_keys]) + 2)
    coords = [(xx, yy, zz, ww) for xx in x_r for yy in y_r for zz in z_r for ww in w_r]
    for xyzw in coords:
        cube = cache[last_t].get(xyzw, 0)
        neighs = [cache[last_t].get(n, 0) for n in neighbours(xyzw)]
        cache[next_t][xyzw] = determine_cube(cube, neighs)
    print_time_set(cache[next_t])


def print_time_set(cached_coords):
    all_keys = cached_coords.keys()
    for z in range(min([t[2] for t in all_keys]), max([t[2] for t in all_keys]) + 1):
        for w in range(min([t[3] for t in all_keys]), max([t[3] for t in all_keys]) + 1):
            yr = range(min([t[1] for t in all_keys]), max([t[1] for t in all_keys]) + 1)
            print(pandas.DataFrame([[cached_coords[k] for k in all_keys if k[1:] == (y, z, w)] for y in yr]).replace(
                {0: ".", 1: "#"}))
            print("\n")


if __name__ == '__main__':
    # cache_test = {}
    # load_t0(test_state, cache_test)
    # evolve_cache(cache_test)
    # evolve_cache(cache_test)
    # evolve_cache(cache_test)
    # evolve_cache(cache_test)
    # evolve_cache(cache_test)
    # evolve_cache(cache_test)
    # print(sum([v for v in cache_test[6].values()]))
    cache_main = {}
    load_t0(run_state, cache_main)
    evolve_cache(cache_main)
    evolve_cache(cache_main)
    evolve_cache(cache_main)
    evolve_cache(cache_main)
    evolve_cache(cache_main)
    evolve_cache(cache_main)
    print(sum([v for v in cache_main[6].values()]))
