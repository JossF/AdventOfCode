import pandas


def main(part):
    raw = pandas.read_csv(r"/2020/complete/day_9.tsv",
                          header=None)
    possibilities = dict()
    broken_number = None
    for i in range(25, len(raw)):
        possibilities[i] = set(
            [raw.loc[i - x, 0] + raw.loc[i - y, 0] for x in range(1, 26) for y in range(1, 26) if x > y])

    for l in range(25, len(raw)):
        if raw.loc[l, 0] not in possibilities[l]:
            broken_number = raw.loc[l, 0]
            break

    for i in range(l):
        total = raw.loc[l - i, 0]
        j = 1
        while total < broken_number:
            total += raw.loc[l - i - j, 0]
            j += 1
            if total == broken_number:
                return broken_number, raw.loc[l - i - j + 1: l - i, 0].max() + raw.loc[l - i - j + 1: l - i, 0].min()


if __name__ == '__main__':
    print(main(1))
