testing = False


def read_data():
    region_map = {}
    graph = {}
    with open(f'puzzle12{"-test" if testing else ""}.in', 'r') as f:
        for row, line in enumerate(f):
            for col, value in enumerate(line.strip()):
                region_map[(row, col)] = value
                graph[(row, col)] = set()
                for neighbour in ((row - 1, col), (row, col - 1)):
                    if neighbour in region_map and region_map[neighbour] == value:
                        graph[neighbour].add((row, col))
                        graph[(row, col)].add(neighbour)
    return graph, region_map


def connected_components(graph):
    nodes, queue = set(graph), set()
    while nodes:
        component = set()
        queue.add(nodes.pop())
        while queue:
            node = queue.pop()
            component.add(node)
            neighbours = graph[node] & nodes
            nodes -= neighbours
            queue |= neighbours
        yield component


def perimeter(region, graph):
    return sum(4 - len(graph[node]) for node in region)


def area(region):
    return len(region)


def price(region, graph):
    return area(region) * perimeter(region, graph)


def move(r, c, heading):
    return (r - heading.imag, c + heading.real)


def perimeter2(region, graph):
    remaining = {
        (node, normal)
        for node in region if len(graph[node]) != 4
        for normal in (1, -1, 1j, -1j) if move(*node, normal) not in region
    }

    sides = 0
    heading, normal = 1, 1j  # moving rightwards, border on top
    current = start = min(node for node, _ in remaining)  # topmost row, as far to the left as possible
    remaining.remove((current, normal))

    while True:
        sides += 1

        # move to the next corner: next pos is outside of region or after it you can turn left within the region
        while (new_pos := move(*current, heading)) in region and move(*new_pos, normal) not in region:
            current = new_pos
            remaining.remove((current, normal))
        if current == start and heading == 1j:  # Got back to the start; second part needed in case the first side is length 1
            break

        if new_pos in region:  # forward possible, new edge turning left
            heading *= 1j
            normal *= 1j
            current = move(*new_pos, heading)  # 1 step to new_pos, turn left, 1 step with new heading
        else:  # new edge turning right, in place
            heading *= -1j
            normal *= -1j
        remaining.remove((current, normal))

    # This covers the outer perimeter so far, now for the perimeter of the 'holes'
    while remaining:
        heading, normal = 1, -1j  # moving rightwards, border at bottom
        current = start = min(node for node, _ in remaining)  # topmost row, as far to the left as possible
        remaining.remove((current, normal))

        while True:
            sides += 1

            # move to the next corner: next pos is outside of region or after it you can turn right within the region
            while (new_pos := move(*current, heading)) in region and move(*new_pos, normal) not in region:
                current = new_pos
                remaining.remove((current, normal))
            if current == move(*start, -(1 + 1j)) and heading == 1j:  # Got back to the start, but from the outside
                break

            if new_pos in region:  # forward possible, new edge turning right
                heading *= -1j
                normal *= -1j
                current = move(*new_pos, heading)  # 1 step to new_pos, turn left, 1 step with new heading
            else:  # new edge turning left, in place
                heading *= 1j
                normal *= 1j
            remaining.remove((current, normal))

    return sides


def price2(region, graph):
    return area(region) * perimeter2(region, graph)


def part_1():
    graph, region_map = read_data()
    regions = connected_components(graph)
    return sum(price(region, graph) for region in regions)


def part_2():
    graph, region_map = read_data()
    regions = connected_components(graph)
    return sum(price2(region, graph) for region in regions)
