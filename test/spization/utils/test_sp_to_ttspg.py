import networkx as nx
from networkx import DiGraph

from spization.objects import Parallel, PureNode, Serial, SyncNode
from spization.utils import sp_to_ttspg


def test_single_node():
    sp = PureNode(0)
    result = sp_to_ttspg(sp)
    correct = DiGraph()
    correct.add_node(0)
    assert nx.is_isomorphic(correct, result)


def test_sp_to_ttspg_parallel():
    sp = Parallel((1, 2, 3))
    result = sp_to_ttspg(sp)
    correct = DiGraph()
    correct.add_nodes_from((1, 2, 3))
    assert nx.is_isomorphic(correct, result)


def test_sp_to_ttspg_serial():
    sp = Serial((1, 2, 3))
    result = sp_to_ttspg(sp)
    correct = DiGraph(
        ((1, SyncNode(0)), (SyncNode(0), 2), (2, SyncNode(1)), (SyncNode(1), 3))
    )
    assert nx.is_isomorphic(correct, result)


def test_sp_to_ttspg_composite():
    sp = Serial((Parallel((1, Serial((2, 3)))), 4))
    result = sp_to_ttspg(sp)
    print(result.edges())
    correct = DiGraph(
        (
            (SyncNode(0), 1),
            (SyncNode(0), 2),
            (1, SyncNode(1)),
            (2, SyncNode(2)),
            (SyncNode(2), 3),
            (3, SyncNode(1)),
            (SyncNode(1), 4),
        )
    )
    assert nx.is_isomorphic(correct, result)


def test_sp_to_ttspg_serial_strands():
    sp = Serial((1, Parallel((Serial((2, 3)), Serial((4, 5)))), 6))
    result = sp_to_ttspg(sp)
    print(result.edges())
    correct = DiGraph(
        (
            (1, SyncNode(0)),
            (SyncNode(0), 2),
            (SyncNode(0), 4),
            (2, SyncNode(3)),
            (SyncNode(3), 3),
            (3, SyncNode(1)),
            (4, SyncNode(4)),
            (SyncNode(4), 5),
            (5, SyncNode(1)),
            (SyncNode(1), 6),
        )
    )
    assert nx.is_isomorphic(correct, result)
