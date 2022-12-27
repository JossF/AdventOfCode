import re
from copy import deepcopy
import pandas as pd

from advent_of_code.aoc2022.tools import get_file_location


def load_str():
    fn = get_file_location("day_6.txt")
    with open(fn) as f:
        return f.read()


def main():
    sig = load_str()
    # sig = 'mjqjpqmgbljsphdztnvjfqwrcgsmlb'
    for i in range(len(sig) - 14):
        if len(set(sig[i: i + 14])) == 14:
            print(i + 14)
            break
    print("Done")


if __name__ == '__main__':
    main()
