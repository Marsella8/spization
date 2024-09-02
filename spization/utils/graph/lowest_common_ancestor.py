from networkx import DiGraph
import networkx as nx
from spization.utils.sp.serial_parallel_decomposition import Node
from spization.utils.general import get_any


def lowest_common_ancestor(g: DiGraph, nodes: set[Node]) -> Node | None:
    assert all(n in g.nodes() for n in nodes)
    lca: Node | None = get_any(nodes)
    for n in nodes:
        lca = nx.lowest_common_ancestor(g, lca, n)
        if lca is None:
            return lca
    return lca
