import pandas as pd

from advent_of_code.aoc2022.tools import get_file_location

strategy1 = dict(A="R", B="P", C="S")
strategy2 = dict(X="R", Y="P", Z="S")
points = dict(R=1, P=2, S=3)
outcome = dict(W=6, D=3, L=0)

strategy22 = dict(X=0, Y=3, Z=6)
movement = dict(X=-1, Y=0, Z=1)
values = ["R", "P", "S"]


def determine_outcome(me, you, **_kwargs):
    if me == you:
        return "D"
    if (me, you) in [("R", "S"), ("S", "P"), ("P", "R")]:
        return "W"
    return "L"

def determine_input(you, me):
    return values[(values.index(you) + movement.get(me)) % 3]

def main1():
    fn = get_file_location("day_2.csv")
    data = pd.read_csv(fn)
    data['you'] = data['one'].apply(strategy1.get)
    data['me'] = data['two'].apply(strategy2.get)
    data['outcome'] = data.apply(lambda r: determine_outcome(r['you'], r['two']), axis=1)
    data['points'] = data['outcome'].apply(outcome.get) + data['me'].apply(points.get)
    print(data['points'].sum())
    print("Done")


def main2():
    fn = get_file_location("day_2.csv")
    data = pd.read_csv(fn)
    data['you'] = data['one'].apply(strategy1.get)
    data['outcome'] = data['two'].apply(strategy22.get)
    data['me'] = data.apply(lambda r: determine_input(r['you'], r['two']), axis=1)
    data['points'] = data['outcome'] + data['me'].apply(points.get)
    print(data['points'].sum())
    print("Done")


if __name__ == '__main__':
    main2()
