import pandas


def get_h_position(v, shift, width=31):
    return (v * shift) % width


def get_coords(d, r, max_d=323):
    coords = []
    i = 1
    while i * d < max_d:
        coords.append((d * i, get_h_position(i, r)))
        i += 1
    return coords


def main(d, r):
    raw = pandas.read_csv(r"C:\Users\Joss\PycharmProjects\pythonProject\advent_of_code\2020\day_3.csv",
                          header=None)

    trees = 0
    raw = raw.dropna(axis=1)
    for pos in get_coords(d, r):
        if raw.iat[pos[0], pos[1]] == '#':
            trees += 1
    return trees


if __name__ == '__main__':
    print(main(1, 1))
    print(main(1, 3))
    print(main(1, 5))
    print(main(1, 7))
    print(main(2, 1))
