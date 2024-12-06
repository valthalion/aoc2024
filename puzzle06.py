from collections import defaultdict


testing = False


def read_data():
    obstacles, pos = set(), None

    with open(f'puzzle06{'-test' if testing else ''}.in', 'r') as f:
        for row, line in enumerate(f):
            for col, value in enumerate(line.strip()):
                if value == '.':
                    continue
                if value == '#':
                    obstacles.add(complex(col, -row))
                elif value == '^':
                    pos = complex(col, -row)
                else:
                    raise RuntimeError(f'Invalid character "{value}" at ({row}, {col}).')
    vert_scroll = complex(0, row)
    obstacles = {vert_scroll + obs for obs in obstacles}
    pos += vert_scroll

    def in_bounds(p):
        if not 0 <= p.real <= col:
            return False
        return 0 <= p.imag <= row

    return obstacles, in_bounds, pos


def trace_path(obstacles, in_bounds, start, heading=1j, path_prefix=None, new_loop=None, new_obstacles=0):
    loops = set()
    path = defaultdict(set)
    if path_prefix:
        for pos, headings in path_prefix.items():
            path[pos] = set(headings)
    pos = start  # override value of 'pos' after the loop

    while True:
        if pos in path and heading in path[pos]:
            loops.add(new_loop)
            return path, loops

        path[pos].add(heading)

        new_pos = pos + heading
        if new_pos in obstacles:
            heading *= -1j
            continue
        if not in_bounds(new_pos):
            break
        if new_obstacles and new_pos not in path:
            _, maybe_loop = trace_path(obstacles | {new_pos}, in_bounds, pos, heading=-1j * heading,
                                       path_prefix=path, new_loop=new_pos, new_obstacles=new_obstacles - 1)
            loops |= maybe_loop

        pos = new_pos

    return path, loops


def part_1():
    obstacles, in_bounds, pos = read_data()
    path, _ = trace_path(obstacles, in_bounds, pos)
    return len(path)


def part_2():
    obstacles, in_bounds, pos = read_data()
    _, loops = trace_path(obstacles, in_bounds, pos, new_obstacles=1)
    return len(loops)
