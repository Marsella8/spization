from networkx import DiGraph

from spization.algorithms import pure_node_dup, tree_pure_node_dup
from spization.objects import Parallel, Serial
from spization.utils import dependencies_are_maintained
from testing_utils import graph_generator

def test_tree_pure_node_dup():
    input = DiGraph([(1, 2), (1, 3), (2, 4), (2, 5), (3, 5), (4, 6), (5, 6)])
    correct = Serial(
        (
            Parallel(
                (
                    Serial((1, 2, 4)),
                    Serial((Parallel((Serial((1, 2)), Serial((1, 3)))), 5)),
                )
            ),
            6,
        )
    )
    result = tree_pure_node_dup(input)
    assert correct == result


def test_pure_node_dup():
    input = DiGraph([(1, 2), (1, 3), (2, 4), (2, 5), (3, 5), (4, 6), (5, 6)])
    correct = Serial((1, Parallel((Serial((2, 4)), Serial((Parallel((2, 3)), 5)))), 6))
    result = pure_node_dup(input)
    assert correct == result


# def test_correctness():
#     for input in graph_generator():
#         result = pure_node_dup(input)
#         assert dependencies_are_maintained(input, result)

#         result = tree_pure_node_dup(input)
#         assert dependencies_are_maintained(input, result)
# TODO reenable after fixing dependencies_are_maintained for multiple nodes.