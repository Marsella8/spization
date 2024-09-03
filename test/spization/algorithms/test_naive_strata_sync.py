from networkx import DiGraph
from test_algorithms_utils import graph_generator

from spization import Parallel, Serial
from spization.algorithms import naive_strata_sync
from spization.utils import is_valid_sp


def test_linear_graph():
    input = DiGraph([(1, 2), (1, 3), (2, 4), (3, 5), (4, 6), (5, 6)])
    correct = Serial((1, Parallel((2, 3)), Parallel((4, 5)), 6))
    result = naive_strata_sync(input)
    assert correct == result


def test_correctness():
    for input in graph_generator():
        result = naive_strata_sync(input)
        assert is_valid_sp(input, result)
