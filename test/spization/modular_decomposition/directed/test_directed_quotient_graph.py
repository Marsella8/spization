import networkx as nx

from spization.modular_decomposition import (
    transitively_closed_dag_quotient_graph,
)
from spization.modular_decomposition.directed.directed_quotient_graph import (
    are_equivalent,
)


def test_transitively_closed_dag_quotient_graph_single_node():
    G = nx.DiGraph()
    G.add_node(1)
    result = transitively_closed_dag_quotient_graph(G)

    def make_correct():
        correct = nx.DiGraph()
        correct.add_node(1)
        return correct

    correct = make_correct()
    assert are_equivalent(result, correct)


def test_transitively_closed_dag_quotient_graph_parallel():
    G = nx.DiGraph()
    G.add_nodes_from([1, 2, 3])
    G = nx.transitive_closure(G)

    result = transitively_closed_dag_quotient_graph(G)

    def make_correct():
        correct = nx.DiGraph()
        n1, n2, n3 = nx.DiGraph(), nx.DiGraph(), nx.DiGraph()
        n1.add_node(1)
        n2.add_node(2)
        n3.add_node(3)
        correct.add_nodes_from((n1, n2, n3))
        return correct

    correct = make_correct()
    assert are_equivalent(result, correct)


def test_transitively_closed_dag_quotient_graph_series():
    G = nx.DiGraph([(1, 2), (2, 3)])
    G = nx.transitive_closure(G)

    result = transitively_closed_dag_quotient_graph(G)

    def make_correct():
        correct = nx.DiGraph()
        n1, n2, n3 = nx.DiGraph(), nx.DiGraph(), nx.DiGraph()
        n1.add_node(1)
        n2.add_node(2)
        n3.add_node(3)
        correct.add_edges_from([(n1, n2), (n2, n3)])
        return correct

    correct = make_correct()
    assert are_equivalent(result, correct)


def test_transitively_closed_dag_quotient_graph_prime():
    G = nx.DiGraph([(1, 3), (1, 4), (2, 4)])
    G = nx.transitive_closure(G)

    result = transitively_closed_dag_quotient_graph(G)

    def make_correct():
        n1, n2, n3, n4 = nx.DiGraph(), nx.DiGraph(), nx.DiGraph(), nx.DiGraph()
        n1.add_node(1)
        n2.add_node(2)
        n3.add_node(3)
        n4.add_node(4)
        correct = nx.DiGraph([(n1, n3), (n1, n4), (n2, n4)])
        return correct

    correct = make_correct()
    assert are_equivalent(result, correct)


def test_transitively_closed_dag_quotient_graph_complex():
    G = nx.DiGraph(
        [
            (1, 3),
            (1, 4),
            (1, 5),
            (1, 6),  # 1 connects to everything after
            (2, 3),
            (2, 4),
            (2, 5),
            (2, 6),  # 2 connects to everything after
            (3, 4),
            (3, 5),
            (3, 6),  # 3 connects to 4, 5, 6
            (4, 5),
            (4, 6),  # 4 connects to 5, 6
        ]
    )
    ...
