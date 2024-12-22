from multimethod import multimethod
from networkx import DiGraph

from spization.objects import (
    Node,
    Parallel,
    Serial,
    SerialParallelDecomposition,
)


@multimethod
def work_cost(node: Node, cost_map: dict[Node, int | float] = None) -> int | float:
    if cost_map is None:
        return 1
    return cost_map[node]


@multimethod
def work_cost(
    sp: Parallel | Serial, cost_map: dict[Node, int | float] = None
) -> int | float:
    return sum(work_cost(child, cost_map) for child in sp)


@multimethod
def work_cost(g: DiGraph, cost_map: dict[Node, int | float] = None) -> int | float:
    if cost_map:
        assert set(cost_map.keys()) == set(g.nodes())
        sum(cost_map.values())
    else:
        return len(g.nodes())


@multimethod
def relative_work_cost_increase(
    original: SerialParallelDecomposition,
    modified: DiGraph,
    cost_map: dict[Node, int | float] = None,
) -> int | float:
    return work_cost(modified, cost_map) / work_cost(original, cost_map)


@multimethod
def relative_work_cost_increase(
    original: DiGraph, modified: DiGraph, cost_map: dict[Node, int | float] = None
) -> int | float:
    return work_cost(modified, cost_map) / work_cost(original, cost_map)
