testing = False


def norm1(x, y):
    return int(abs(x.real - y.real) + abs(x.imag - y.imag))


def neighbours(node):
    return {node + 1, node - 1, node + 1j, node - 1j}


def deltas(distance):
    result = set()
    for r in range(distance + 1):
        for i in range(distance - r + 1):
            if r + i <= 1:
                continue
            result.add(complex(r, i))
            result.add(complex(r, -i))
            result.add(complex(-r, i))
            result.add(complex(-r, -i))
    return result


def distance_neighbours(node, distance):
    return {node + delta for delta in deltas(distance)}


def build_path(nodes, start, end):
    path = {}
    seen = set()
    current = start
    while True:
        seen.add(current)
        next_node = (neighbours(current) & nodes) - seen
        if not next_node:
            break
        next_node = next_node.pop()
        path[current] = next_node
        current = next_node
    path[end] = None
    return path


def calculate_distances(path, start, end):
    distances = {end: 0}
    stack = []
    current = start
    while current != end:
        stack.append(current)
        current = path[current]
    while stack:
        node = stack.pop()
        next_node = path[node]
        distances[node] = distances[next_node] + 1
    return distances


def read_data():
    nodes, start, end = set(), None, None
    with open(f'puzzle20{"-test" if testing else ""}.in', 'r') as f:
        for row, line in enumerate(f):
            for col, value in enumerate(line.strip()):
                if value == '#':
                    continue
                node = complex(col, row)
                if value == 'S':
                    start = node
                elif value == 'E':
                    end = node
                nodes.add(node)
    path = build_path(nodes, start, end)
    distances = calculate_distances(path, start, end)
    return path, distances, start, end


def cheats(path, distances, distance, start, end):
    path_nodes = set(path)
    current = start
    while distances[current] > distance:
        for next_node in distance_neighbours(current, distance) & path_nodes:
            saved_time = distances[current] - distances[next_node] - norm1(current, next_node)  # discount time elpsed during cheat
            if saved_time > 0:
                yield saved_time
        current = path[current]


def best_cheats(path, distances, start, end, cheat_distance, limit, test_limit):
    counts = {}
    for saved_time in cheats(path, distances, cheat_distance, start, end):
        if saved_time in counts:
            counts[saved_time] += 1
        else:
            counts[saved_time] = 1

    saving_limit = test_limit if testing else limit
    if testing:
        for saved_time in sorted(counts):
            if saved_time < saving_limit:
                continue
            print(saved_time, '->', counts[saved_time])
    return sum(count for saved_time, count in counts.items() if saved_time >= saving_limit)


def part_1():
    path, distances, start, end = read_data()
    return best_cheats(path, distances, start, end, cheat_distance=2, limit=100, test_limit=0)


def part_2():
    path, distances, start, end = read_data()
    return best_cheats(path, distances, start, end, cheat_distance=20, limit=100, test_limit=50)
