import networkx as nx
from networkx import DiGraph

from spization.__internals.general import get_any
from spization.objects import Node


def lowest_common_ancestor(g: DiGraph, nodes: set[Node]) -> Node | None:
    assert all(n in g.nodes() for n in nodes)
    lca: Node | None = get_any(nodes)
    for n in nodes:
        lca = nx.lowest_common_ancestor(g, lca, n)
        if lca is None:
            return lca
    return lca
