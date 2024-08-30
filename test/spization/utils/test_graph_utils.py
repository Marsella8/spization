import networkx as nx
from spization.utils.graph_utils import (
    sources,
    sinks,
    is_2_terminal_dag,
    is_integer_graph,
)


def test_sources_basic():
    G = nx.DiGraph()
    G.add_edges_from([(1, 2), (1, 3), (2, 4), (3, 4)])
    result = sources(G)
    expected = {1}
    assert result == expected


def test_sources_multiple():
    G = nx.DiGraph()
    G.add_edges_from([(1, 3), (2, 3), (3, 4)])
    result = sources(G)
    expected = {1, 2}
    assert result == expected


def test_sources_no_sources():
    G = nx.DiGraph()
    G.add_edges_from([(1, 2), (2, 3), (3, 1)])
    result = sources(G)
    expected = set()
    assert result == expected


def test_sinks_basic():
    G = nx.DiGraph()
    G.add_edges_from([(1, 2), (1, 3), (2, 4), (3, 4)])
    result = sinks(G)
    expected = {4}
    assert result == expected


def test_sinks_multiple():
    G = nx.DiGraph()
    G.add_edges_from([(1, 2), (1, 3), (2, 4)])
    result = sinks(G)
    expected = {3, 4}
    assert result == expected


def test_sinks_no_sinks():
    G = nx.DiGraph()
    G.add_edges_from([(1, 2), (2, 3), (3, 1)])
    result = sinks(G)
    expected = set()
    assert result == expected


def test_is_2_terminal_dag_valid():
    G = nx.DiGraph()
    G.add_edges_from([(1, 2), (1, 3), (2, 4), (3, 4)])
    assert is_2_terminal_dag(G) is True


def test_is_2_terminal_dag_not_dag():
    G = nx.DiGraph()
    G.add_edges_from([(1, 2), (2, 3), (3, 1)])
    assert is_2_terminal_dag(G) is False


def test_is_2_terminal_dag_multiple_sources():
    G = nx.DiGraph()
    G.add_edges_from([(1, 3), (2, 3), (3, 4)])
    assert is_2_terminal_dag(G) is False


def test_is_2_terminal_dag_multiple_sinks():
    G = nx.DiGraph()
    G.add_edges_from([(1, 2), (1, 3), (2, 4)])
    assert is_2_terminal_dag(G) is False


def test_is_integer_graph_valid():
    G = nx.DiGraph()
    G.add_nodes_from([1, 2, 3, 4])
    assert is_integer_graph(G) is True


def test_is_integer_graph_invalid():
    G = nx.DiGraph()
    G.add_nodes_from([1, 2, "a", 4])
    is_integer_graph(G) is False
