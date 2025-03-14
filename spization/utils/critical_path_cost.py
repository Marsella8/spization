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


@multimethod
def critical_path_cost(
    node: Node, cost_map: dict[Node, int | float] | None = None
) -> int | float:
    if cost_map is None:
        return 1
    return cost_map[node]


@multimethod
def critical_path_cost(
    parallel: Parallel, cost_map: dict[Node, int | float] | None = None
) -> int | float:
    return max(critical_path_cost(child, cost_map) for child in parallel)


@multimethod
def critical_path_cost(
    serial: Serial, cost_map: dict[Node, int | float] | None = None
) -> int | float:
    return sum(critical_path_cost(child, cost_map) for child in serial)


@multimethod
def critical_path_cost(
    g: DiGraph, cost_map: dict[Node, int | float] | None = None
) -> int | float:
    mp = get_critical_path_cost_map(g, cost_map)
    return 0 if mp == {} else max(mp.values())


def get_critical_path_cost_map(
    g: DiGraph, cost_map: dict[Node, int | float] | None = None
) -> dict[Node, int | float]:
    if g.number_of_nodes() == 0:
        return {}

    assert nx.is_directed_acyclic_graph(g)

    if cost_map is None:
        cost_map = {node: 1 for node in g.nodes()}

    path_map = {node: cost_map[node] for node in sources(g)}

    for node in nx.topological_sort(g):
        if node not in sources(g):
            path_map[node] = cost_map[node] + max(
                path_map[p] for p in g.predecessors(node)
            )

    return path_map


@multimethod
def relative_critical_path_cost_increase(
    original: DiGraph,
    modified: SerialParallelDecomposition,
    cost_map: dict[Node, int | float] | None = None,
) -> int | float:
    return critical_path_cost(modified, cost_map) / critical_path_cost(
        original, cost_map
    )


@multimethod
def relative_critical_path_cost_increase(
    original: DiGraph,
    modified: DiGraph,
    cost_map: dict[Node, int | float] | None = None,
) -> int | float:
    return critical_path_cost(modified, cost_map) / critical_path_cost(
        original, cost_map
    )
