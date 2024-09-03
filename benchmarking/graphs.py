from random import randint, random

import networkx as nx
import numpy as np
from networkx import DiGraph

from spization.utils.graph.properties import is_2_terminal_dag
from spization.utils.graph.sinks import sinks
from spization.utils.graph.sources import sources
from spization.utils.sp.serial_parallel_decomposition import Node


def make_random_2_terminal_dag(num_nodes: int, p: float) -> DiGraph:
    g = nx.DiGraph()

    g.add_nodes_from(range(num_nodes))

    for i in range(num_nodes):
        for j in range(i + 1, num_nodes):
            if random() < p:
                g.add_edge(i, j)

    source = 0
    sink = num_nodes - 1

    for node in sources(g) - {source}:
        g.add_edge(source, node)

    for node in sinks(g) - {sink}:
        g.add_edge(node, sink)

    assert is_2_terminal_dag(g)
    return g


def make_random_local_2_terminal_dag(
    num_nodes: int, p: float, locality_ratio: float
) -> DiGraph:
    g = nx.DiGraph()

    g.add_nodes_from(range(num_nodes))

    locality_window = max(1, num_nodes * locality_ratio)

    for i in range(num_nodes):
        max_j = int(min(i + 1 + locality_window, num_nodes))
        for j in range(i + 1, max_j):
            if random() < p:
                g.add_edge(i, j)
    assert is_2_terminal_dag(g)

    source = 0
    sink = num_nodes - 1

    for node in sources(g) - {source}:
        g.add_edge(source, node)

    for node in sinks(g) - {sink}:
        g.add_edge(node, sink)

    assert is_2_terminal_dag(g)
    return g


def make_random_nasbench_101() -> DiGraph:
    MAX_NODES = 7
    MAX_EDGES = 9

    def make_cell() -> DiGraph:
        num_nodes: int = randint(1, MAX_NODES)
        num_edges: int = randint(num_nodes - 1, MAX_EDGES)
        config = np.triu(np.random.matrix(2, size=(num_nodes - 2, num_nodes - 2)))
        input: Node = 0
        output: Node = num_nodes - 1
        g = DiGraph()
        return g

    def is_valid_cell(cell: DiGraph) -> bool:
        assert len(cell.nodes()) <= MAX_NODES
        assert len(cell.edges()) <= MAX_EDGES

def make_taso_nasnet_a():
    ...

# TODO:other results