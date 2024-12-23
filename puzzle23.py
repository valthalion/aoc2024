import networkx as nx


testing = False


def read_data():
    graph = nx.Graph()
    with open(f'puzzle23{"-test" if testing else ""}.in', 'r') as f:
        for line in f:
            graph.add_edge(*line.strip().split('-'))
    return graph


def find_3cliques(graph):
    cliques = set()
    for node in graph:
        neighbours = set(graph[node])
        for second_node in neighbours:
            clique_nodes = set(graph[second_node]) & neighbours
            for third_node in clique_nodes:
                cliques.add(frozenset((node, second_node, third_node)))
    return cliques


def find_password(graph):
    for clique in nx.enumerate_all_cliques(graph):
        pass  # just get to the last one, which is the largest
    return ','.join(sorted(clique))


def part_1():
    graph = read_data()
    all_3cliques = find_3cliques(graph)
    return sum(1 for clique in all_3cliques if any(computer[0] == 't' for computer in clique))


def part_2():
    graph = read_data()
    return find_password(graph)
