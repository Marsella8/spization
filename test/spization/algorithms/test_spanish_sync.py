from networkx import DiGraph
import networkx as nx
from spization.algorithms import spanish_strata_sync


def test_spanish_strata_sync_simple():
    input = DiGraph([(1, 2), (1, 3), (2, 4), (2, 5), (3, 5), (4, 6), (5, 6)])
    correct = DiGraph([(1, 2), (1, 3), (2, 4), (2, 5), (3, 4), (3, 5), (4, 6), (5, 6)])

    result = spanish_strata_sync(input)
    assert nx.utils.graphs_equal(correct, result)


def test_spanish_strata_sync_simple_with_parallel_strand():
    input = DiGraph(
        [(1, 2), (1, 3), (2, 4), (2, 5), (3, 5), (4, 6), (5, 6), (1, 7), (7, 6)]
    )
    correct = DiGraph(
        [(1, 2), (1, 3), (2, 4), (2, 5), (3, 4), (3, 5), (4, 6), (5, 6), (1, 7), (7, 6)]
    )

    result = spanish_strata_sync(input)
    assert nx.utils.graphs_equal(correct, result)


def test_spanish_strata_sync_simple_with_appendage():
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
            (2, 4),
            (2, 5),
            (2, 8),
            (3, 4),
            (3, 5),
            (3, 8),
            (4, 6),
            (5, 6),
            (1, 7),
            (7, 6),
            (3, 8),
            (8, 6),
        ]
    )

    result = spanish_strata_sync(input)
    assert nx.utils.graphs_equal(correct, result)
