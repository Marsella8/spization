from networkx import DiGraph

from spization.objects import Parallel, PureNode, Serial
from spization.utils import work_cost

n = [PureNode(i) for i in range(4)]


def test_work_cost_single_node():
    cost_map = {n[0]: 5}
    result = work_cost(n[0], cost_map)
    assert result == 5


def test_work_cost_parallel():
    cost_map = {n[0]: 2, n[1]: 3}
    parallel = Parallel((n[0], n[1], n[0]))
    result = work_cost(parallel, cost_map)
    assert result == 2 + 2 + 3


def test_work_cost_serial():
    cost_map = {n[0]: 2, n[1]: 3}
    serial = Serial((n[0], n[1], n[0]))
    result = work_cost(serial, cost_map)
    assert result == 2 + 2 + 3


def test_work_cost_composite():
    serial = Serial((n[0], Parallel((n[1], n[2])), n[3]))
    cost_map = {n[0]: 2, n[1]: 3, n[2]: 1, n[3]: 4}
    result = work_cost(serial, cost_map)
    assert result == 2 + 3 + 1 + 4


def test_work_cost_graph():
    input = DiGraph(
        ((0, 1), (0, 2), (0, 3), (1, 4), (2, 4), (3, 5), (4, 5), (4, 6), (5, 7), (6, 7))
    )
    result = work_cost(input)
    assert result == 8
