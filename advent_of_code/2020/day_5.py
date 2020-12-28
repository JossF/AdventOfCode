import pandas


def read_binary(b_in, one):
    """
    >>> read_binary("UDUD", "U")
    10
    >>> read_binary("FFFFFFF", "F")
    127
    """
    total = 0
    for i in range(len(b_in)):
        v = b_in[-i - 1] == one
        total += v * (2 ** (i))
    return total


def read_seat(seat_code):
    return read_binary(seat_code[:7], "B"), read_binary(seat_code[7:], "R")


def main(part):
    raw = pandas.read_csv(r"C:\Users\Joss\PycharmProjects\pythonProject\advent_of_code\2020\day_5.csv", sep='\t',
                          header=None)
    raw_list = raw[0].tolist()
    comp_list = [read_seat(s) for s in raw_list]
    seat_ids = [c[0]*8 + c[1] for c in comp_list]
    if part==1:
        return max(seat_ids)
    expected_seats = [(i,j) for i in range(1, 127) for j in range(8)]
    missing = [x for x in expected_seats if x not in comp_list]


if __name__ == '__main__':
    print(main(1))
    print(main(2))
    print(84*8 + 4)
