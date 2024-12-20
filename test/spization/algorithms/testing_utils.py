import random
import networkx as nx
from collections import deque
import numpy as np


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


def make_binary_dag(depth):
    """Create a DAG resembling a binary tree with a final sink node."""
    G = nx.DiGraph()
    num_nodes_without_sink = 2**depth - 1
    num_nodes = num_nodes_without_sink + 1  # Add one node for the sink

    G.add_nodes_from(range(num_nodes))
    sink_node = num_nodes - 1

    for i in range((num_nodes_without_sink - 1) // 2):
        left_child = 2 * i + 1
        right_child = 2 * i + 2

        if left_child < num_nodes_without_sink:
            G.add_edge(i, left_child)

        if right_child < num_nodes_without_sink:
            G.add_edge(i, right_child)

    # Connect leaf nodes to the sink
    for leaf in range((num_nodes_without_sink - 1) // 2, num_nodes_without_sink):
        G.add_edge(leaf, sink_node)

    return G


def make_random_2_terminal_dag(num_nodes: int, p: float) -> nx.DiGraph:
    g = nx.DiGraph()

    g.add_nodes_from(range(num_nodes))

    for i in range(num_nodes):
        for j in range(i + 1, num_nodes):
            if random.random() < p:
                g.add_edge(i, j)

    source = 0
    sink = num_nodes - 1

    # Ensure all sources except the actual source connect to it
    for node in range(1, num_nodes):
        if g.in_degree(node) == 0 and node != source:
            g.add_edge(source, node)

    # Ensure all sinks except the actual sink connect to it
    for node in range(num_nodes - 1):
        if g.out_degree(node) == 0 and node != sink:
            g.add_edge(node, sink)

    return g


def make_random_local_2_terminal_dag(
    num_nodes: int, p: float, locality_ratio: float
) -> nx.DiGraph:
    g = nx.DiGraph()

    g.add_nodes_from(range(num_nodes))

    locality_window = max(1, num_nodes * locality_ratio)

    for i in range(num_nodes):
        max_j = int(min(i + 1 + locality_window, num_nodes))
        for j in range(i + 1, max_j):
            if random.random() < p:
                g.add_edge(i, j)

    source = 0
    sink = num_nodes - 1

    # Ensure all sources except the actual source connect to it
    for node in range(1, num_nodes):
        if g.in_degree(node) == 0 and node != source:
            g.add_edge(source, node)

    # Ensure all sinks except the actual sink connect to it
    for node in range(num_nodes - 1):
        if g.out_degree(node) == 0 and node != sink:
            g.add_edge(node, sink)

    return g


def graph_generator():
    # Existing DAG graphs
    yield make_linear(3)
    yield make_linear(10)
    yield make_rhombus()
    yield make_diamond()
    yield make_fully_connected((1, 5, 1))
    yield make_fully_connected((1, 3, 5, 10, 5, 8, 1))
    yield make_parallel_chains(9, 3)
    yield make_binary_dag(3)
    yield make_binary_dag(6)

    for _ in range(5):
        yield make_random_2_terminal_dag(random.randint(10, 30), random.random() ** 4)

    for _ in range(5):
        yield make_random_local_2_terminal_dag(
            random.randint(10, 30), random.random() ** 4, random.random() ** 3
        )
