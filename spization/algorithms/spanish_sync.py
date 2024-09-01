from networkx import DiGraph
import networkx as nx
from spization.utils.graph import (
    single_source_dag_longest_path_lengths_from_source,
    lowest_common_ancestor,
)
from spization.utils.general import get_only
from spization.utils.graph import (
    sources,
    replace_sync_nodes,
    strata_sort,
    is_2_terminal_dag,
    is_integer_graph,
)
from spization import Node, SyncNode, DummyNode


def get_subtree(g: DiGraph, root: Node) -> set[Node]:
    return set(nx.descendants(g, root)) | {root}


def add_dummy_nodes(g: DiGraph) -> DiGraph:
    new_g = g.copy()
    depth_map: dict[Node, int] = single_source_dag_longest_path_lengths_from_source(g)
    for src, dst in list(g.edges()):
        depth_diff = depth_map[dst] - depth_map[src]
        if depth_diff > 1:
            new_g.remove_edge(src, dst)

            prev_node = src
            for i in range(1, depth_diff):
                intermediate_node = DummyNode()
                new_g.add_node(intermediate_node)
                new_g.add_edge(prev_node, intermediate_node)
                prev_node = intermediate_node

            new_g.add_edge(prev_node, dst)
    new_depth_map: dict[Node, int] = single_source_dag_longest_path_lengths_from_source(
        new_g
    )
    assert all(
        new_depth_map[dst] - new_depth_map[src] == 1 for src, dst in new_g.edges()
    )
    return new_g


def delete_dummy_nodes(g: DiGraph) -> DiGraph:
    c = g.copy()

    for node in g.nodes():
        if isinstance(node, DummyNode):
            for pred in list(c.predecessors(node)):
                for succ in list(c.successors(node)):
                    c.add_edge(pred, succ)
            c.remove_node(node)
    return c


def spanish_strata_sync(g: DiGraph) -> DiGraph:
    assert is_2_terminal_dag(g) and is_integer_graph(g)
    g = add_dummy_nodes(g)
    depth_map: dict[Node, int] = single_source_dag_longest_path_lengths_from_source(g)
    SP = DiGraph()
    root: Node = get_only(sources(g))
    SP.add_node(root)
    for node in strata_sort(g):
        if node == root:
            continue
        SP.add_node(node)
        SP.add_edges_from(g.in_edges(node))
        SP = nx.transitive_reduction(SP)
        max_depth: int = max([depth_map[n] for n in SP.nodes() & g.nodes()])
        ss: DiGraph = replace_sync_nodes(SP)
        S: DiGraph = ss.subgraph(
            [n for n in ss.nodes() if depth_map[n] in (max_depth, max_depth - 1)]
        )
        component: set[Node] = get_only(
            [c for c in nx.weakly_connected_components(S) if node in c]
        )

        handle: Node | None = lowest_common_ancestor(SP, component)
        assert handle is not None
        subtrees = [get_subtree(SP, succ) for succ in SP.successors(handle)]
        subtrees = [subtree for subtree in subtrees if subtree & component]
        forest = (set().union(*subtrees) | {handle}) & g.nodes()  # exclude sync nodes

        down = {node for node in forest if depth_map[node] == max_depth}
        up = {node for node in forest if depth_map[node] == max_depth - 1}

        sync = SyncNode()

        for u in up:
            to_remove = [
                (src, dst)
                for src, dst in SP.out_edges(u)
                if isinstance(dst, SyncNode) or (depth_map[dst] == max_depth)
            ]
            SP.remove_edges_from(to_remove)
            SP.add_edge(u, sync)

        for d in down:
            to_remove = [
                (src, dst)
                for src, dst in SP.in_edges(d)
                if isinstance(src, SyncNode) or (depth_map[src] == max_depth - 1)
            ]
            SP.remove_edges_from(to_remove)
            SP.add_edge(sync, d)

    return nx.transitive_reduction(
        replace_sync_nodes(nx.transitive_reduction(delete_dummy_nodes(SP)))
    )
