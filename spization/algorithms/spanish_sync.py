from networkx import DiGraph
import networkx as nx
from spization.utils.graph import (
    single_source_dag_longest_path_lengths_from_source,
    lowest_common_ancestor,
)
from spization.utils.general import get_only
from spization.utils.graph import sources, replace_dummy_nodes, strata_sort
from spization import Node, DummyNode


def get_subtree(g: DiGraph, root: Node) -> set[Node]:
    return set(nx.descendants(g, root)) | {root}


def spanish_strata_sync(g: DiGraph) -> DiGraph:
    SP = DiGraph()
    root: Node = get_only(sources(g))
    SP.add_node(root)
    depth_map: dict[Node, int] = single_source_dag_longest_path_lengths_from_source(g)
    for node in strata_sort(g):
        if node == root:
            continue
        SP.add_node(node)
        SP.add_edges_from(g.in_edges(node))
        SP = nx.transitive_reduction(SP)
        max_depth = max([depth_map[n] for n in SP.nodes() & g.nodes()])
        ss = replace_dummy_nodes(SP)
        S = ss.subgraph(
            [n for n in ss.nodes() if depth_map[n] in (max_depth, max_depth - 1)]
        )
        component: set[Node] = get_only(
            [c for c in nx.weakly_connected_components(S) if node in c]
        )
        handle = lowest_common_ancestor(SP, component)
        subtrees = [get_subtree(SP, succ) for succ in SP.successors(handle)]
        subtrees = [subtree for subtree in subtrees if subtree & component]
        forest = (set().union(*subtrees) | {handle}) & g.nodes()  # exclude sync nodes
        down = {node for node in forest if depth_map[node] == max_depth}
        up = {node for node in forest if depth_map[node] == max_depth - 1}
        for u in up:
            to_remove = [
                (src, dst)
                for src, dst in SP.out_edges(u)
                if isinstance(dst, DummyNode) or (depth_map[dst] == max_depth)
            ]
            SP.remove_edges_from(to_remove)

        for d in down:
            to_remove = [
                (src, dst)
                for src, dst in SP.in_edges(d)
                if isinstance(src, DummyNode) or (depth_map[src] == max_depth - 1)
            ]
            SP.remove_edges_from(to_remove)

        sync: DummyNode = DummyNode(node)

        for u in up:
            SP.add_edge(u, sync)

        for d in down:
            SP.add_edge(sync, d)

    return replace_dummy_nodes(SP)
