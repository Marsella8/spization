import random

from networkx import DiGraph

from spization.algorithms import flexible_sync
from spization.objects import Node
from spization.utils import dependencies_are_maintained


def random_cost_map(nodes: set[Node]) -> dict[Node, float]:
    return {node: random.choice([1, 3, 5]) for node in nodes}


def constant_cost_map(nodes: set[Node]) -> dict[Node, float]:
    return {node: 1 for node in nodes}


# TODO put in internals graphs
def print_edges(G):
    dot_rep = "digraph G {\n"

    for u, v in G.edges():
        dot_rep += f'\t"{u}" -> "{v}";\n'

    dot_rep += "}\n"

    print(dot_rep)


def test_flexible_sync_linear():
    input = DiGraph([(1, 2), (2, 3), (3, 4)])
    cost_map = constant_cost_map({1, 2, 3, 4})

    result = flexible_sync(input, cost_map)
    correct = Serial((1, 2, 3, 4))

    assert result == correct
    assert dependencies_are_maintained(input, result)


def test_flexible_sync_6_node_diamond_graph():
    input = DiGraph([(1, 2), (1, 3), (2, 4), (2, 5), (3, 5), (4, 6), (5, 6)])
    cost_map = constant_cost_map(input.nodes)
    cost_map[3] = 100
    cost_map[4] = 100

    result = flexible_sync(input, cost_map)
    correct = Serial((1, Parallel((Serial((2, 4)), 3)), 5, 6))

    assert correct == result
    assert dependencies_are_maintained(input, result)


def test_flexible_sync_with_parallel_strand():
    input = DiGraph(((1, 2), (1, 3), (2, 4), (3, 5), (4, 6), (5, 7), (6, 8), (7, 8)))
    cost_map = constant_cost_map(input.nodes)

    result = flexible_sync(input, cost_map)
    correct = Serial((1, Parallel((Serial((2, 4, 6)), Serial((3, 5, 7)))), 8))

    assert result == correct
    assert dependencies_are_maintained(input, result)


def test_spanish_strata_sync_simple_with_parallel_strand():
    input = DiGraph(
        ((1, 2), (1, 3), (2, 4), (2, 5), (3, 5), (4, 7), (5, 7), (1, 6), (6, 7))
    )
    cost_map = constant_cost_map(input.nodes)
    cost_map[3] = 100
    cost_map[4] = 100

    result = flexible_sync(input, cost_map)
    correct = Serial((1, Parallel((Serial((Parallel((Serial((2, 4)), 3)), 5)), 6)), 7))
    assert result == correct
    assert dependencies_are_maintained(input, result)


def test_flexible_sync_with_appendage():
    input = DiGraph(
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
    cost_map = {n: 1 for n in input.nodes}

    result = flexible_sync(input, cost_map)
    # assert nx.utils.graphs_equal(correct, result)
    assert dependencies_are_maintained(input, result)


def test_flexible_sync_with_appendage_weighted():
    input = DiGraph(
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
    cost_map = {n: 1 for n in input.nodes}
    cost_map[2] = 100
    cost_map[8] = 100

    result = flexible_sync(input, cost_map)
    # assert nx.utils.graphs_equal(correct, result)
    assert dependencies_are_maintained(input, result)


def test_flexible_sync_transitive_edge():
    input = DiGraph(
        ((1, 2), (1, 3), (2, 4), (2, 5), (3, 11), (4, 12), (5, 11), (11, 12))
    )
    cost_map = {1: 1, 2: 1, 3: 1, 4: 10, 5: 1, 11: 10, 12: 1}
    correct = DiGraph(
        [(1, 2), (1, 3), (2, 5), (3, 11), (3, 4), (5, 11), (5, 4), (4, 12), (11, 12)]
    )
    result = flexible_sync(input, cost_map)
    assert dependencies_are_maintained(input, result)


def test_flexible_sync_graph_from_paper():
    input = DiGraph(
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
    cost_map = random_cost_map(set(input.nodes))

    result = flexible_sync(input, cost_map)
    assert dependencies_are_maintained(input, result)


# def test_correctness():
#     for input in graph_generator():
#         cost_map = random_cost_map(set(input.nodes))
#         result = flexible_sync(input, cost_map)
#         assert dependencies_are_maintained(input, result)

# TODO do a shit ton of property testing.
