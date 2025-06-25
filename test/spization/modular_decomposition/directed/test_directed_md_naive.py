from networkx import DiGraph, transitive_closure

from spization.modular_decomposition.directed.directed_md import (
    transitively_closed_dag_md_naive,
)
from spization.modular_decomposition.directed.objects import (
    MDParallel,
    MDPrime,
    MDSeries,
)


def test_modular_decomposition_single_node():
    input = DiGraph()
    input.add_node(1)
    input = transitive_closure(input)
    correct = 1
    result = transitively_closed_dag_md_naive(input)
    assert correct == result


def test_modular_decomposition_parallel():
    input = DiGraph()
    input.add_nodes_from((1, 2, 3, 4))
    input = transitive_closure(input)
    correct = MDParallel((1, 2, 3, 4))
    result = transitively_closed_dag_md_naive(input)
    assert correct == result


def test_modular_decomposition_series():
    input = DiGraph(((1, 2), (2, 3), (3, 4)))
    input = transitive_closure(input)
    correct = MDSeries((1, 2, 3, 4))
    result = transitively_closed_dag_md_naive(input)
    assert correct == result


def test_modular_decomposition_prime():
    input = DiGraph(((1, 3), (1, 4), (2, 4)))
    input = transitive_closure(input)
    correct = MDPrime((1, 2, 3, 4))
    result = transitively_closed_dag_md_naive(input)
    assert correct == result


def test_modular_decomposition_N_shape():
    input = DiGraph(((1, 4), (1, 3), (2, 5), (3, 5)))
    input = transitive_closure(input)
    correct = MDPrime((1, 2, 3, 4, 5))
    result = transitively_closed_dag_md_naive(input)
    assert correct == result
