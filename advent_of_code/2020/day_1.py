import pandas


def two_num(sub_list: list, target: float = 2020) -> float:
    for val in sub_list:
        if target - val in sub_list:
            return val


def three_num(sub_list: list, target: float = 2020) -> (float, float):
    for val in sub_list:
        if two_num(sub_list, target - val):
            return val, two_num(sub_list, target - val)


def main(level=1):
    values = pandas.read_csv(r"C:\Users\Joss\PycharmProjects\pythonProject\advent_of_code\2020\day_1.tsv", sep='\t')
    all_values = values.iloc[:, 0].tolist()
    if level == 1:
        return two_num(all_values) * (2020 - two_num(all_values))

    n31, n32 = three_num(all_values, 2020)
    return n31 * n32 * (2020 - n31 - n32)


if __name__ == '__main__':
    print(main(1))
    print(main(2))
