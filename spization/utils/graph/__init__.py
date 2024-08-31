import networkx as nx
from networkx import DiGraph
from spization.utils.general import get_any, get_only
from spization.utils.sp.serial_parallel_decomposition import Node, SyncNode


def sources(g: DiGraph) -> set[Node]:
    return {node for node, in_degree in g.in_degree() if in_degree == 0}


def sinks(g: DiGraph) -> set[Node]:
    return {node for node, out_degree in g.out_degree() if out_degree == 0}


def single_source_dag_longest_path_lengths_from_source(g: DiGraph) -> dict[Node, int]:
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


def lowest_common_ancestor(g: DiGraph, nodes: set[Node]) -> Node | None:
    assert all(n in g.nodes() for n in nodes)
    lca: Node | None = get_any(nodes)
    for n in nodes:
        lca = nx.lowest_common_ancestor(g, lca, n)
        if lca is None:
            return lca
    return lca


def replace_sync_nodes(g: DiGraph) -> DiGraph:
    c = g.copy()

    for node in g.nodes():
        if isinstance(node, SyncNode):
            for pred in list(c.predecessors(node)):
                for succ in list(c.successors(node)):
                    c.add_edge(pred, succ)
            c.remove_node(node)

    return c


def strata_sort(g: DiGraph) -> list[Node]:
    depth_map: dict[Node, int] = single_source_dag_longest_path_lengths_from_source(g)
    return sorted(depth_map.keys(), key=lambda node: depth_map[node])


def is_2_terminal_dag(g: DiGraph) -> bool:
    if not nx.is_directed_acyclic_graph(g):
        return False

    sources: set[Node] = {n for n in g.nodes() if g.in_degree(n) == 0}
    sinks: set[Node] = {n for n in g.nodes() if g.out_degree(n) == 0}
    if len(sources) != 1 or len(sinks) != 1:
        return False
    return True


def is_integer_graph(g: DiGraph) -> bool:
    return all(isinstance(node, Node) for node in g.nodes())


def is_single_sourced(g: DiGraph) -> bool:
    sources: set[Node] = {n for n in g.nodes() if g.in_degree(n) == 0}
    return len(sources) == 1
