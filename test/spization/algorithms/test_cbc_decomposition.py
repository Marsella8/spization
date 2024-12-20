import networkx as nx
from spization.utils import cbc_decomposition, BipartiteComponent

def test_six_node_diamond_graph():
    g = nx.DiGraph()
    nodes = list(range(6))
    g.add_edges_from([(0, 1), (0, 2), (1, 3), (2, 4), (3, 5), (4, 5)])

    result = cbc_decomposition(g)
    correct = {
        BipartiteComponent(frozenset({0}), frozenset({1, 2})),
        BipartiteComponent(frozenset({1}), frozenset({3})),
        BipartiteComponent(frozenset({2}), frozenset({4})),
        BipartiteComponent(frozenset({3, 4}), frozenset({5})),
    }
    assert result == correct


def test_graph_without_edges():
    g = nx.DiGraph()
    g.add_nodes_from(range(4))

    result = cbc_decomposition(g)
    assert result == set()


def test_irreducible_non_cbc_graph():
    g = nx.DiGraph()
    nodes = list(range(4))
    g.add_edges_from([(0, 2), (1, 2), (1, 3)])

    result = cbc_decomposition(g)
    assert result is None
