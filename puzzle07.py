from operator import add, mul


testing = False


def read_data():
    with open(f'puzzle07{"-test" if testing else ""}.in', 'r') as f:
        for line in f:
            target, numbers = line.strip().split(': ')
            yield int(target), tuple(int(n) for n in numbers.split())


def concat(x, y):
    return int(''.join((str(x), str(y))))


def is_possible(target, numbers, operators):
    if len(numbers) == 1:
        return target == numbers[0]
    if target < numbers[0]:  # concat, + and * can only increase the result, so we can prune this branch
        return False

    for op in operators:
        if is_possible(target, (op(*numbers[:2]), *numbers[2:]), operators):
            return True
    return False


def part_1():
    operators = (mul, add)
    return sum(target for target, numbers in read_data() if is_possible(target, numbers, operators))


def part_2():
    operators = (concat, mul, add)
    return sum(target for target, numbers in read_data() if is_possible(target, numbers, operators))
