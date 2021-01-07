import pandas

cached_colors = {}

cached_count = dict()


def contains_bag(col, df, my_color='shiny gold'):
    if cached_colors.get(col, None) is not None:
        return cached_colors.get(col)
    contains = df.loc[col, 'others_l']
    if my_color in contains:
        cached_colors[col] = True
    else:
        for sub_col in contains:
            if contains_bag(sub_col, df):
                cached_colors[col] = True
                break
        cached_colors[col] = cached_colors.get(col, False)
    return cached_colors[col]


def internal_count(col, df):
    if cached_count.get(col, None) is not None:
        return cached_count.get(col)
    count_dict = df.loc[col, 'others_d']
    total = 1
    if count_dict not in ({}, ''):
        for sub_col, sub_count in count_dict.items():
            subtotal = int(sub_count)*internal_count(sub_col, df)
            total += subtotal
    cached_count[col] = total
    return total


def to_d(x):
    x1 = [i.split(";")[0] for i in x if len(i) > 0]
    x2 = [i.split(";")[1] for i in x if len(i) > 0]
    return dict(zip(x1, x2))


def to_l(x):
    x1 = [i.split(";")[0] for i in x if len(i) > 0]
    return x1


def main(part):
    raw = pandas.read_csv(r"/2020/complete/day_7.tsv", sep='\t',
                          header=None)
    data = raw.copy()
    data['split'] = raw[0].apply(lambda x: x.split(":"))
    data['start'] = data['split'].apply(lambda x: x[0])
    data['others_d'] = data['split'].apply(lambda x: to_d(x[1:]))
    data['others_l'] = data['split'].apply(lambda x: to_l(x[1:]))

    if part == 1:
        return sum(
            [1 for c in data['start'].tolist() if contains_bag(c, data.set_index('start'), my_color="shiny gold")])
    final_count = internal_count('shiny gold', data.set_index('start'))
    return final_count - 1


if __name__ == '__main__':
    print(main(1))
    print(main(2))
