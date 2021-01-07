import pandas
from collections import Counter

directs = {
    "N": (0, 1),
    "S": (0, -1),
    "E": (1, 0),
    "W": (-1, 0)

}

degrees = {
    (0, 1): 0,
    (0, -1): 180,
    (1, 0): 90,
    (-1, 0): 270,
    0: (0, 1),
    180: (0, -1),
    90: (1, 0),
    270: (-1, 0),

}

rotations = {
    90: [[0, -1], [1, 0]],
    180: [[-1, 0], [0, -1]],
    270: [[0, 1], [-1, 0]],
}


def apply(command, n, pos, dir):
    if directs.get(command):
        acr, up = directs.get(command)
        pos = (pos[0] + n * acr, pos[1] + n * up)
    elif command == 'F':
        pos = (pos[0] + n * dir[0], pos[1] + n * dir[1])
    elif command == 'L':
        deg = degrees[dir] + (360 - n)
        dir = degrees.get(deg % 360)
    elif command == 'R':
        deg = (degrees[dir] + n) % 360
        dir = degrees.get(deg)
    return pos, dir


def main(part):
    test_set = pandas.read_csv(r"/2020/complete/day_12_test.csv",
                               header=None)
    raw = pandas.read_csv(r"/2020/complete/day_12.csv",
                          header=None)
    raw_c = raw.copy()
    if part == 1:
        pos = (0, 0)
        dir = (1, 0)
        for ord in raw.values:
            pos, dir = apply(ord[0], ord[1], pos, dir)
            print(pos, dir)
        print(pos)
        return abs(pos[0]) + abs(pos[1])
    else:
        pos = (0, 0)
        dir = (1, 0)
        waypos = (10, 1)
        df = raw if part == 2 else test_set
        for ord in df.values:
            if ord[0] == 'F':
                pos = pos[0] + ord[1] * waypos[0], pos[1] + ord[1] * waypos[1]
            elif ord[0] == 'L':
                waypos = pandas.DataFrame(rotations[ord[1]]).dot(waypos)
            elif ord[0] == 'R':
                waypos = pandas.DataFrame(rotations[360 - ord[1]]).dot(waypos)
            else:
                waypos, dir = apply(ord[0], ord[1], waypos, dir)
            print(pos, dir)
        print(pos)
        return abs(pos[0]) + abs(pos[1])


if __name__ == '__main__':
    print(main(2))
