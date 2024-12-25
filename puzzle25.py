testing = False


def encode(schematic, is_key):
    to_count = '#' if is_key else '.'
    numeric = [[1 if c == to_count else 0 for c in line] for line in schematic]
    transpose = zip(*numeric)
    return tuple(sum(row) for row in transpose)


def read_data():
    keys, locks = set(), set()
    with open(f'puzzle25{"-test" if testing else ""}.in', 'r') as f:
        while True:
            line = f.readline().strip()
            is_key = all(c == '.' for c in line)
            schematic = [f.readline().strip() for _ in range(5)]
            (keys if is_key else locks).add(encode(schematic, is_key))
            f.readline()  # skip last line, not relevant
            if not f.readline():  # EOF, otherwise '\n' separatign schematics
                break
    return keys, locks


def fit(key, lock):
    return all(k <= l for k, l in zip(key, lock))


def part_1():
    keys, locks = read_data()
    count = sum(1 for key in keys for lock in locks if fit(key, lock))
    return count


def part_2():
    pass
