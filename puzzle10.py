from collections import defaultdict


testing = False


def read_data():
    heightmap, graph, trailheads = {}, defaultdict(set), set()
    with open(f'puzzle10{"-test" if testing else ""}.in', 'r') as f:
        for row, line in enumerate(f):
            for col, value in enumerate(line.strip()):
                node = (row, col)
                heightmap[node] = int(value)
                if heightmap[node] == 0:
                    trailheads.add(node)
                for neighbour in ((row - 1, col), (row, col - 1)):
                    if neighbour not in heightmap:
                        continue
                    if heightmap[neighbour] - heightmap[node] == 1:
                        graph[node].add(neighbour)
                    elif heightmap[node] - heightmap[neighbour] == 1:
                        graph[neighbour].add(node)
    return heightmap, graph, trailheads


def visit(graph, root):
    seen, queue = set(), {root}
    while queue:
        node = queue.pop()
        seen.add(node)
        queue |= graph[node] - seen
        yield node


def score(heightmap, graph, trailhead):
    return sum(1 for node in visit(graph, trailhead) if heightmap[node] == 9)


def rating(heightmap, graph, trailhead):
    if heightmap[trailhead] == 9:
        return 1
    if trailhead not in graph or not graph[trailhead]:
        return 0
    return sum(rating(heightmap, graph, node) for node in graph[trailhead])


def part_1():
    heightmap, graph, trailheads = read_data()
    return sum(score(heightmap, graph, trailhead) for trailhead in trailheads)


def part_2():
    heightmap, graph, trailheads = read_data()
    return sum(rating(heightmap, graph, trailhead) for trailhead in trailheads)
