from collections import defaultdict
from fractions import Fraction


testing = False


def read_data():
    antennas = defaultdict(list)
    with open(f'puzzle08{"-test" if testing else ""}.in', 'r') as f:
        for row, line in enumerate(f):
            for col, freq in enumerate(line.strip()):
                if freq == '.':
                    continue
                antennas[freq].append((row, col))
        return antennas, row + 1, col + 1


def find_antinodes(antennas, nrows, ncols):
    def in_bounds(r, c):
        return 0 <= r < nrows and 0 <= c < ncols

    antinodes = set()
    for freq, locations in antennas.items():
        if len(locations) < 2:
            continue
        for idx, (row1, col1) in enumerate(locations[:-1]):
            for (row2, col2) in locations[idx + 1:]:
                rowdiff, coldiff = row1 - row2, col1 - col2
                antinode = (row1 + rowdiff, col1 + coldiff)
                if in_bounds(*antinode):
                    antinodes.add(antinode)
                antinode = (row2 - rowdiff, col2 - coldiff)
                if in_bounds(*antinode):
                    antinodes.add(antinode)
    return antinodes


def line(row1, col1, row2, col2, nrows, ncols):
    if row1 == row2:
        for c in range(0, ncols):
            yield (row1, c)
            return

    if col1 == col2:
        for r in range(0, nrows):
            yield (r, col1)
            return

    slope = Fraction(row2 - row1, col2 - col1)
    r, c = row1, col1
    while 0 <= r < nrows and 0 <= c < ncols:
        yield (r, c)
        r += slope.numerator
        c += slope.denominator
    r, c = row1 - slope.numerator, col1 - slope.denominator
    while 0 <= r < nrows and 0 <= c < ncols:
        yield (r, c)
        r -= slope.numerator
        c -= slope.denominator


def find_harmonic_antinodes(antennas, nrows, ncols):
    antinodes = set()
    for freq, locations in antennas.items():
        if len(locations) < 2:
            continue
        for idx, (row1, col1) in enumerate(locations[:-1]):
            for (row2, col2) in locations[idx + 1:]:
                antinodes |= set(line(row1, col1, row2, col2, nrows, ncols))
    return antinodes


def part_1():
    antennas, nrows, ncols = read_data()
    antinodes = find_antinodes(antennas, nrows, ncols)
    return len(antinodes)


def part_2():
    antennas, nrows, ncols = read_data()
    antinodes = find_harmonic_antinodes(antennas, nrows, ncols)
    return len(antinodes)
