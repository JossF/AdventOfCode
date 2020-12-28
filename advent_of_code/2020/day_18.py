import re
import pandas


def resolve(str_in):
    """
    >>> resolve("2 * 3 + (4 * 5)")
    '2 * 3 + 20'
    >>> resolve("2 * 3 + 20")
    '6 + 20'
    >>> resolve("6 + 20")
    '26'
    """
    m_str = r"([0-9]+)[ ]*\*[ ]+([0-9]+)"
    p_str = r"([0-9]+)[ ]*\+[ ]+([0-9]+)"
    patterns = {
        "m": re.compile(m_str),
        "p": re.compile(p_str),
        "bm": re.compile(r"\(" + m_str + r"\)"),
        "bp": re.compile(r"\(" + p_str + r"\)"),
    }
    subs = {
        "m": lambda x: f"{int(x.group(1)) * int(x.group(2))}",
        "p": lambda x: f"{int(x.group(1)) + int(x.group(2))}",
        "bm": lambda x: f"{int(x.group(1)) * int(x.group(2))}",
        "bp": lambda x: f"{int(x.group(1)) + int(x.group(2))}"
    }
    indices = {(name[0] != "b", op.search(str_in).start()): name for name, op in patterns.items() if op.search(str_in)}
    return patterns[indices[sorted(indices.keys())[0]]].sub(subs[indices[sorted(indices.keys())[0]]], str_in, 1)


def resolve_add(str_in):
    """
    >>> resolve_add("2 * 3 + (4 * 5)")
    '2 * 3 + 20'
    >>> resolve_add("2 * 3 + 20")
    '2 * 23'
    >>> resolve_add("2 * 23")
    '46'
    """
    m_str = r"([0-9]+)[ ]*\*[ ]+([0-9]+)"
    p_str = r"([0-9]+)[ ]*\+[ ]+([0-9]+)"
    patterns = {
        "m": re.compile(m_str),
        "p": re.compile(p_str),
        "bm": re.compile(r"\(" + m_str + r"\)"),
        "bp": re.compile(r"\(" + p_str + r"\)"),
    }
    subs = {
        "m": lambda x: f"{int(x.group(1)) * int(x.group(2))}",
        "p": lambda x: f"{int(x.group(1)) + int(x.group(2))}",
        "bm": lambda x: f"{int(x.group(1)) * int(x.group(2))}",
        "bp": lambda x: f"{int(x.group(1)) + int(x.group(2))}"
    }

    def orderer(op_name):
        if op_name == "bp": return 0
        if op_name == "bm": return 1
        if op_name == "p": return 2
        return 3

    indices = {(orderer(name), op.search(str_in).start()): name for name, op in patterns.items() if op.search(str_in)}
    return patterns[indices[sorted(indices.keys())[0]]].sub(subs[indices[sorted(indices.keys())[0]]], str_in, 1)


def resolve_all(str_in, add=False, pp=False):
    """
    >>> resolve_all("1 + (2 * 3) + (4 * (5 + 6))")
    '51'
    >>> resolve_all("2 * 3 + (4 * 5)")
    '26'
    >>> resolve_all("5 + (8 * 3 + 9 + 3 * 4 * 3)")
    '437'
    >>> resolve_all("5 * 9 * (7 * 3 * 3 + 9 * 3 + (8 + 6 * 4))")
    '12240'
    >>> resolve_all("((2 + 4 * 9) * (6 + 9 * 8 + 6) + 6) + 2 + 4 * 2")
    '13632'
    >>> resolve_all("1 + (2 * 3) + (4 * (5 + 6))",add=True)
    '51'
    >>> resolve_all("2 * 3 + (4 * 5)",add=True)
    '46'
    >>> resolve_all("5 + (8 * 3 + 9 + 3 * 4 * 3)",add=True)
    '1445'
    >>> resolve_all("5 * 9 * (7 * 3 * 3 + 9 * 3 + (8 + 6 * 4))",add=True)
    '669060'
    >>> resolve_all("((2 + 4 * 9) * (6 + 9 * 8 + 6) + 6) + 2 + 4 * 2",add=True)
    '23340'
    >>> resolve_all("2 + 3 * 4",add=True)
    '20'
    """
    out_str = str_in
    i = 1
    while " " in out_str and i < 100:
        new_str = resolve(out_str) if not add else resolve_add(out_str)
        if new_str == out_str:
            raise (ValueError(f"{out_str} resolved to {new_str} which is the same!"))
        out_str = new_str
        i += 1
        if pp:
            print(out_str)
    return out_str


def part_1():
    lines = pandas.read_csv(r"C:\Users\Joss\PycharmProjects\pythonProject\advent_of_code\2020\day_18.csv", header=None)
    vals = []
    for l in lines[0].tolist():
        vals.append(resolve_all(l))
    return vals


def part_2():
    lines = pandas.read_csv(r"C:\Users\Joss\PycharmProjects\pythonProject\advent_of_code\2020\day_18.csv", header=None)
    vals = []
    for l in lines[0].tolist():
        vals.append(resolve_all(l, add=True, pp=True))
    return vals


if __name__ == '__main__':
    import doctest

    doctest.testmod()
    print(sum([int(i) for i in part_1()]))
    print(sum([int(i) for i in part_2()]))
