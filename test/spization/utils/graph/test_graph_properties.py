import networkx as nx

from spization import DupNode
from spization.utils.graph.properties import is_2_terminal_dag, is_compatible_graph


def test_is_2_terminal_dag_valid():
    g = nx.DiGraph()
    g.add_edges_from([(1, 2), (1, 3), (2, 4), (3, 4)])
    assert is_2_terminal_dag(g) is True


def test_is_2_terminal_dag_not_dag():
    g = nx.DiGraph()
    g.add_edges_from([(1, 2), (2, 3), (3, 1)])
    assert is_2_terminal_dag(g) is False


def test_is_2_terminal_dag_multiple_sources():
    g = nx.DiGraph()
    g.add_edges_from([(1, 3), (2, 3), (3, 4)])
    assert is_2_terminal_dag(g) is False


def test_is_2_terminal_dag_multiple_sinks():
    g = nx.DiGraph()
    g.add_edges_from([(1, 2), (1, 3), (2, 4)])
    assert is_2_terminal_dag(g) is False


def test_is_compatible_graph_valid():
    g = nx.DiGraph()
    g.add_nodes_from([1, 2, 3])
    assert is_compatible_graph(g) is True


def test_is_compatible_graph_invalid():
    g = nx.DiGraph()
    g.add_node(1)
    g.add_node(DupNode(2, 0))
    is_compatible_graph(g) is False
