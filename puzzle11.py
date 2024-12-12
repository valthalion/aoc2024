testing = False


def read_data():
    with open(f'puzzle11{"-test" if testing else ""}.in', 'r') as f:
        return (int(n) for n in next(f).split())


def blink(stone, times):
    if times == 0:
        return (stone,)

    if stone == 0:
        return blink(1, times - 1)

    stone_str = str(stone)
    stone_len = len(stone_str)
    if stone_len % 2 == 0:
        midpoint = stone_len // 2
        stone1, stone2 = int(stone_str[:midpoint]), int(stone_str[midpoint:])
        return (*blink(stone1, times - 1), *blink(stone2, times - 1))

    return blink(stone * 2024, times - 1)


def part_1():
    stones = read_data()
    return sum(len(blink(stone, 25)) for stone in stones)
