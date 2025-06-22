import random

from networkx import DiGraph

from benchmarking.graphs import make_taso_nasnet_a
from spization.algorithms import flexible_sync
from spization.objects import Node, Parallel, PureNode, Serial
from spization.utils import dependencies_are_maintained
from test.spization.testing_utils import graph_generator

random.seed(0)


def random_cost_map(g: DiGraph, choose_from=(1, 3, 5)) -> dict[Node, float | int]:
    return {node: random.choice(choose_from) for node in g.nodes()}


def constant_cost_map(g: DiGraph) -> dict[Node, int]:
    return {node: 1 for node in g.nodes()}


def truly_random_cost_map(g: DiGraph) -> dict[Node, float]:
    return {node: random.random() for node in g.nodes()}


def test_flexible_sync_single_node():
    input = DiGraph()
    input.add_node(PureNode(0))
    cost_map = truly_random_cost_map(input)

    result = flexible_sync(input, cost_map)
    correct = PureNode(0)

    assert result == correct
    assert dependencies_are_maintained(input, result)


def test_flexible_sync_tri_node_graph():
    for _ in range(10):
        input = DiGraph(((1, 2), (1, 3)))
        cost_map = truly_random_cost_map(input)

        result = flexible_sync(input, cost_map)
        correct = Serial((1, Parallel((2, 3))))

        assert result == correct
        assert dependencies_are_maintained(input, result)


def test_flexible_sync_serial():
    for _ in range(10):
        input = DiGraph(((1, 2), (2, 3), (3, 4)))
        cost_map = truly_random_cost_map(input)

        result = flexible_sync(input, cost_map)
        correct = Serial((1, 2, 3, 4))

        assert result == correct
        assert dependencies_are_maintained(input, result)


def test_flexible_sync_6_node_diamond_graph_cost_map_v1():
    input = DiGraph([(1, 2), (1, 3), (2, 4), (2, 5), (3, 5)])
    cost_map = constant_cost_map(input)

    result = flexible_sync(input, cost_map)
    correct = Serial((1, Parallel((2, 3)), Parallel((4, 5))))

    assert correct == result
    assert dependencies_are_maintained(input, result)


def test_flexible_sync_6_node_diamond_graph_cost_map_v2():
    input = DiGraph([(1, 2), (1, 3), (2, 4), (2, 5), (3, 5)])
    cost_map = constant_cost_map(input)
    cost_map[4] = 1000
    cost_map[3] = 10
    result = flexible_sync(input, cost_map)
    correct = Serial((1, 2, Parallel((Serial((3, 5)), 4))))

    assert correct == result
    assert dependencies_are_maintained(input, result)


def test_flexible_sync_6_node_diamond_graph_cost_map_v3():
    input = DiGraph([(1, 2), (1, 3), (2, 4), (2, 5), (3, 5)])
    cost_map = constant_cost_map(input)
    cost_map[4] = 1000
    cost_map[3] = 1000

    result = flexible_sync(input, cost_map)
    correct = Serial((1, Parallel((Serial((2, 4)), 3)), 5))

    assert correct == result
    assert dependencies_are_maintained(input, result)


def test_flexible_sync_with_parallel_strand():
    input = DiGraph(((1, 2), (1, 3), (2, 4), (3, 5), (4, 6), (5, 7), (6, 8), (7, 8)))
    cost_map = constant_cost_map(input)

    result = flexible_sync(input, cost_map)
    correct = Serial((1, Parallel((Serial((2, 4, 6)), Serial((3, 5, 7)))), 8))

    assert result == correct
    assert dependencies_are_maintained(input, result)


def test_spanish_strata_sync_simple_with_parallel_strand():
    input = DiGraph(
        ((1, 2), (1, 3), (2, 4), (2, 5), (3, 5), (4, 7), (5, 7), (1, 6), (6, 7))
    )
    cost_map = constant_cost_map(input)
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

    correct = Serial(
        (1, Parallel((7, Serial((Parallel((2, 3)), Parallel((4, 5, 8)))))), 6)
    )
    cost_map = constant_cost_map(input)

    result = flexible_sync(input, cost_map)
    assert correct == result
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

    correct = Serial(
        (1, Parallel((7, Serial((3, Parallel((8, Serial((2, Parallel((4, 5)))))))))), 6)
    )

    cost_map = constant_cost_map(input)
    cost_map[2] = 100
    cost_map[8] = 100

    result = flexible_sync(input, cost_map)
    assert correct == result
    assert dependencies_are_maintained(input, result)


def test_flexible_sync_transitive_edge():
    input = DiGraph(
        ((1, 2), (1, 3), (2, 4), (2, 5), (3, 11), (4, 12), (5, 11), (11, 12))
    )
    cost_map = constant_cost_map(input)
    cost_map[4] = 10
    cost_map[11] = 10
    correct = Serial((1, Parallel((Serial((2, 5)), 3)), Parallel((4, 11)), 12))
    result = flexible_sync(input, cost_map)
    assert correct == result
    assert dependencies_are_maintained(input, result)


def test_flexible_sync_graph_from_paper_constant_map():
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
            (11, 10),
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

    cost_map = constant_cost_map(input)
    result = flexible_sync(input, cost_map)
    correct = Serial(
        (
            1,
            Parallel(
                (
                    Serial((2, Parallel((4, 5)))),
                    Serial((3, Parallel((12, 13)))),
                )
            ),
            Parallel(
                (
                    Serial((Parallel((11, 6, 7, 8)), Parallel((9, 10)))),
                    Serial((Parallel((14, 15)), 16)),
                )
            ),
            17,
            18,
        )
    )
    assert dependencies_are_maintained(input, result)
    assert correct == result


def test_flexible_sync_graph_from_paper_non_constant_map():
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
    cost_map = constant_cost_map(input)
    result = flexible_sync(input, cost_map)
    assert dependencies_are_maintained(input, result)


def test_failing():
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
    cost_map = {
        1: 1,
        2: 3,
        3: 5,
        4: 3,
        5: 5,
        6: 3,
        7: 5,
        8: 1,
        9: 5,
        10: 5,
        11: 3,
        12: 3,
        13: 1,
        14: 3,
        15: 3,
        16: 1,
        17: 1,
        18: 1,
    }

    result = flexible_sync(input, cost_map)
    assert result is not None
    assert dependencies_are_maintained(input, result)


def test_correctness():
    for input in graph_generator():
        cost_map = truly_random_cost_map(input)
        result = flexible_sync(input, cost_map)
        assert dependencies_are_maintained(input, result)


def test_taso_nasnet():
    input = make_taso_nasnet_a(2, 6)
    cost_map = truly_random_cost_map(input)
    result = flexible_sync(input, cost_map)
    assert result is not None
    assert dependencies_are_maintained(input, result)
