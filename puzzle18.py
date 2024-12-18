import networkx as nx


testing = False


def read_data():
    with open(f'puzzle18{"-test" if testing else ""}.in', 'r') as f:
        for line in f:
            yield tuple(int(n) for n in line.split(','))


def full_graph(size):
    nodes = {(col, row) for row in range(size + 1) for col in range(size + 1)}
    graph = nx.Graph()
    for col, row in nodes:
        if (col - 1, row) in nodes: graph.add_edge((col, row), (col - 1, row))
        if (col, row - 1) in nodes: graph.add_edge((col, row), (col, row - 1))
    return graph


def part_1():
    time = 12 if testing else 1024
    size = 6 if testing else 70
    graph = full_graph(size)
    start, end = (0, 0), (size, size)
    for idx, node in enumerate(read_data()):
        if idx >= time:
            break
        graph.remove_node(node)
    return nx.shortest_path_length(graph, start, end)


def part_2():
    time = 12 if testing else 1024
    size = 6 if testing else 70
    graph = full_graph(size)
    start, end = (0, 0), (size, size)
    for idx, node in enumerate(read_data()):
        graph.remove_node(node)
        if idx >= time and not nx.has_path(graph, start, end):
            break
    return ','.join(str(n) for n in node)
