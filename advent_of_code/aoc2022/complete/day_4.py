import pandas as pd

from advent_of_code.aoc2022.tools import get_file_location


def to_tuple(input: str) -> tuple:
    l = input.split("-")
    return (int(l[0]), int(l[1]))


def tuple_contains(tuple1, tuple2) -> bool:
    if tuple1[0] <= tuple2[0] and tuple1[1] >= tuple2[1]:
        return True
    return False


def overlap(tuple1, tuple2) -> bool:
    if tuple1[0] <= tuple2[0] <= tuple1[1] or tuple1[0] <= tuple2[1] <= tuple1[1]:
        return True
    return False


def main():
    fn = get_file_location("day_4.csv")
    data = pd.read_csv(fn)
    data['e1'] = data['one'].apply(to_tuple)
    data['e2'] = data['two'].apply(to_tuple)
    data['o'] = data.apply(lambda r: overlap(r['e1'], r['e2']), axis=1)
    total = 0
    for t1, t2 in zip(data['e1'].to_list(), data['e2'].to_list()):
        if tuple_contains(t1, t2) or tuple_contains(t2, t1):
            total += 1
    print(total)
    total2 = 0
    for t1, t2 in zip(data['e1'].to_list(), data['e2'].to_list()):
        if overlap(t1, t2) or tuple_contains(t1, t2) or tuple_contains(t2, t1):
            total2 += 1
    print(total)
    print("Done")


def main2():
    fn = get_file_location("day_3.csv")
    data = pd.read_csv(fn).iloc[:, 0].to_list()
    print("Done")


if __name__ == '__main__':
    main()
