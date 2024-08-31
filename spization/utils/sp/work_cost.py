from multimethod import multimethod
from .serial_parallel_decomposition import (
    Node,
    SerialParallelDecomposition,
    Serial,
    Parallel,
)
from networkx import DiGraph


@multimethod
def work_cost(node: Node, cost_map: dict[Node, float] = None) -> float:
    if cost_map is None:
        return 1
    return cost_map[node]


@multimethod
def work_cost(sp: Parallel | Serial, cost_map: dict[Node, float] = None) -> float:
    return sum(work_cost(child, cost_map) for child in sp)


@multimethod
def work_cost(g: DiGraph, cost_map: dict[Node, float] = None) -> float:
    assert set(cost_map.keys()) == set(g.nodes())
    return sum(cost_map.values())


def relative_work_cost_increase(
    sp: SerialParallelDecomposition, g: DiGraph, cost_map: dict[Node, float] = None
) -> float:
    return work_cost(sp, cost_map) / work_cost(sp, cost_map)
