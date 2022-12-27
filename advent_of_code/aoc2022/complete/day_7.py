import re
from copy import deepcopy
import pandas as pd

from advent_of_code.aoc2022.tools import get_file_location


def load_str():
    fn = get_file_location("day_7.txt")
    with open(fn) as f:
        return f.read().splitlines(keepends=False)

sizes = []
def traverse_dict(pointer, direct_dict):
    d = direct_dict
    for c in pointer:
        d = d[c]
    return d


def apply_code(command, pointer, direct_dict):
    if command == "$ cd /":
        return []
    elif command == "$ cd ..":
        pointer.pop(-1)
        return pointer
    elif command == "$ ls":
        return pointer
    elif re.findall(r"dir ([\w]*)", command):
        traverse_dict(pointer, direct_dict)[re.findall(r"dir ([\w]*)", command)[0]] = {}
        return pointer
    elif re.findall(r"([\d]+) ([\w\.]+)", command):
        l = re.findall(r"([\d]*) ([\w\.]+)", command)[0]
        siz, val = int(l[0]), l[1]
        traverse_dict(pointer, direct_dict)[val] = siz
        return pointer
    elif re.findall(r"\$ cd ([\w]*)", command):
        v = re.findall(r"\$ cd ([\w]*)", command)
        return pointer + v
    return pointer


def dir_size(file_dict: dict):
    total = 0
    for k, v in file_dict.items():
        if isinstance(v, int):
            total += v
        if isinstance(v, dict):
            total += dir_size(v)
    return total


def potential_dirs(file_dict: dict):
    total = 0
    size = dir_size(file_dict)
    sizes.append(size)
    total += size if size < 100_000 else 0
    for k, v in file_dict.items():
        if isinstance(v, dict):
            total += potential_dirs(v)
    return total

def main():
    sig = load_str()
    files = {}
    pointer = []
    for s in sig:
        pointer = apply_code(s, pointer, files)
    print(potential_dirs(files))
    print("Done")


if __name__ == '__main__':
    main()
