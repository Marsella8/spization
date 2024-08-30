from networkx import DiGraph
from spization.sp_utils.serial_parallel_decomposition import Serial, Parallel
from spization.algorithms.pure_node_dup import pure_node_dup

def test_linear_graph():
    input = DiGraph([(1,2), (1,3), (2,4), (2,5), (3,5), (4,6), (5,6)])
    correct = Serial((Parallel((Serial((1, 2, 4)), Serial((Parallel((Serial((1, 2)), Serial((1, 3)))), 5)))), 6))
    result = pure_node_dup(input)
    assert correct == result