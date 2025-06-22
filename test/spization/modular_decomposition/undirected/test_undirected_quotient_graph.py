import networkx as nx

from spization.modular_decomposition import (
    undirected_quotient_graph,
)
from spization.modular_decomposition.undirected.undirected_quotient_graph import (
    are_equivalent,
)


def test_undirected_quotient_graph_single_node():
    G = nx.Graph()
    G.add_node(1)
    result = undirected_quotient_graph(G)

    def make_correct():
        correct = nx.Graph()
        correct.add_node(1)
        return correct

    correct = make_correct()
    assert are_equivalent(result, correct)


def test_undirected_quotient_graph_parallel():
    G = nx.Graph()
    G.add_nodes_from([1, 2, 3])

    result = undirected_quotient_graph(G)

    def make_correct():
        correct = nx.Graph()
        n1, n2, n3 = nx.Graph(), nx.Graph(), nx.Graph()
        n1.add_node(1)
        n2.add_node(2)
        n3.add_node(3)
        correct.add_nodes_from((n1, n2, n3))
        return correct

    correct = make_correct()
    assert are_equivalent(result, correct)


def test_undirected_quotient_graph_series():
    G = nx.Graph([(1, 2), (1, 3), (2, 3)])

    result = undirected_quotient_graph(G)

    def make_correct():
        correct = nx.Graph()
        n1, n2, n3 = nx.Graph(), nx.Graph(), nx.Graph()
        n1.add_node(1)
        n2.add_node(2)
        n3.add_node(3)
        correct.add_edges_from([(n1, n2), (n2, n3)])
        return correct

    correct = make_correct()
    assert are_equivalent(result, correct)


def test_undirected_quotient_graph_prime():
    G = nx.Graph([(1, 3), (1, 4), (2, 4)])

    result = undirected_quotient_graph(G)

    def make_correct():
        n1, n2, n3, n4 = nx.Graph(), nx.Graph(), nx.Graph(), nx.Graph()
        n1.add_node(1)
        n2.add_node(2)
        n3.add_node(3)
        n4.add_node(4)
        correct = nx.Graph([(n1, n3), (n1, n4), (n2, n4)])
        return correct

    correct = make_correct()
    assert are_equivalent(result, correct)


# def test_undirected_quotient_graph_complex():
#     G = nx.Graph(((1, 3), (1, 4), (1, 5), (1, 6), (2, 3), (2, 4), (2, 5), (2, 6), (3, 4), (5, 6)))
#     pass
