from collections import Counter


def read_data():
    list1, list2 = [], []
    with open('puzzle01.in', 'r') as f:
        for line in f:
            x, y = line.strip().split()
            list1.append(int(x))
            list2.append(int(y))
    return list1, list2


def dists(list1, list2):
    for x, y in zip(sorted(list1), sorted(list2)):
        yield abs(x -y)


def sims(list1, list2):
    list2_counts = Counter(list2)
    for x in list1:
        yield x * list2_counts[x]


def part_1():
    list1, list2 = read_data()
    return sum(dists(list1, list2))


def part_2():
    list1, list2 = read_data()
    return sum(sims(list1, list2))
