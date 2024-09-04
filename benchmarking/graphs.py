from random import randint, random

import networkx as nx
import numpy as np
from networkx import DiGraph

from spization.__internals.general import get_only
from spization.__internals.graph import is_2_terminal_dag, sinks, sources
from spization.objects import PureNode
from spization.utils import graph_serial_composition


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

    source = 0
    sink = num_nodes - 1

    for node in sources(g) - {source}:
        g.add_edge(source, node)

    for node in sinks(g) - {sink}:
        g.add_edge(node, sink)

    assert is_2_terminal_dag(g)
    return g


def make_random_nasbench_101() -> DiGraph:
    MIN_NODES = 7
    MAX_NODES = 7
    MAX_EDGES = 9
    NUM_CELLS = 9

    def make_cell() -> DiGraph:
        num_nodes: int = randint(MIN_NODES, MAX_NODES)
        inner_nodes_config = np.triu(
            np.random.randint(2, size=(num_nodes - 2, num_nodes - 2))
        )
        input = PureNode(0)
        output = PureNode(num_nodes - 1)
        inner_nodes = [PureNode(i) for i in range(1, num_nodes - 1)]
        g = DiGraph()
        g.add_node(input)
        g.add_node(output)
        for n in inner_nodes:
            g.add_node(n)
        for a in inner_nodes:
            for b in inner_nodes:
                if inner_nodes_config[a - 1][b - 1]:
                    g.add_edge(a, b)
        for node in inner_nodes:
            if g.in_degree(node) == 0:
                g.add_edge(input, node)
            if g.out_degree(node) == 0:
                g.add_edge(node, output)
        return g

    def is_valid_cell(cell: DiGraph) -> bool:
        if not MIN_NODES <= len(cell.nodes()) <= MAX_NODES:
            return False
        if len(cell.edges()) > MAX_EDGES:
            return False
        if not is_2_terminal_dag(cell):
            return False
        if not nx.is_weakly_connected(cell):
            return False
        if get_only(sources(cell)) != PureNode(0):
            return False
        if get_only(sinks(cell)) != max(cell.nodes()):
            return False
        return True

    while True:
        cell = make_cell()
        if is_valid_cell(cell):
            break
    cells = []
    for i in range(NUM_CELLS):
        offset = i * MAX_NODES
        relabeled_cell = nx.relabel_nodes(cell, lambda x: x + offset)
        cells.append(relabeled_cell)
    net = graph_serial_composition(cells)
    return net


def make_taso_nasnet_a() -> DiGraph: ...


def make_efficient_net() -> DiGraph: ...
