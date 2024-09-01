from multimethod import multimethod
from .serial_parallel_decomposition import (
    Node,
    SerialParallelDecomposition,
    Serial,
    Parallel,
)
from spization.utils.graph import sources
from networkx import DiGraph
import networkx as nx


@multimethod
def critical_path_cost(node: Node, cost_map: dict[Node, float] = None) -> float:
    if cost_map is None:
        return 1
    return cost_map[node]


@multimethod
def critical_path_cost(parallel: Parallel, cost_map: dict[Node, float] = None) -> float:
    return max(critical_path_cost(child, cost_map) for child in parallel)


@multimethod
def critical_path_cost(serial: Serial, cost_map: dict[Node, float] = None) -> float:
    return sum(critical_path_cost(child, cost_map) for child in serial)


@multimethod
def critical_path_cost(g: DiGraph, cost_map: dict[Node, float] = None) -> float:
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


def relative_critical_path_cost_increase(
    sp: SerialParallelDecomposition, g: DiGraph, cost_map: dict[Node, float] = None
) -> float:
    return critical_path_cost(sp, cost_map) / critical_path_cost(sp, cost_map)