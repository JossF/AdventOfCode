import pandas

switch_index = []
passed_loop = []


def test_loop(start_index, data):
    ran = []
    index = start_index
    repeat = False
    while not repeat:
        ran.append(index)
        if index >= len(data):
            return True
        instruction = data.iloc[index, :]
        if instruction[0] == 'nop':
            index += 1
        elif instruction[0] == 'jmp':
            index += instruction[1]
        else:
            index += 1
        repeat = index in ran
    return False


def run_program(start_index, data, check_for_switches):
    ran = []
    acc_total = 0
    first_total = 0
    index = start_index
    repeat = False
    while not repeat:
        ran.append(index)
        if index >= len(data):
            return acc_total, True, first_total
        instruction = data.iloc[index, :]
        if instruction[0] == 'nop':
            index += 1
            if check_for_switches and test_loop(index + instruction[1], data):
                switch_index.append(index)
                first_total += acc_total
        elif instruction[0] == 'jmp':
            index += instruction[1]
            if check_for_switches and test_loop(index + 1, data):
                switch_index.append(index)
                first_total += acc_total

        else:
            index += 1
            acc_total += instruction[1]
        repeat = index in ran
    return acc_total, False, first_total


def main(part):
    raw = pandas.read_csv(r"C:\Users\Joss\PycharmProjects\pythonProject\advent_of_code\2020\day_8.csv",
                          header=None)
    total1, found_end, total2 = run_program(0, raw, True)
    if part == 1:
        return total1
    switched = raw.copy()
    x = switched.loc[switch_index[0], 0]
    switched.loc[switch_index[0], 0] = 'nop' if x == 'jmp' else 'jmp'
    return run_program(0, switched, False)[0]


if __name__ == '__main__':
    print(main(1))
    print(main(2))
