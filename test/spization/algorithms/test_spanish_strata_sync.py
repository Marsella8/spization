from networkx import DiGraph
from testing_utils import graph_generator

from spization.algorithms import spanish_strata_sync
from spization.objects import Parallel, Serial
from spization.utils import dependencies_are_maintained


def test_spanish_strata_sync_6_diamond_with_cross_edge():
    input = DiGraph(((1, 2), (1, 3), (2, 4), (2, 5), (3, 5), (4, 6), (5, 6)))
    correct = Serial((1, Parallel((2, 3)), Parallel((4, 5)), 6))
    result = spanish_strata_sync(input)

    assert correct == result
    assert dependencies_are_maintained(input, result)


def test_spanish_strata_sync_6_diamond_with_cross_edge_and_parallel_strand():
    input = DiGraph(
        ((1, 2), (1, 3), (2, 4), (2, 5), (3, 5), (4, 6), (5, 6), (1, 7), (7, 6))
    )
    correct = Serial(
        (1, Parallel((7, Serial((Parallel((2, 3)), Parallel((4, 5)))))), 6)
    )
    result = spanish_strata_sync(input)

    assert correct == result
    assert dependencies_are_maintained(input, result)


def test_spanish_strata_sync_simple_with_appendage():
    input = DiGraph(
        (
            (1, 2),
            (1, 3),
            (2, 4),
            (2, 5),
            (3, 5),
            (4, 8),
            (5, 8),
            (1, 7),
            (7, 8),
            (3, 6),
            (6, 8),
        )
    )

    correct = Serial(
        (1, Parallel((Serial((Parallel((2, 3)), Parallel((4, 5, 6)))), 7)), 8)
    )
    result = spanish_strata_sync(input)
    assert correct == result
    assert dependencies_are_maintained(input, result)


def test_spanish_strata_sync_transitive_edges():
    input = DiGraph(
        ((1, 2), (1, 3), (1, 6), (2, 4), (2, 5), (2, 6), (3, 5), (3, 6), (4, 6), (5, 6))
    )

    result = spanish_strata_sync(input)
    correct = Serial((1, Parallel((2, 3)), Parallel((4, 5)), 6))
    assert dependencies_are_maintained(input, result)
    assert correct == result


def test_spanish_strata_sync_graph_from_paper():
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
            (11, 10),  # this edge should be present, bug in the paper,
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

    result = spanish_strata_sync(input)
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
    assert correct == result
    assert dependencies_are_maintained(input, result)


# TODO check also without the funky bug edge


def test_correctness():
    for input in graph_generator():
        result = spanish_strata_sync(input)
        assert dependencies_are_maintained(input, result)


# TODO: move everything to use get_series_parallel_decomposition
# TODO does adding transitive reduction at each step affect
