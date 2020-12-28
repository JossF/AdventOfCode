import pandas


def data_stream():
    c = pandas.read_csv(r"C:\Users\Joss\PycharmProjects\pythonProject\advent_of_code\2020\day_14.csv")
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
    def coder(in_bit, mask_bit):
        if mask_bit == '0':
            return in_bit
        if mask_bit == '1':
            return 1
        return "X"

    def switcher(bits_in):
        if "X" not in bits_in:
            return [bits_in]
        x_loc = bits_in.index("X")
        bit_0 = [bits_in[i] if i != x_loc else 0 for i in range(len(bits_in))]
        bit_1 = [bits_in[i] if i != x_loc else 1 for i in range(len(bits_in))]
        return switcher(bit_0) + switcher(bit_1)

    masked_bits = [coder(bits_in[i], mask[i]) for i in range(len(mask))]
    return switcher(masked_bits)


def full_whammy(n_in, mask):
    return [bits_to_n(i) for i in bit_masker(n_to_bits(n_in), mask)]


def load_data(df_inf: pandas.DataFrame):
    mem = {}
    mask = "0101XX01X00X1X1011X1X000000101X10001"
    for r, row in df_inf.iterrows():
        vals = row.tolist()
        if vals[0] == 'mask':
            mask = vals[1]
        else:
            for mem_loc in full_whammy(int(vals[0]), mask):
                mem[mem_loc] = vals[1]
    return mem


if __name__ == '__main__':
    m1 = "000000000000000000000000000000X1001X"
    print(full_whammy(42, m1))
    m2 = '00000000000000000000000000000000X0XX'
    print(full_whammy(26, m2))
    mem_loc = load_data(data_stream())
    print(sum([int(i) for i in mem_loc.values()]))
