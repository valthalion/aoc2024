testing = False


def parse_button(line, sep):
    _, point = line.strip().split(': ')
    x, y = point.split(', ')
    _, x = x.split(sep)
    _, y = y.split(sep)
    x = int(x)
    y = int(y)
    return x, y


class Machine:
    def __init__(self, line1, line2, line3, prize_offset=0):
        self.a = parse_button(line1, '+')
        self.b = parse_button(line2, '+')
        self.prize = parse_button(line3, '=')
        self.prize = tuple(prize_offset + x for x in self.prize)

    def win(self):
        (xa, ya), (xb, yb), (xp, yp) = self.a, self.b, self.prize
        b = (xa * yp - xp * ya) // (xa * yb - xb * ya)
        a = (xp - xb * b) // xa
        if a * xa + b * xb == xp and a * ya + b * yb == yp:
            return 3 * a + b
        return None


def read_data(prize_offset=0):
    machines = []
    with open(f'puzzle13{"-test" if testing else ""}.in', 'r') as f:
        while True:
            lines = next(f), next(f), next(f)
            machines.append(Machine(*lines, prize_offset=prize_offset))
            try:
                next(f)
            except StopIteration:
                break
    return machines


def part_1():
    machines = read_data()
    total = 0
    for machine in machines:
        result = machine.win()
        if result is not None:
            total += result
    return total


def part_2():
    machines = read_data(prize_offset=10000000000000)
    total = 0
    for machine in machines:
        result = machine.win()
        if result is not None:
            total += result
    return total
