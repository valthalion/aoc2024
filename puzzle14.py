from math import prod
from typing import NamedTuple


testing = False
foldx = 11 if testing else 101
foldy = 7 if testing else 103
midx = foldx // 2
midy = foldy // 2


class Vector(NamedTuple):
    x: int
    y: int

    def __add__(self, other):
        return Vector((self.x + other.x) % foldx, (self.y + other.y) % foldy)

    def __mul__(self, scalar):
        return Vector((self.x * scalar) % foldx, (self.y * scalar) % foldy)


class Robot(NamedTuple):
    pos: Vector
    vel: Vector

    def move(self, t):
        return self.pos + self.vel * t


def read_data():
    robots = []
    with open(f'puzzle14{"-test" if testing else ""}.in', 'r') as f:
        for line in f:
            pos, vel = line.strip().split()
            _, pos = pos.split('=')
            x, y = pos.split(',')
            pos = Vector(int(x), int(y))
            _, vel = vel.split('=')
            x, y = vel.split(',')
            vel = Vector(int(x), int(y))
            robots.append(Robot(pos, vel))
    return robots


def quadrant(pos):
    if pos.x == midx or pos.y == midy:
        return None
    q = 0
    if pos.x > midx:
        q += 1
    if pos.y > midy:
        q += 2
    return q


def show(positions):
    pic = [[' '] * foldx for _ in range(foldy)]
    for pos in positions:
        pic[pos.y][pos.x] = 'X'
    for line in pic:
        print(''.join(line))


def part_1():
    robots = read_data()
    robots_in_quadrants = {q: 0 for q in range(4)}
    for robot in robots:
        if (q := quadrant(robot.move(100))) is not None:
            robots_in_quadrants[q] += 1
    return prod(robots_in_quadrants.values())


def part_2():
    # Redirect to file for easy viewing, quick scan
    # First look one by one up to 3-4 hundred reveals a clear 101-step pattern
    # Just following the 101-step sequence soon leads to the christmass tree

    # robots = read_data()
    # for t in range(4945, 5000, 101):
    #     print(t)
    #     positions = [robot.move(t) for robot in robots]
    #     show(positions)
    #     print()
    #     print('*' * foldx)
    #     print()
    show([robot.move(7672) for robot in robots])
    return 7672
