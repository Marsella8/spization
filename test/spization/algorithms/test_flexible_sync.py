import random
from typing import Dict

import networkx as nx
from networkx import DiGraph
from testing_utils import graph_generator

from spization.algorithms import flexible_sync
from spization.objects import Node
from spization.utils import is_valid_sp


def random_cost_map(nodes: set[Node]) -> Dict[Node, float]:
    return {node: random.choice([1, 100]) for node in nodes}


def print_edges(G):
    dot_rep = "digraph G {\n"

    for u, v in G.edges():
        dot_rep += f'\t"{u}" -> "{v}";\n'

    dot_rep += "}\n"

    print(dot_rep)


def test_flexible_sync_linear():
    input_graph = DiGraph([(1, 2), (2, 3), (3, 4)])
    cost_map = random_cost_map(set(input_graph.nodes))

    result = flexible_sync(input_graph, cost_map)
    assert is_valid_sp(input_graph, result)
    assert set(result.edges) == {(1, 2), (2, 3), (3, 4)}


def test_flexible_sync_simple():
    input_graph = DiGraph([(1, 2), (1, 3), (2, 4), (2, 5), (3, 5), (4, 6), (5, 6)])
    cost_map = {1: 1, 2: 1, 3: 10, 4: 10, 5: 1, 6: 1}
    result = flexible_sync(input_graph, cost_map)
    print(result.edges)
    assert is_valid_sp(input_graph, result)
    assert set(result.edges) == {(1, 2), (1, 3), (2, 4), (3, 5), (4, 5), (5, 6)}


def test_flexible_sync_with_parallel_strand():
    input_graph = DiGraph(
        [(1, 2), (1, 3), (2, 4), (3, 5), (4, 6), (5, 7), (6, 8), (7, 8)]
    )
    cost_map = {x: 1 for x in input_graph.nodes}

    result = flexible_sync(input_graph, cost_map)
    assert is_valid_sp(input_graph, result)
    assert set(result.edges) == {
        (1, 2),
        (1, 3),
        (2, 4),
        (3, 5),
        (4, 6),
        (5, 7),
        (6, 8),
        (7, 8),
    }


def test_spanish_strata_sync_simple_with_parallel_strand():
    input = DiGraph(
        [(1, 2), (1, 3), (2, 4), (2, 5), (3, 5), (4, 6), (5, 6), (1, 7), (7, 6)]
    )
    correct = DiGraph([(1, 2), (1, 3), (2, 4), (4, 5), (3, 5), (5, 6), (1, 7), (7, 6)])
    cost_map = {x: 1 for x in input.nodes}
    cost_map[3] = 100
    cost_map[4] = 100

    result = flexible_sync(input, cost_map)
    assert nx.utils.graphs_equal(correct, result)
    assert is_valid_sp(input, result)


def test_flexible_sync_with_appendage():
    input_graph = DiGraph(
        [
            (1, 2),
            (1, 3),
            (2, 4),
            (2, 5),
            (3, 5),
            (4, 6),
            (5, 6),
            (1, 7),
            (7, 6),
            (3, 8),
            (8, 6),
        ]
    )
    correct = DiGraph(
        [
            (1, 2),
            (1, 3),
            (1, 7),
            (2, 8),
            (2, 4),
            (2, 5),
            (3, 8),
            (3, 4),
            (3, 5),
            (7, 6),
            (4, 6),
            (5, 6),
            (8, 6),
        ]
    )
    cost_map = {n: 1 for n in input_graph.nodes}

    result = flexible_sync(input_graph, cost_map)
    assert nx.utils.graphs_equal(correct, result)
    assert is_valid_sp(input_graph, result)


def test_flexible_sync_with_appendage_weighted():
    input_graph = DiGraph(
        [
            (1, 2),
            (1, 3),
            (2, 4),
            (2, 5),
            (3, 5),
            (4, 6),
            (5, 6),
            (1, 7),
            (7, 6),
            (3, 8),
            (8, 6),
        ]
    )
    correct = DiGraph(
        [(1, 3), (1, 7), (2, 4), (2, 5), (3, 2), (3, 8), (4, 6), (5, 6), (8, 6), (7, 6)]
    )
    cost_map = {n: 1 for n in input_graph.nodes}
    cost_map[2] = 100
    cost_map[8] = 100

    result = flexible_sync(input_graph, cost_map)
    assert nx.utils.graphs_equal(correct, result)
    assert is_valid_sp(input_graph, result)


def test_flexible_sync_transitive_edge():
    input_graph = DiGraph(
        ((1, 2), (1, 3), (2, 4), (2, 5), (3, 11), (4, 12), (5, 11), (11, 12))
    )
    cost_map = {1: 1, 2: 1, 3: 1, 4: 10, 5: 1, 11: 10, 12: 1}
    correct = DiGraph(
        [(1, 2), (1, 3), (2, 5), (3, 11), (3, 4), (5, 11), (5, 4), (4, 12), (11, 12)]
    )
    result = flexible_sync(input_graph, cost_map)
    assert is_valid_sp(input_graph, result)
    assert nx.utils.graphs_equal(correct, result)


def test_flexible_sync_graph_from_paper():
    input_graph = DiGraph(
        (
            (1, 2),
            (1, 3),
            (2, 4),
            (2, 5),
            (3, 11),
            (3, 12),
            (3, 13),
            (4, 6),
            (4, 7),
            (5, 7),
            (5, 8),
            (5, 11),
            (6, 9),
            (7, 9),
            (7, 10),
            (8, 9),
            (9, 18),
            (10, 18),
            (11, 17),
            (12, 17),
            (13, 14),
            (13, 15),
            (14, 16),
            (15, 16),
            (16, 17),
            (17, 18),
        )
    )
    cost_map = random_cost_map(set(input_graph.nodes))

    result = flexible_sync(input_graph, cost_map)
    assert is_valid_sp(input_graph, result)


def test_correctness():
    for input in graph_generator():
        cost_map = random_cost_map(set(input.nodes))
        result = flexible_sync(input, cost_map)
        assert is_valid_sp(input, result)
