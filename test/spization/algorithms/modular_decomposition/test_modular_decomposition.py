from networkx import DiGraph, Graph

from spization.algorithms.modular_decomposition.objects import (
    MDLeaf,
    MDParallel,
    MDPrime,
    MDSeries,
    transitive_dag_modular_decomposition,
    undirected_modular_decomposition,
)


def test_modular_decomposition_single_node():
    G = DiGraph()
    G.add_node(1)
    expected = MDLeaf(1)
    result = transitive_dag_modular_decomposition(G)
    print(expected.node, result.node)
    assert expected == result


def test_modular_decomposition_parallel():
    G = DiGraph()
    G.add_nodes_from([1, 2, 3])
    expected = MDParallel(frozenset({MDLeaf(1), MDLeaf(2), MDLeaf(3)}))
    result = transitive_dag_modular_decomposition(G)
    assert expected == result


def test_modular_decomposition_series():
    G = DiGraph(((1, 2), (2, 3), (1, 3)))
    expected = MDSeries((MDLeaf(1), MDLeaf(2), MDLeaf(3)))
    result = transitive_dag_modular_decomposition(G)
    assert expected == result


def test_modular_decomposition_composed_series_parallel():
    G = DiGraph(
        (
            (1, 2),
            (1, 3),
            (1, 4),
            (1, 5),
            (1, 6),
            (2, 4),
            (2, 6),
            (3, 4),
            (3, 6),
            (4, 6),
            (5, 6),
        )
    )
    expected = MDSeries(
        (
            MDLeaf(1),
            MDParallel(
                    {
                        MDSeries(
                            (
                                MDParallel({MDLeaf(2), MDLeaf(3)}),
                                MDLeaf(4),
                            )
                        ),
                        MDLeaf(5),
                    }
            ),
            MDLeaf(6),
        )
    )

    result = transitive_dag_modular_decomposition(G)
    assert expected == result


def test_undirected_modular_decomposition_complex_graph():
    G = Graph(
        (
            (1, 3),
            (1, 4),
            (1, 5),
            (1, 6),
            (2, 3),
            (2, 4),
            (2, 5),
            (2, 6),
            (3, 4),
            (4, 5),
            (5, 6),
        )
    )

    result = undirected_modular_decomposition(G)
    correct = MDSeries(
        (
            MDParallel((MDLeaf(1), MDLeaf(2))),
            MDPrime((MDLeaf(3), MDLeaf(4), MDLeaf(5), MDLeaf(6))),
        )
    )

    assert result == correct


def test_undirected_modular_decomposition_other_complex_graph():
    G = Graph(
        (
            (1, 2),
            (2, 3),
            (2, 4),
            (3, 4),
            (3, 5),
            (3, 6),
            (4, 5),
            (4, 6),
        )
    )

    result = undirected_modular_decomposition(G)
    correct = MDPrime(
        (
            MDLeaf(1),
            MDLeaf(2),
            MDSeries((MDLeaf(3), MDLeaf(4))),
            MDParallel((MDLeaf(5), MDLeaf(6))),
        )
    )
    print(result)

    assert result == correct


# TODO: change MDLead to just node
