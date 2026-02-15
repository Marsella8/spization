from typing import Iterable

from networkx import DiGraph

from spization.objects import DiEdge, Node


def add_node(g: DiGraph) -> Node:
    n = max(g.nodes(), default=-1) + 1
    g.add_node(n)
    return n


def add_nodes(g: DiGraph, n: int) -> list[Node]:
    return [add_node(g) for _ in range(n)]


def add_edges(g: DiGraph, edges: Iterable[DiEdge]) -> None:
    for edge in edges:
        g.add_edge(edge[0], edge[1])
