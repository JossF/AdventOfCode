import pandas
from collections import Counter

fixed = {}

neighbor_seats = {}


def get_seat_coords(i, j, df, part):
    if neighbor_seats.get((i, j)):
        return neighbor_seats.get((i, j))
    mi = 0
    ma = df.shape
    coords = []
    for x in (-1, 0, 1):
        for y in (-1, 0, 1):
            if x == y == 0:
                continue
            z = 1
            keep_searching = True
            search_count = 1
            while keep_searching:
                if not (mi <= j + y * z <= ma[1] - 1):
                    keep_searching = False
                elif not (mi <= i + x * z <= ma[0] - 1):
                    keep_searching = False
                elif df.loc[i + x * z, j + y * z] != '.' or part == 1:
                    coords.append((i + x * z, j + y * z))
                    keep_searching = False
                elif search_count > 100:
                    raise (ValueError("Never ending search?"))
                search_count += 1
                z += 1
    neighbor_seats[(i, j)] = coords
    return coords


def add_views(df, i, j, sub_df):
    """
    SWITCH TO GIVE LIST OF SEAT VALUES
    """
    sub_df = sub_df.copy()
    x_len, y_len = df.shape
    for a, b in [(x, y) for x in range(-1, 2) for y in range(-1, 2)]:
        if a == b == 0:
            continue
        z = 1
        while 0 <= z * a + i <= x_len and 0 < z * b + j <= y_len:
            if df.loc[z * a + i, z * b + j] == '.':
                z += 1
            else:
                sub_df.loc[i + a, j + b] = df.loc[z * a + i, z * b + j]
    return sub_df


def check_fixed(current_seat, current_coords, other_coords, part=1):
    edit = 1 if part == 2 else 0
    if fixed.get(tuple(current_coords), False):
        return
    surrounding_fixed = [fixed.get(coords) for coords in other_coords if coords in fixed.keys()]
    if current_seat == 'L' and '#' in surrounding_fixed:
        fixed[current_coords] = 'L'
    if current_seat == '#' and len(other_coords) - surrounding_fixed.count('L') - surrounding_fixed.count('.') < (
            4 + edit):
        fixed[current_coords] = '#'


def new_val(df, current_seat, other_coords, part):
    edit = 1 if part == 2 else 0
    vals = [df.loc[x] for x in other_coords]
    if current_seat == "L" and vals.count('#') == 0:
        return '#'
    if current_seat == "#" and vals.count('#') >= (4 + edit):
        return 'L'
    return current_seat


def evolve_seats(df, part):
    df = df.copy()
    new_df = df.copy()
    full_ij = [(i, j) for i in range(len(df)) for j in range(df.shape[1])]
    reduced_ij = [x for x in full_ij if fixed.get(x) is None]
    print(f"reviewing: {len(reduced_ij)}")
    for i, j in reduced_ij:
        if fixed.get((i, j)):
            new_df.loc[i, j] = fixed.get((i, j))
        elif df.loc[i, j] == '.':
            fixed[(i, j)] = '.'
            new_df.loc[i, j] = '.'
        else:
            surrounding_coords = get_seat_coords(i, j, df, part)
            current_seat = new_df.loc[i, j]
            check_fixed(current_seat, (i, j), surrounding_coords, part=part)
            new_seat = new_val(df.copy(), df.loc[i, j], surrounding_coords, part=part)
            new_df.loc[i, j] = new_seat
    return new_df


def find_constant_seat_count(df, part=1):
    df = df.copy()
    x = False
    prev_df = df
    i = 0
    while not x and i < 120:
        i += 1
        new_df = evolve_seats(prev_df, part=part)
        if new_df.equals(prev_df):
            x = True
        else:
            prev_df = new_df
            print(f"iter {i} : fixed {len(fixed)}")
    evolve_seats(new_df, part=part)
    print(f"iter {i} : fixed {len(fixed)}")
    return new_df.stack().value_counts().to_dict().get('#', 0)


def main(part):
    test_set = pandas.read_csv(r"/2020/complete/day_11_test.csv",
                               header=None)
    raw = pandas.read_csv(r"/2020/complete/day_11.csv",
                          header=None)
    raw_c = raw.copy()
    if part == 0:
        return find_constant_seat_count(test_set)
    if part == 1:
        return find_constant_seat_count(raw_c)
    if part == 2:
        # return find_constant_seat_count(test_set, part=2)
        return find_constant_seat_count(raw_c, part=2)


if __name__ == '__main__':
    # print(main(0))
    # del fixed
    # fixed = {}
    # del neighbor_seats
    # neighbor_seats = {}
    # print(main(1))
    # del fixed
    # fixed = {}
    # del neighbor_seats
    # neighbor_seats = {}
    print(main(2))
