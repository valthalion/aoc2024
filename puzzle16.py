import networkx as nx


testing = False
STEP_COST = 1
TURN_COST = 1_000
turns = {'east': ('north', 'south'), 'west': ('north', 'south'), 'north': ('east', 'west'), 'south': ('east', 'west')}
directions = {'east': 1, 'west': -1, 'north': -1j, 'south': 1j}


def read_data():
    start, end, nodes = None, None, set()
    with open(f'puzzle16-test{testing}.in' if testing else 'puzzle16.in', 'r') as f:
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
    graph = nx.DiGraph()
    for node in nodes:
        for orig, dests in turns.items():
            for dest in dests:
                graph.add_edge((node, orig), (node, dest), weight=0 if node == end else TURN_COST)
        for direction, delta in directions.items():
            other_node = node + delta
            if other_node in nodes:
                graph.add_edge((node, direction), (other_node, direction), weight=STEP_COST)
    return graph, (start, 'east'), (end, 'east')


def part_1():
    graph, start, end = read_data()
    return nx.shortest_path_length(graph, start, end, weight='weight')


def part_2():
    graph, start, end = read_data()
    shortest_paths = nx.all_shortest_paths(graph, start, end, weight='weight')
    common = None
    for bp in shortest_paths:
        if common is None:
            common = {node for node, _ in bp}
            continue
        common |= {node for node, _ in bp}
    return len(common)
