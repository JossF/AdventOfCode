import pandas as pd

from advent_of_code.aoc2022.tools import get_file_location


def load_str():
    fn = get_file_location("day_8.txt")
    with open(fn) as f:
        return f.read().splitlines(keepends=False)


def scenic_score(f, x, y, xn, yn):
    val = f.loc[x, y]
    score = 1
    l = f.loc[0:x - 1, y].to_list()
    r = f.loc[x + 1:xn, y].to_list()
    u = f.loc[x, 0:y - 1].to_list()
    d = f.loc[x, y + 1:yn].to_list()
    if x in (0, xn - 1) or y in (0, yn - 1):
        return 0
    for lis in [l, u]:
        subscore = 1
        while lis and val > lis[-1]:
            lis.pop(-1)
            subscore += 1 if lis else 0
        score *= subscore
        if subscore == 0:
            return 0
    for lis in [r, d]:
        subscore = 1
        while lis and val > lis[0]:
            lis.pop(0)
            subscore += 1 if lis else 0
        score *= subscore
        if subscore == 0:
            return 0
    return score


def main():
    forest = load_str()
    forest_df = pd.DataFrame([[int(i) for i in f] for f in forest])
    seen = pd.DataFrame([[0 for i in f] for f in forest])
    score = pd.DataFrame([[0 for i in f] for f in forest])
    x_n, y_n = forest_df.shape
    for x in range(x_n):
        for y in range(y_n):
            score.loc[x, y] = scenic_score(forest_df, x, y, x_n, y_n)
            if x in (0, x_n - 1) or y in (0, y_n - 1):
                seen.loc[x, y] = 1
                continue
            h = forest_df.loc[x, y]
            if h > forest_df.loc[0:x - 1, y].max() or \
                    h > forest_df.loc[x + 1:x_n, y].max() or \
                    h > forest_df.loc[x, 0:y - 1].max() or \
                    h > forest_df.loc[x, y + 1:y_n].max():
                seen.loc[x, y] = 1
    print(seen.sum().sum())
    print(score.max().max())
    print("Done")


if __name__ == '__main__':
    main()
