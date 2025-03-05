from typing import Iterable

from networkx import DiGraph

from spization.objects import DiEdge, PureNode


def add_node(g: DiGraph) -> PureNode:
    if len(g.nodes()) == 0:
        g.node_counter = 0
        g.add_node(0)
        return 0
    g.node_counter = max(g.nodes()) + 1
    n = g.node_counter
    g.add_node(n)
    return n


def add_nodes(g: DiGraph, n: int) -> list[PureNode]:
    return [add_node(g) for _ in range(n)]


def add_edges(g: DiGraph, edges: Iterable[DiEdge]) -> None:
    for edge in edges:
        g.add_edge(edge[0], edge[1])
