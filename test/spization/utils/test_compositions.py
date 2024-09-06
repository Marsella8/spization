import networkx as nx
from networkx import DiGraph

from spization.objects import Parallel, Serial
from spization.utils import (
    graph_parallel_composition,
    graph_serial_composition,
    sp_parallel_composition,
    sp_serial_composition,
)


def test_parallel_composition_basic():
    result = sp_parallel_composition((1, 2, 3))
    expected = Parallel((1, 2, 3))
    assert result == expected


def test_parallel_composition_nested():
    result = sp_parallel_composition((Parallel((1, 2)), Serial((3, 4)), 5))
    expected = Parallel((1, 2, 5, Serial((3, 4))))
    assert result == expected


def test_serial_composition_basic():
    result = sp_serial_composition((1, 2, 3))
    expected = Serial((1, 2, 3))
    assert result == expected


def test_serial_composition_nested():
    result = sp_serial_composition((Serial((1, 2)), Parallel((3, 4)), 5))
    expected = Serial((1, 2, Parallel((3, 4)), 5))
    assert result == expected


def test_parallel_composition_empty():
    result = sp_parallel_composition((Parallel(()),))
    expected = Parallel(())
    assert result == expected


def test_serial_composition_empty():
    result = sp_serial_composition((Serial(()),))
    expected = Serial(())
    assert result == expected


def test_serial_graph_composition():
    g1 = DiGraph(((0, 1), (0, 2)))
    g2 = DiGraph(((3, 4), (3, 5), (5, 6), (4, 6)))
    result = graph_serial_composition(g1, g2)
    correct = DiGraph(((0, 1), (0, 2), (3, 4), (3, 5), (5, 6), (4, 6), (2, 3), (1, 3)))
    assert nx.utils.graphs_equal(result, correct)


def test_parallel_graph_composition():
    g1 = DiGraph(((0, 1), (0, 2)))
    g2 = DiGraph(((3, 4), (3, 5), (5, 6), (4, 6)))
    result = graph_parallel_composition((g1, g2))
    correct = DiGraph(((0, 1), (0, 2), (3, 4), (3, 5), (5, 6), (4, 6)))
    assert nx.utils.graphs_equal(result, correct)
