import pandas


def tallier(x):
    return len([j for j in x['unique'] if x[0].count(j) == x['length']])


def main(part):
    raw = pandas.read_csv(r"/2020/complete/day_6.tsv", sep='\t',
                          header=None)
    data = raw.copy()
    data['length'] = data[0].apply(lambda x: len(x.split(',')))
    data['unique'] = data[0].apply(lambda x: sorted([i for i in set(x) if i != ',']))
    data['unique_yes'] = data['unique'].apply(lambda x: len(x))
    data['all_yes'] = data.apply(tallier, axis=1)
    if part == 1:
        return data['unique_yes'].sum()
    return data['all_yes'].sum()


if __name__ == '__main__':
    print(main(1))
    print(main(2))
