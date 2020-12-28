import pandas


def get_other_tix():
    return pandas.read_csv(r'C:\Users\Joss\PycharmProjects\pythonProject\advent_of_code\2020\day_16.csv', header=None)


pm = pandas.DataFrame(index=range(20), columns=range(20), data=1)


def run_rules(series_in):
    rule_list = [lambda x: 50 <= x <= 692 or 705 <= x <= 969,
                 lambda x: 35 <= x <= 540 or 556 <= x <= 965,
                 lambda x: 27 <= x <= 776 or 790 <= x <= 974,
                 lambda x: 48 <= x <= 903 or 911 <= x <= 955,
                 lambda x: 33 <= x <= 814 or 836 <= x <= 953,
                 lambda x: 34 <= x <= 403 or 421 <= x <= 966,
                 lambda x: 37 <= x <= 489 or 510 <= x <= 963,
                 lambda x: 46 <= x <= 128 or 150 <= x <= 960,
                 lambda x: 45 <= x <= 75 or 97 <= x <= 959,
                 lambda x: 28 <= x <= 535 or 541 <= x <= 952,
                 lambda x: 38 <= x <= 340 or 349 <= x <= 966,
                 lambda x: 42 <= x <= 308 or 316 <= x <= 969,
                 lambda x: 49 <= x <= 324 or 340 <= x <= 970,
                 lambda x: 31 <= x <= 627 or 648 <= x <= 952,
                 lambda x: 38 <= x <= 878 or 893 <= x <= 955,
                 lambda x: 39 <= x <= 54 or 71 <= x <= 967,
                 lambda x: 36 <= x <= 597 or 615 <= x <= 960,
                 lambda x: 41 <= x <= 438 or 453 <= x <= 959,
                 lambda x: 42 <= x <= 370 or 389 <= x <= 971,
                 lambda x: 36 <= x <= 114 or 127 <= x <= 965,
                 ]
    new_pm = pm.copy()
    for i in range(20):
        new_pm[i] = new_pm[i].multiply([rule_list[i](series_in[k]) for k in range(20)])
    return new_pm


def totally_invalid_numbers():
    totally_invalid = 0
    i = 0
    for x in get_other_tix().values:
        df_out = run_rules(x)
        totally_invalid += sum([x[k] for k in df_out[df_out.max(axis=1) == 0].index])
        i += 1
    return totally_invalid


def determine_rules():
    i = 1
    updating_pm = pandas.DataFrame(index=range(20), columns=range(20), data=1)
    for x in get_other_tix().values:
        i += 1
        print(i)
        df_out = run_rules(x)
        if len(df_out[df_out.max(axis=1) == 0]) > 0:
            continue
        else:
            updating_pm = updating_pm * df_out
        if updating_pm.sum().sum() == 20:
            return updating_pm
        updating_pm = sudokoize(updating_pm, [])
    return updating_pm


def sudokoize(df, ignore):
    ignorer_again = list(ignore)
    for ind, val in df.sum().items():
        if val > 1:
            continue
        if ind in ignore:
            continue
        else:
            r = df[ind].idxmax()
            df.loc[r, :] = 0
            df.loc[r, ind] = 1
            ignorer_again.append(ind)
    if ignore == ignorer_again:
        return df
    return sudokoize(df=df, ignore=ignorer_again)


if __name__ == '__main__':
    print(totally_invalid_numbers())
    inds = determine_rules()
    vals = [107,157,197,181,71,113,179,109,97,163,73,53,101,193,173,151,167,191,127,103]
    ix = inds.loc[:, :5].max(axis=1)
    print((ix.multiply(vals).replace(0, 1)).product())
