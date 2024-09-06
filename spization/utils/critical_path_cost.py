import networkx as nx
from multimethod import multimethod
from networkx import DiGraph

from spization.__internals.graph import sources
from spization.objects import (
    Node,
    Parallel,
    Serial,
    SerialParallelDecomposition,
)

Number = float | int


@multimethod
def critical_path_cost(
    node: Node, cost_map: dict[Node, Number] | None = None
) -> Number:
    if cost_map is None:
        return 1
    return cost_map[node]


@multimethod
def critical_path_cost(
    parallel: Parallel, cost_map: dict[Node, Number] | None = None
) -> Number:
    return max(critical_path_cost(child, cost_map) for child in parallel)


@multimethod
def critical_path_cost(
    serial: Serial, cost_map: dict[Node, Number] | None = None
) -> Number:
    return sum(critical_path_cost(child, cost_map) for child in serial)


@multimethod
def critical_path_cost(
    g: DiGraph, cost_map: dict[Node, Number] | None = None
) -> Number:
    assert nx.is_directed_acyclic_graph(g)
    if cost_map is None:
        cost_map = {node: 1 for node in g.nodes()}
    path_map = {node: cost_map[node] for node in sources(g)}
    for node in nx.topological_sort(g):
        if node not in sources(g):
            path_map[node] = cost_map[node] + max(
                path_map[p] for p in g.predecessors(node)
            )
    return max(path_map.values())


@multimethod
def relative_critical_path_cost_increase(
    original: DiGraph,
    modified: SerialParallelDecomposition,
    cost_map: dict[Node, Number] | None = None,
) -> Number:
    return critical_path_cost(modified, cost_map) / critical_path_cost(
        original, cost_map
    )


@multimethod
def relative_critical_path_cost_increase(
    original: DiGraph, modified: DiGraph, cost_map: dict[Node, Number] | None = None
) -> Number:
    return critical_path_cost(modified, cost_map) / critical_path_cost(
        original, cost_map
    )
