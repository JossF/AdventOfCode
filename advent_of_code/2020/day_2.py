import pandas


def password_check_1(r):
    return r['lower'] <= len([i for i in r['password'] if i == r['letter']]) <= r['upper']


def password_check_2(r):
    return (r['password'][r['lower'] - 1] == r['letter']) * 1 + (r['password'][r['upper'] - 1] == r['letter']) * 1 == 1


def main():
    raw = pandas.read_csv(r"C:\Users\Joss\PycharmProjects\pythonProject\advent_of_code\2020\day_2.csv")
    raw['acceptable_1'] = raw.apply(password_check_1, axis=1)
    raw['acceptable_2'] = raw.apply(password_check_2, axis=1)
    return len(raw[raw['acceptable_1']]), len(raw[raw['acceptable_2']])


if __name__ == '__main__':
    print(main())
