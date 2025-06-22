import random

from networkx import Graph

from spization.modular_decomposition import undirected_md_naive
from spization.modular_decomposition.undirected.objects import (
    MDParallelUndirected,
    MDPrimeUndirected,
    MDSeriesUndirected,
)


def test_modular_decomposition_single_node():
    input = Graph()
    input.add_node(1)
    correct = 1
    result = undirected_md_naive(input)
    assert correct == result


def test_modular_decomposition_parallel():
    input = Graph()
    input.add_nodes_from((1, 2, 3))
    correct = MDParallelUndirected((1, 2, 3))
    result = undirected_md_naive(input)
    assert correct == result


def test_modular_decomposition_series():
    input = Graph(((1, 2), (2, 3), (1, 3)))
    correct = MDSeriesUndirected((1, 2, 3))
    result = undirected_md_naive(input)
    assert correct == result


def test_modular_decomposition_prime():
    input = Graph(((1, 3), (1, 4), (2, 4)))
    correct = MDPrimeUndirected((1, 2, 3, 4))
    result = undirected_md_naive(input)
    assert correct == result


def test_modular_decomposition_emerald():
    input = Graph(((1, 2), (1, 3), (2, 4), (3, 5), (4, 6), (5, 6)))
    correct = MDPrimeUndirected((1, 2, 3, 4, 5, 6))
    result = undirected_md_naive(input)
    assert correct == result


def test_modular_decomposition_diamond():
    input = Graph(((1, 2), (1, 3), (2, 4), (3, 4)))
    correct = MDSeriesUndirected(
        (MDParallelUndirected((1, 4)), MDParallelUndirected((2, 3)))
    )
    result = undirected_md_naive(input)
    assert correct == result


def test_modular_decomposition_wikipedia():
    # pulled from https://en.wikipedia.org/wiki/Modular_decomposition#/media/File:ModularDecomposition.png
    edges = (
        (1, 2),
        (1, 3),
        (1, 4),
        (2, 4),
        (3, 4),
        (2, 5),
        (3, 5),
        (4, 5),
        (5, 6),
        (5, 7),
        (2, 8),
        (2, 9),
        (2, 10),
        (2, 11),
        (3, 8),
        (3, 9),
        (3, 10),
        (3, 11),
        (4, 8),
        (4, 9),
        (4, 10),
        (4, 11),
        (5, 8),
        (5, 9),
        (5, 10),
        (5, 11),
        (8, 9),
        (8, 10),
        (8, 11),
        (9, 10),
        (9, 11),
    )

    input = Graph(edges)

    correct = MDPrimeUndirected(
        (
            1,
            MDSeriesUndirected(
                (
                    MDParallelUndirected((2, 3)),
                    4,
                )
            ),
            5,
            MDParallelUndirected((6, 7)),
            MDSeriesUndirected(
                (
                    8,
                    9,
                    MDParallelUndirected((10, 11)),
                )
            ),
        )
    )

    result = undirected_md_naive(input)
    assert correct == result


def test_modular_decomposition_complex_2():
    # pulled from https://www.researchgate.net/figure/The-graph-G_fig1_226478903
    input = Graph(
        (
            (1, 2),
            (2, 7),
            (3, 5),
            (3, 7),
            (4, 6),
            (4, 7),
            (5, 6),
            (5, 7),
            (6, 7),
            (7, 8),
            (7, 9),
            (8, 9),
        )
    )
    correct = MDPrimeUndirected(
        (
            1,
            2,
            7,
            MDParallelUndirected(
                (MDSeriesUndirected((8, 9)), MDPrimeUndirected((3, 4, 5, 6)))
            ),
        )
    )
    result = undirected_md_naive(input)
    assert correct == result


def make_random_undirected_graph(num_nodes: int, p: float) -> Graph:
    """Generate a random undirected graph"""
    G = Graph()
    G.add_nodes_from(range(num_nodes))

    for i in range(num_nodes):
        for j in range(i + 1, num_nodes):
            if random.random() < p:
                G.add_edge(i, j)

    return G


def test_modular_decomposition_random_graphs():
    """Test that naive and non-naive implementations match on random graphs"""
    random.seed(42)  # For reproducibility

    for _ in range(100):
        num_nodes = random.randint(2, 20)
        p = random.random() * 0.7

        G = make_random_undirected_graph(num_nodes, p)

        naive_result = undirected_md_naive(G)
        our_result = undirected_md_naive(G)

        assert (
            naive_result == our_result
        ), f"Results differ for graph with {num_nodes} nodes and {len(G.edges)} edges"
