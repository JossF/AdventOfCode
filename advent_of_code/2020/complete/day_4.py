import pandas


def main():
    raw = pandas.read_csv(r"/2020/complete/day_4.csv", sep='\t',
                          header=None)
    list_vals = raw[0].values
    first_3 = [[j[:3] for j in i.split(',')] for i in list_vals]
    last_part = [[j[4:] for j in i.split(',')] for i in list_vals]
    required = ['byr', 'iyr', 'eyr', 'hgt', 'hcl', 'ecl', 'pid']

    def validate_full(l1, l2):
        results = [validator(i, j) for i, j in zip(l1, l2)]
        print("-----------")
        return len([x for x in l1 if x in required]) == 7 and len([r for r in results if r]) == 7

    def validator(field, val):
        val_dict = {
            'byr': lambda x: 1920 <= int(x) <= 2002,
            'iyr': lambda x: 2010 <= int(x) <= 2020,
            'eyr': lambda x: 2020 <= int(x) <= 2030,
            'hgt': lambda x: len(x) > 2 and ((150 <= int(x[:-2]) <= 193 and x[-2:] == 'cm') or (59 <= int(x[:-2]) <= 76 and x[-2:] == 'in')),
            'hcl': lambda x: x[0] == '#' and len(
                [i for i in x if i in [str(i) for i in range(10)] + ['a', 'b', 'c', 'd', 'e', 'f']]) == 6,
            'ecl': lambda x: x in ['amb', 'blu', 'brn', 'gry', 'grn', 'hzl', 'oth'],
            'pid': lambda x: len(x) == 9 and len([i for i in x if i in [str(i) for i in range(10)]]) == 9,
            'cid': lambda x: False,
        }
        print(field, val, val_dict[field](val))
        return val_dict[field](val)

    xyx = [validate_full(i, j) for i, j in zip(first_3, last_part)]
    return len([z for z in xyx if z])

if __name__ == '__main__':
    print(main())
