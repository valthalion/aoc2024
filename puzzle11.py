testing = False


def read_data():
    with open(f'puzzle11{"-test" if testing else ""}.in', 'r') as f:
        return (int(n) for n in next(f).split())


def cached(f):
    cache = {}
    def inner(*args):
        if args not in cache:
            cache[args] = f(*args)
        return cache[args]
    return inner


@cached
def blink_len(stone, times):
    if times == 0:
        return 1

    if stone == 0:
        return blink_len(1, times - 1)

    stone_str = str(stone)
    stone_len = len(stone_str)
    if stone_len % 2 == 0:
        midpoint = stone_len // 2
        stone1, stone2 = int(stone_str[:midpoint]), int(stone_str[midpoint:])
        return blink_len(stone1, times - 1) + blink_len(stone2, times - 1)
    return blink_len(stone * 2024, times - 1)


def part_1():
    stones = read_data()
    return sum(blink_len(stone, 25) for stone in stones)


def part_2():
    stones = read_data()
    return sum(blink_len(stone, 75) for stone in stones)
