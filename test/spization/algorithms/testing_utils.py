import random

import networkx as nx


def make_linear(length):
    G = nx.DiGraph()
    if length == 0:
        return G
    G.add_nodes_from(range(length))
    G.add_edges_from([(i, i + 1) for i in range(length - 1)])
    return G


def make_rhombus():
    G = nx.DiGraph()
    G.add_nodes_from(range(4))
    G.add_edges_from([(0, 1), (0, 2), (1, 3), (2, 3)])
    return G


def make_diamond():
    G = nx.DiGraph()
    G.add_nodes_from(range(6))
    G.add_edges_from([(0, 1), (0, 2), (1, 3), (2, 3), (2, 4), (3, 5), (4, 5)])
    return G


def make_fully_connected(layer_sizes):
    G = nx.DiGraph()
    node_id = 0
    layers = []
    for size in layer_sizes:
        layer = list(range(node_id, node_id + size))
        layers.append(layer)
        node_id += size
    G.add_nodes_from(range(node_id))
    for i in range(len(layers) - 1):
        for n1 in layers[i]:
            for n2 in layers[i + 1]:
                G.add_edge(n1, n2)
    return G


def make_parallel_chains(chain_length, chain_num):
    assert chain_length >= 3
    assert chain_num >= 1
    G = nx.DiGraph()
    node_id = 1
    chains = []
    for _ in range(chain_num):
        chain = list(range(node_id, node_id + chain_length - 2))
        chains.append(chain)
        node_id += chain_length - 2
    G.add_nodes_from(range(node_id + 1))
    for chain in chains:
        G.add_edge(0, chain[0])
        G.add_edge(chain[-1], node_id)
        G.add_edges_from(zip(chain[:-1], chain[1:]))
    return G


def make_2_terminal_random_dag(num_nodes, p):
    G = nx.DiGraph()

    G.add_nodes_from(range(num_nodes))

    for i in range(num_nodes - 2):
        for j in range(i + 1, num_nodes - 1):
            if random.random() < p:
                G.add_edge(i, j)

    for i in range(1, num_nodes - 1):
        if G.in_degree(i) == 0:
            G.add_edge(0, i)
        if G.out_degree(i) == 0:
            G.add_edge(i, num_nodes - 1)

    if G.out_degree(0) == 0:
        G.add_edge(0, 1)

    if G.in_degree(num_nodes - 1) == 0:
        G.add_edge(num_nodes - 2, num_nodes - 1)

    return G


def graph_generator():
    yield make_linear(3)
    yield make_linear(10)
    yield make_rhombus()
    yield make_diamond()
    yield make_fully_connected((1, 5, 1))
    yield make_fully_connected((1, 3, 5, 10, 5, 8, 1))
    # yield make_parallel_chains(9, 3)
    yield make_2_terminal_random_dag(25, 0.1)
    # yield make_2_terminal_random_dag(50, 0.05)
    # yield make_2_terminal_random_dag(30, 0.15)
