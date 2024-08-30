from networkx import DiGraph
from spization.sp_utils.serial_parallel_decomposition import Serial, Parallel
from spization.algorithms.naive_strata_sync import barrier_sync


def test_linear_graph():
    input = DiGraph([(1, 2), (1, 3), (2, 4), (3, 5), (4, 6), (5, 6)])
    correct = Serial((1, Parallel((2, 3)), Parallel((4, 5)), 6))
    result = barrier_sync(input)
    assert correct == result
