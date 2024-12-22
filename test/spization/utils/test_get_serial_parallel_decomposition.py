from networkx import DiGraph

from spization.objects import Parallel, PureNode, Serial
from spization.utils import get_serial_parallel_decomposition


def test_get_serial_parallel_decomposition_single_node():
    g = DiGraph()
    g.add_node(0)
    result = get_serial_parallel_decomposition(g)
    correct = PureNode(0)
    assert correct == result


def test_get_serial_parallel_decomposition_parallel():
    g = DiGraph()
    g.add_nodes_from((0, 1))
    result = get_serial_parallel_decomposition(g)
    correct = Parallel((0, 1))
    assert correct == result


def test_get_serial_parallel_decomposition_serial():
    g = DiGraph(((0, 1),))
    result = get_serial_parallel_decomposition(g)
    correct = Serial((0, 1))
    assert correct == result


def test_get_serial_parallel_decomposition_composite():
    g = DiGraph(((0, 1), (0, 2)))
    result = get_serial_parallel_decomposition(g)
    correct = Serial((0, Parallel((1, 2))))
    assert result == correct


def test_get_serial_parallel_decomposition_diamond_graph():
    g = DiGraph(((0, 1), (0, 2), (1, 3), (2, 4), (3, 5), (4, 5)))
    result = get_serial_parallel_decomposition(g)
    correct = Serial((0, Parallel((Serial((1, 3)), Serial((2, 4)))), 5))
    assert result == correct


def test_get_serial_parallel_decomposition_all_to_all_connection():
    g = DiGraph(((0, 2), (0, 3), (1, 2), (1, 3)))
    result = get_serial_parallel_decomposition(g)
    correct = Serial((Parallel((0, 1)), Parallel((2, 3))))
    assert result == correct


def test_get_serial_parallel_decomposition_non_sp_graph():
    g = DiGraph(((0, 2), (1, 2), (1, 3)))
    result = get_serial_parallel_decomposition(g)
    correct = None
    assert result == correct


def test_get_serial_parallel_decomposition_requires_transitive_reduction():
    g = DiGraph(((0, 1), (0, 2), (1, 2), (1, 3), (2, 3)))
    result = get_serial_parallel_decomposition(g)
    correct = Serial((0, 1, 2, 3))
    assert result == correct
