testing = False


def read_data(target):
    table = {}
    with open(f'puzzle04{'-test' if testing else ''}.in', 'r') as f:
        for row, line in enumerate(f):
            for col, value in enumerate(line.strip()):
                if value in target:
                    table[(row, col)] = value
    nrows, ncols = row + 1, col + 1
    return table, nrows, ncols


def paths(row, col, nrows, ncols, target_len):
    right = col + target_len <= ncols
    left = col >= target_len - 1
    up = row >= target_len - 1
    down = row + target_len <= nrows

    if right:
        yield ((row, c) for c in range(col, col + target_len))
    if left:
        yield ((row, c) for c in range(col, col - target_len, -1))
    if up:
        yield ((r, col) for r in range(row, row - target_len, -1))
    if down:
        yield ((r, col) for r in range(row, row + target_len))
    if right and up:
        yield zip(range(row, row - target_len, -1), range(col, col + target_len))
    if right and down:
        yield zip(range(row, row + target_len), range(col, col + target_len))
    if left and up:
        yield zip(range(row, row - target_len, -1), range(col  , col - target_len, -1))
    if left and down:
        yield zip(range(row, row + target_len), range(col, col - target_len, -1))


def find_words(target, table, nrows, ncols):
    target_len = len(target)
    for row in range(nrows):
        for col in range(ncols):
            if (row, col) not in table:
                continue
            if table[(row, col)] != target[0]:
                continue
            for path in paths(row, col, nrows, ncols, target_len):
                if ''.join(table.get(pos, '') for pos in path) == target:
                    yield 1


def neighbours(row, col):
    yield (row - 1, col - 1)
    yield (row - 1, col + 1)
    yield (row + 1, col - 1)
    yield (row + 1, col + 1)


def find_crosses(table, nrows, ncols):
    for row in range(1, nrows - 1):
        for col in range(1, ncols - 1):
            if table.get((row, col), '') != 'A':
                continue
            if (''.join(sorted(table.get(pos, '') for pos in neighbours(row, col))) == 'MMSS'
                    and table[(row - 1, col - 1)] != table[(row + 1, col + 1)]):
                yield 1


def part_1():
    target = 'XMAS'
    table, nrows, ncols = read_data(target)
    return sum(find_words(target, table, nrows, ncols))


def part_2():
    target = 'MAS'
    table, nrows, ncols = read_data(target)
    return sum(find_crosses(table, nrows, ncols))
