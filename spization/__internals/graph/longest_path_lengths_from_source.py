import networkx as nx
from multimethod import multimethod
from networkx import DiGraph

from spization.__internals.general import get_only
from spization.objects import Node

from .properties import is_single_sourced
from .sources import sources


@multimethod
def longest_path_lengths_from_source(g: DiGraph) -> dict[Node, int]:
    assert is_single_sourced(g)
    dist: dict[Node, int] = dict.fromkeys(g.nodes, -1)
    root: Node = get_only(sources(g))
    dist[root] = 0
    topo_order = nx.topological_sort(g)
    for n in topo_order:
        if n == root:
            continue
        dist[n] = 1 + max(dist[p] for p in g.predecessors(n))
    return dist


@multimethod
def longest_path_lengths_from_source(
    g: DiGraph, cost_map: dict[Node, int | float]
) -> dict[Node, int | float]:
    assert is_single_sourced(g)
    dist: dict[Node, int] = dict.fromkeys(g.nodes, -1)
    root: Node = get_only(sources(g))
    dist[root] = cost_map[root]
    topo_order = nx.topological_sort(g)
    for n in topo_order:
        if n == root:
            continue
        dist[n] = cost_map[n] + max(dist[p] for p in g.predecessors(n))
    return dist
