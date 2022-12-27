import pandas as pd

from advent_of_code.aoc2022.tools import get_file_location


def letter_to_point(input: str) -> int:
    add = 1 if input.islower() else 27
    return ord(input.lower()) - ord('a') + add


def find_common(input: str) -> int:
    half_l = int(len(input) / 2)
    letter = set(input[:half_l]).intersection(set(input[half_l:]))
    return letter_to_point(sorted(letter)[0])


def main():
    fn = get_file_location("day_3.csv")
    data = pd.read_csv(fn).iloc[:, 0].to_list()
    vals = [find_common(s) for s in data]
    print(sum(vals))
    print("Done")


def main2():
    fn = get_file_location("day_3.csv")
    data = pd.read_csv(fn).iloc[:, 0].to_list()
    final = 0
    while len(data) > 0:
        total_str = set(data.pop(0)).intersection(set(data.pop(0)).intersection(set(data.pop(0))))
        final += letter_to_point(list(total_str)[0])
    print(final)
    print("Done")


if __name__ == '__main__':
    main2()
