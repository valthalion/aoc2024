testing = False
directions = {'>': 1, '<': -1, 'v': 1j, '^': -1j}


class Box:
    width = 1

    def __init__(self, pos, boxes, walls):
        self.pos = pos
        self.boxes = boxes
        self.walls = walls
        self._next_move_boxes = None

    def _step(self, direction):
        if self._next_move_boxes:
            for box in self._next_move_boxes:
                if self._touches(box, direction):  # do not move if already moved through other path
                    box._step(direction)
            self._next_move_boxes = None
        del(self.boxes[self.pos])
        self.pos += direction
        self.boxes[self.pos] = self

    def _touches(self, box, direction):
        if direction.imag != 0:
            return abs(self.pos.imag - box.pos.imag) <= 1
        return abs(self.pos.real - box.pos.real) <= self.width

    def move(self, direction):
        if self._can_move(direction):
            self._step(direction)
            return True
        return False

    def _can_move(self, direction):
        vertical = direction.imag != 0

        if vertical:
            walls = tuple(self.pos + x + direction for x in range(self.width))
        else:
            walls = (self.pos + (self.width if direction == 1 else -1),)
        if any(wall in self.walls for wall in walls):
            return False

        if vertical:
            other_boxes = [self.pos + direction + offset for offset in range(1 - self.width, self.width)]
        else:
            other_boxes = [self.pos + self.width * direction]
        other_boxes = [self.boxes[pos] for pos in other_boxes if pos in self.boxes]
        if not other_boxes:
            return True
        if all(box._can_move(direction) for box in other_boxes):
            self._next_move_boxes = other_boxes
            return True
        return False


def read_data():
    robot, boxes, walls = None, {}, set()
    with open(f'puzzle15-test{testing}.in' if testing else 'puzzle15.in', 'r') as f:
        for row, line in enumerate(f):
            if line == '\n':
                break
            for col, value in enumerate(line.strip()):
                pos = complex(Box.width * col, row)
                if value == '.':
                    continue
                elif value == '@':
                    robot = pos
                elif value == 'O':
                    boxes[pos] = Box(pos, boxes, walls)
                elif value == '#':
                    for offset in range(Box.width):
                        walls.add(pos + offset)
                else:
                    raise ValueError(f'Unknown value: {value}')
        moves = [directions[c] for line in f for c in line.strip()]
    return robot, boxes, walls, moves


def gps(pos):
    return pos.real + 100 * pos.imag


def simulate(robot, boxes, walls, moves):
    for direction in moves:
        new_pos = robot + direction
        if new_pos in walls:
            if testing: show(robot, boxes, walls, direction)
            continue

        if direction == 1:
            box = boxes.get(new_pos, None)
        elif direction == -1:
            box = boxes.get(robot - Box.width, None)
        else:
            for offset in range(1 - Box.width, 1):
                if new_pos + offset in boxes:
                    box = boxes[new_pos + offset]
                    break
            else:
                box = None

        if box is None or box.move(direction):
            robot = new_pos

        if testing: show(robot, boxes, walls, direction)
    return robot


def show(robot, boxes, walls, move):
    num_cols, num_rows = int(max(x.real for x in walls)) + 1, int(max(x.imag for x in walls)) + 1
    lines = [['.'] * num_cols for _ in range(num_rows)]
    lines[int(robot.imag)][int(robot.real)] = '@'
    for x in walls:
        lines[int(x.imag)][int(x.real)] = '#'
    if Box.width == 1:
        for x in boxes:
            lines[int(x.imag)][int(x.real)] = 'O'
    else:  # Box.width 2, not in the mood to generalize this
        for x in boxes:
            lines[int(x.imag)][int(x.real)] = '['
            lines[int(x.imag)][int(x.real) + 1] = ']'
    print()
    print(move)
    for line in lines:
        print(''.join(line))


def main(width):
    Box.width = width
    robot, boxes, walls, moves = read_data()
    if testing: show(robot, boxes, walls, move=None)
    robot = simulate(robot, boxes, walls, moves)
    return int(sum(gps(box) for box in boxes))


def part_1():
    return main(width=1)


def part_2():
    return main(width=2)
