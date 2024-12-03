import re


mult_re = re.compile(r'mul\((?P<x>\d{1,3})\,(?P<y>\d{1,3})\)')
instructions_re = re.compile(r'mul\((?P<x>\d{1,3})\,(?P<y>\d{1,3})\)|do\(\)|don\'t\(\)')


def read_data():
    with open('puzzle03.in', 'r') as f:
        memory = '/n'.join(f)
    return memory.strip()


def find_multiplies(memory):
    for m in mult_re.finditer(memory):
        yield int(m.group('x')), int(m.group('y'))


def find_multiplies2(memory):
    enabled = True
    for m in instructions_re.finditer(memory):
        if m[0] == 'do()':
            enabled = True
        elif m[0] == 'don\'t()':
            enabled = False
        elif enabled:  # mul operation AND enabled
            yield int(m.group('x')), int(m.group('y'))


def part_1():
    memory = read_data()
    result = sum(x * y for x, y in find_multiplies(memory))
    return result


def part_2():
    memory = read_data()
    result = sum(x * y for x, y in find_multiplies2(memory))
    return result
