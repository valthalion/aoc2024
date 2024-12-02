from operator import gt, lt


def read_data():
    with open('puzzle02.in', 'r') as f:
        for line in f:
            yield [int(x) for x in line.strip().split()]


def safe(levels):
    direction = gt if levels[1] > levels[0] else lt
    for pred, succ in zip(levels, levels[1:]):
        if not direction(succ, pred):
            return False
        if not 1 <= abs(pred - succ) <= 3:
            return False
    return True


def safe_dampened(levels):
    diffs = [succ - pred for pred, succ in zip(levels, levels[1:])]
    direction = (lambda x: x < 0) if sum(diffs) < 0 else (lambda x: x > 0)

    def safe_step(diff):
        return direction(diff) and 1 <= abs(diff) <= 3

    if safe_step(diffs[0]):
        dampened, idx = False, 1
    else:
        if safe_step(diffs[1]) or safe_step(diffs[0] + diffs[1]):  # Just drop the first or second value
            dampened, idx = True, 2  # idx == 1 is already checked
        else:
            return False

    while idx < len(diffs):
        if safe_step(diffs[idx]):
            idx += 1
            continue

        if dampened:
            return False

        if idx == len(diffs) - 1:  # drop last value
            return True

        if safe_step(diffs[idx] + diffs[idx - 1]):  # try to drop value at idx
            dampened = True
            idx += 1
        elif safe_step(diffs[idx] + diffs[idx + 1]):  # try to drop value at idx + 1
            dampened = True
            idx += 2
        else:
            return False

    return True



def part_1():
    return sum(1 for levels in read_data() if safe(levels))


def part_2():
    return sum(1 for levels in read_data() if safe_dampened(levels))
