import pandas as pd

from advent_of_code.aoc2022.tools import get_file_location

def main():
    fn = get_file_location("day_1.csv")
    data = pd.read_csv(fn).iloc[:,0].to_list()
    values = [0]
    for i in data:
        if i == "--NewElf--":
            values.append(0)
        else:
            values[-1] += int(i)
    print(max(values))
    print(sorted(values)[-3:])
    print(sum(sorted(values)[-3:]))

if __name__ == '__main__':
    main()