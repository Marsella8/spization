from typing import Iterable

from networkx import DiGraph

from spization.objects import DiEdge, PureNode


def add_node(g: DiGraph) -> PureNode:
    if not hasattr(g, "node_counter"):
        g.node_counter = 1
        return 0
    n = g.node_counter
    g.node_counter += 1
    if n in set(g.nodes()):
        g.node_counter = max(g.nodes())
        return add_node(g)
    return n


def add_nodes(g: DiGraph, n: int) -> list[PureNode]:
    return [add_node(g) for _ in range(n)]


def add_edges(g: DiGraph, edges: Iterable[DiEdge]) -> None:
    for edge in edges:
        g.add_edge(edge[0], edge[1])
