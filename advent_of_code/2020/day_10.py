import pandas
import operator
from collections import Counter

cache = {
    (0,): 1,
    (0, 1): 1,
    (0, 2): 1,
    (0, 1, 2): 2,
    (0, 1, 2, 3): 4,
    (0, 1, 2, 3, 4): 7,
}


def comb(l_in):
    return cache[l_in]


def split_into_sub(l_in):
    s_list = sorted(l_in)
    split_list = []
    temp_list = []
    for i in range(1, len(l_in)):
        temp_list.append(s_list[i - 1])
        if s_list[i] - s_list[i - 1] == 3:
            split_list.append(temp_list)
            temp_list = []
    return split_list


def verify_set(l_in, mi, ma):
    l_ends = sorted(set(l_in + [mi, ma]))
    x = pandas.Series(l_ends) - pandas.Series(l_ends).shift(1)
    return set(x.dropna().unique()).issubset({1, 2, 3})


def test_adapter_set(x):
    """
    >>> print(test_adapter_set([1, 4, 5, 6, 7, 10, 11, 12, 15, 16, 19]))
    8
    """
    ma = max(x) + 3
    mi = 0
    fixed_end_lists = split_into_sub([mi, ma] + x)
    as_tuples = [tuple([i - min(sub_l) for i in sub_l]) for sub_l in fixed_end_lists]
    combis = [comb(i) for i in as_tuples]
    l = [i for i in combis if i > 1]
    total = 1
    for x in l:
        total = total * x
    return total


def main(part):
    raw = pandas.read_csv(r"C:\Users\Joss\PycharmProjects\pythonProject\advent_of_code\2020\day_10.csv",
                          header=None)
    if part == 1:
        return verify_set(raw[0].tolist(), 0, 163)
    print(test_adapter_set([1, 4, 5, 6, 7, 10, 11, 12, 15, 16, 19]))
    return test_adapter_set(raw[0].tolist())


if __name__ == '__main__':
    print(main(2))
