import networkx as nx

from spization.objects import Parallel, Serial
from spization.utils import critical_path_cost

n = [i for i in range(10)]


def test_critical_path_cost_single_node():
    cost_map = {n[0]: 5}
    result = critical_path_cost(n[0], cost_map)
    assert result == 5


def test_critical_path_cost_parallel():
    cost_map = {n[0]: 2, n[1]: 3, n[2]: 1}
    parallel = Parallel((n[0], n[1], n[2]))
    result = critical_path_cost(parallel, cost_map)
    assert result == 3


def test_critical_path_cost_serial():
    cost_map = {n[0]: 2, n[1]: 3, n[2]: 1}
    serial = Serial((n[0], n[1], n[2]))
    result = critical_path_cost(serial, cost_map)
    assert result == 6


def test_critical_path_cost_dag():
    G = nx.DiGraph()
    G.add_edges_from([(n[0], n[2]), (n[1], n[2]), (n[2], n[3])])
    cost_map = {n[0]: 2, n[1]: 3, n[2]: 4, n[3]: 1}
    result = critical_path_cost(G, cost_map)
    assert result == 8  # n[1] -> n[2] -> n[3]


def test_critical_path_cost_complex():
    serial = Serial((n[0], Parallel((n[1], n[2])), n[3]))
    cost_map = {n[0]: 2, n[1]: 3, n[2]: 1, n[3]: 4}
    result = critical_path_cost(serial, cost_map)
    assert result == 9  # 2 + max(3, 1) + 4
