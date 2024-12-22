import networkx as nx

from spization.__internals.graph import sinks, sources


def test_sources_basic():
    g = nx.DiGraph()
    g.add_edges_from([(1, 2), (1, 3), (2, 4), (3, 4)])
    result = sources(g)
    correct = {1}
    assert result == correct


def test_sources_multiple():
    g = nx.DiGraph()
    g.add_edges_from([(1, 3), (2, 3), (3, 4)])
    result = sources(g)
    correct = {1, 2}
    assert result == correct


def test_sources_no_sources():
    g = nx.DiGraph()
    g.add_edges_from([(1, 2), (2, 3), (3, 1)])
    result = sources(g)
    correct = set()
    assert result == correct


def test_sinks_basic():
    g = nx.DiGraph()
    g.add_edges_from([(1, 2), (1, 3), (2, 4), (3, 4)])
    result = sinks(g)
    correct = {4}
    assert result == correct


def test_sinks_multiple():
    g = nx.DiGraph()
    g.add_edges_from([(1, 2), (1, 3), (2, 4)])
    result = sinks(g)
    correct = {3, 4}
    assert result == correct


def test_sinks_no_sinks():
    g = nx.DiGraph()
    g.add_edges_from([(1, 2), (2, 3), (3, 1)])
    result = sinks(g)
    correct = set()
    assert result == correct
