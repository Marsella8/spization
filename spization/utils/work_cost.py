from multimethod import multimethod
from networkx import DiGraph

from spization.objects import (
    Node,
    Parallel,
    Serial,
    SerialParallelDecomposition,
)

Number = int | float


@multimethod
def work_cost(node: Node, cost_map: dict[Node, Number] = None) -> Number:
    if cost_map is None:
        return 1
    return cost_map[node]


@multimethod
def work_cost(sp: Parallel | Serial, cost_map: dict[Node, Number] = None) -> Number:
    return sum(work_cost(child, cost_map) for child in sp)


@multimethod
def work_cost(g: DiGraph, cost_map: dict[Node, Number] = None) -> Number:
    assert set(cost_map.keys()) == set(g.nodes())
    return sum(cost_map.values())


def relative_work_cost_increase(
    sp: SerialParallelDecomposition, g: DiGraph, cost_map: dict[Node, Number] = None
) -> Number:
    return work_cost(sp, cost_map) / work_cost(sp, cost_map)