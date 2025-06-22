from collections import deque
from random import randint, random

import networkx as nx
import numpy as np
from networkx import DiGraph

from spization.__internals.general import get_only
from spization.__internals.graph import (
    add_edges,
    add_nodes,
    is_2_terminal_dag,
    sinks,
    sources,
)
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
        g.add_edge(node - 1, node)

    for node in sinks(g) - {sink}:
        g.add_edge(node, node + 1)

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
        if is_valid_cell(cell) and spg_to_sp(cell) is None:
            break
    cells = []
    for i in range(NUM_CELLS):
        offset = i * MAX_NODES
        relabeled_cell = nx.relabel_nodes(cell, lambda x: x + offset)
        cells.append(relabeled_cell)
    net = graph_serial_composition(cells)
    return net


def make_normal_taso_nasnet_cell() -> tuple[nx.DiGraph, PureNode, PureNode]:
    g = nx.DiGraph()

    inputs = add_nodes(g, 2)
    sep = add_nodes(g, 5)
    id_nodes = add_nodes(g, 2)
    avg = add_nodes(g, 3)
    add_nodes_list = add_nodes(g, 5)
    concat = add_nodes(g, 1)

    edges = [
        (inputs[0], sep[1]),
        (inputs[0], id_nodes[1]),
        (inputs[0], avg[1]),
        (inputs[0], avg[2]),
        (inputs[0], sep[3]),
        (inputs[0], sep[4]),
        (inputs[1], sep[0]),
        (inputs[1], id_nodes[0]),
        (inputs[1], avg[0]),
        (inputs[1], sep[2]),
        (sep[0], add_nodes_list[0]),
        (id_nodes[0], add_nodes_list[0]),
        (sep[1], add_nodes_list[1]),
        (sep[2], add_nodes_list[1]),
        (avg[0], add_nodes_list[2]),
        (id_nodes[1], add_nodes_list[2]),
        (avg[1], add_nodes_list[3]),
        (avg[2], add_nodes_list[3]),
        (sep[3], add_nodes_list[4]),
        (sep[4], add_nodes_list[4]),
    ]
    add_edges(g, edges)

    for add_node in add_nodes_list:
        g.add_edge(add_node, concat[0])

    assert len(sinks(g)) == 1
    assert len(sources(g)) == 2
    assert nx.is_directed_acyclic_graph(g)

    return g, inputs[0], inputs[1]


def make_reduction_taso_nasnet_cell() -> tuple[nx.DiGraph, int, int]:
    g = nx.DiGraph()

    inputs = add_nodes(g, 2)
    sep = add_nodes(g, 5)
    id_nodes = add_nodes(g, 1)
    avg = add_nodes(g, 2)
    max_pool = add_nodes(g, 2)
    add_nodes_list = add_nodes(g, 5)
    concat = add_nodes(g, 1)

    edges = [
        (inputs[0], sep[0]),
        (inputs[0], sep[2]),
        (inputs[0], sep[3]),
        (inputs[1], max_pool[1]),
        (inputs[1], sep[1]),
        (inputs[1], max_pool[0]),
        (inputs[1], avg[0]),
        (sep[0], add_nodes_list[0]),
        (sep[1], add_nodes_list[0]),
        (max_pool[0], add_nodes_list[1]),
        (sep[2], add_nodes_list[1]),
        (avg[0], add_nodes_list[2]),
        (sep[3], add_nodes_list[2]),
        (max_pool[1], add_nodes_list[3]),
        (sep[4], add_nodes_list[3]),
        (avg[1], add_nodes_list[4]),
        (id_nodes[0], add_nodes_list[4]),
        (add_nodes_list[0], sep[4]),
        (add_nodes_list[0], avg[1]),
        (add_nodes_list[1], id_nodes[0]),
    ]
    add_edges(g, edges)

    for i in range(2, 5):
        g.add_edge(add_nodes_list[i], concat[0])

    assert len(sinks(g)) == 1
    assert len(sources(g)) == 2
    assert nx.is_directed_acyclic_graph(g)

    return g, inputs[0], inputs[1]


def make_taso_nasnet_a(num_reduction_cells: int = 2, N: int = 6) -> nx.DiGraph:
    g = nx.DiGraph()
    input_node = 0
    g.add_node(input_node)

    outputting: deque[PureNode] = deque([input_node, input_node, input_node])
    inputting: deque[PureNode] = deque()

    num_cells = num_reduction_cells + N * (num_reduction_cells + 1)

    for i in range(num_cells):
        if i % (N + 1) == N:
            cell, earlier_input, later_input = make_reduction_taso_nasnet_cell()
        else:
            cell, earlier_input, later_input = make_normal_taso_nasnet_cell()

        cell_output = get_only(sinks(cell))

        offset = g.number_of_nodes()
        mapping = {n: n + offset for n in cell.nodes()}
        cell = nx.relabel_nodes(cell, mapping)
        earlier_input = mapping[earlier_input]
        later_input = mapping[later_input]
        cell_output = mapping[cell_output]

        g.add_nodes_from(cell.nodes())
        g.add_edges_from(cell.edges())

        outputting.append(cell_output)
        outputting.append(cell_output)
        inputting.append(earlier_input)
        inputting.append(later_input)

        for _ in range(2):
            src = outputting.popleft()
            dst = inputting.popleft()
            g.add_edge(src, dst)

        assert len(inputting) == 0
        assert len(outputting) == 3
    assert is_2_terminal_dag(g)
    return g
