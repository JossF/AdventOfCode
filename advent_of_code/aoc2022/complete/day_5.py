import re
from copy import deepcopy
import pandas as pd

from advent_of_code.aoc2022.tools import get_file_location


def load_start():
    fn = get_file_location("day_5_blocks.txt")
    txt = None
    with open(fn) as f:
        txt = f.read()
    new_txt = None
    while txt != new_txt:
        new_txt = txt
        txt = txt.replace("    [", "[0] [")
    split = new_txt.split("\n")
    values = [re.findall(r"\[(\w)\]", s) for s in split if "[" in s]
    stacks = {i + 1: [v[i] for v in reversed(values) if v[i] != '0'] for i in range(len(values[0]))}
    return stacks


def apply_move(quantity, from_n, to_n, stacks):
    new_stacks = deepcopy(stacks)
    for i in range(int(quantity)):
        val = new_stacks[int(from_n)].pop(-1)
        new_stacks[int(to_n)].append(val)
    return new_stacks


def apply_move2(quantity, from_n, to_n, stacks):
    new_stacks = deepcopy(stacks)
    new_list = []
    for i in range(int(quantity)):
        val = new_stacks[int(from_n)].pop(-1)
        new_list.append(val)
    new_stacks[int(to_n)].extend(reversed(new_list))
    return new_stacks


def main():
    stacks = load_start()
    fn = get_file_location("day_5.csv")
    data = pd.read_csv(fn)['orders'].values.tolist()
    tuples = [re.findall(r"move ([\d]*) from ([\d]) to ([\d])", x) for x in data]
    new_stacks = deepcopy(stacks)
    for t in tuples:
        print([(s, len(new_stacks[s])) for s in new_stacks])
        new_stacks = apply_move(t[0][0], t[0][1], t[0][2], new_stacks)
    print([new_stacks[v][-1] for v in new_stacks])
    new_stacks2 = deepcopy(stacks)
    for t in tuples:
        print([(s, len(new_stacks2[s])) for s in new_stacks2])
        new_stacks2 = apply_move2(t[0][0], t[0][1], t[0][2], new_stacks2)
    print([new_stacks2[v][-1] for v in new_stacks2])
    print("Done")


def main2():
    fn = get_file_location("day_3.csv")
    data = pd.read_csv(fn).iloc[:, 0].to_list()
    print("Done")


if __name__ == '__main__':
    main()
