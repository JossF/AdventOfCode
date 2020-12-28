def calculate_next_bus(time, *bus_ids):
    min_wait = 100000000000
    id = 0
    for bus in bus_ids:
        multi, rem = divmod(time, bus)
        wait = bus - rem
        print(f"{bus} : {wait}")
        if wait < min_wait:
            id = bus
            min_wait = wait
    return id * min_wait


def timing_requirements(str_in):
    l = str_in.split(",")
    out_d = {}
    for id in l:
        if id == "x":
            continue
        out_d[int(id)] = l.index(id) #- len(out_d)
    return out_d


def jump_value_calculator(req_dict):
    def checker(int_in):
        output = 1
        continue_calc = False
        for id, ind in req_dict.items():
            if divmod(int_in + ind, id)[1] == 0:
                output *= id
            else:
                continue_calc = True
        if continue_calc:
            return output
        return 0

    return checker


def first_timing(req_dict):
    iterations = 0
    current_x = max(req_dict.keys())
    completed = False
    scale_calcer = jump_value_calculator(req_dict)
    scalar = 1
    while iterations < 10000 and not completed:
        scalar_new = scale_calcer(current_x)
        if scalar_new == 0:
            return current_x
        else:
            current_x += scalar_new
            if scalar != scalar_new:
                print(f"Next bus condition met: {current_x} - {scalar_new/scalar}")
            scalar = scalar_new
        iterations += 1
    print("Run over 10000 iterations")
    return scalar


if __name__ == '__main__':
    y = calculate_next_bus(939, 7, 13, 59, 31, 19)
    print(y)
    y = calculate_next_bus(1002578, 19, 37, 751, 29, 13, 23, 431, 41, 17)
    print(y)
    for in_str in ["67,7,59,61", "67,x,7,59,61", "67,7,x,59,61", "1789,37,47,1889"]:
        req = timing_requirements(in_str)
        print(first_timing(req))
    in_str = "19,x,x,x,x,x,x,x,x,x,x,x,x,37,x,x,x,x,x,751,x,29,x,x,x,x,x,x,x,x,x,x,13,x,x,x,x,x,x,x,x,x,23,x,x,x,x,x,x,x,431,x,x,x,x,x,x,x,x,x,41,x,x,x,x,x,x,17"
    req = timing_requirements(in_str)
    print(first_timing(req))