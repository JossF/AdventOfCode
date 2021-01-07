import pandas


def data_stream():
    c = pandas.read_csv(r"/2020/complete/day_14.csv")
    return c


def n_to_bits(n):
    output = []
    rem_n = n
    for i in reversed(range(36)):
        output = output + ([1] if 2 ** i <= rem_n else [0])
        rem_n = rem_n - 2 ** i if 2 ** i <= rem_n else rem_n
    return output


def bits_to_n(bit_list):
    return sum([2 ** i for i in range(len(bit_list)) if bit_list[35 - i]])


def bit_masker(bits_in, mask):
    return [int(mask[i]) if mask[i] != "X" else bits_in[i] for i in range(len(mask))]


def full_whammy(n_in, mask):
    return bits_to_n(bit_masker(n_to_bits(n_in), mask))


def load_data(df_inf: pandas.DataFrame):
    mem = {}
    mask = "0101XX01X00X1X1011X1X000000101X10001"
    for r, row in df_inf.iterrows():
        vals = row.tolist()
        if vals[0] == 'mask':
            mask = vals[1]
        else:
            mem[vals[0]] = full_whammy(int(vals[1]), mask)
    return mem


if __name__ == '__main__':
    m1 = "XXXXXXXXXXXXXXXXXXXXXXXXXXXXX1XXXX0X"
    print(full_whammy(11, m1))
    print(full_whammy(101, m1))
    print(full_whammy(0, m1))
    m = load_data(data_stream())
    print(sum(m.values()))
