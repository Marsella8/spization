import networkx as nx
from networkx import DiGraph

from spization.utils import ttspg_to_spg
from spization.utils.general import get_only
from spization.utils.graph.longest_path_lengths_from_source import (
    longest_path_lengths_from_source,
)
from spization.utils.graph.lowest_common_ancestor import lowest_common_ancestor
from spization.utils.graph.properties import is_2_terminal_dag, is_compatible_graph
from spization.utils.graph.sources import sources
from spization.utils.graph.strata_sort import strata_sort
from spization.utils.sp.serial_parallel_decomposition import DummyNode, Node, SyncNode


def add_dummy_nodes(g: DiGraph) -> DiGraph:
    """Fixes the edges spanning across multiple strata by breaking up the edge into a linear graph"""
    new_g = g.copy()
    depth_map: dict[Node, int] = longest_path_lengths_from_source(g)
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
    new_depth_map: dict[Node, int] = longest_path_lengths_from_source(new_g)
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


def get_component(SP: DiGraph, node: Node, depth_map: dict[Node, int]) -> set[Node]:
    max_depth: int = max([depth_map[n] for n in SP.nodes() if isinstance(n, Node)])
    SP_without_sync_nodes: DiGraph = ttspg_to_spg(SP)
    last_two_layers: DiGraph = SP_without_sync_nodes.subgraph(
        [
            n
            for n in SP_without_sync_nodes.nodes()
            if depth_map[n] in (max_depth, max_depth - 1)
        ]
    )
    component: set[Node] = get_only(
        [c for c in nx.weakly_connected_components(last_two_layers) if node in c]
    )
    return component


def get_forest(SP: DiGraph, handle: Node, component: set[Node]) -> set[Node]:
    subtrees = [
        (set(nx.descendants(SP, node)) | {node}) for node in SP.successors(handle)
    ]
    subtrees = [subtree for subtree in subtrees if subtree & component]
    forest = set().union(*subtrees) | {handle}
    forest = {node for node in forest if not isinstance(node, SyncNode)}
    return forest


def get_up_and_down(
    forest: set[Node], depth_map: dict[Node, int], max_depth: int
) -> tuple[set[Node], set[Node]]:
    down = {node for node in forest if depth_map[node] == max_depth}
    up = {node for node in forest if depth_map[node] == max_depth - 1}
    return up, down


def edges_to_remove(
    SP: DiGraph, up: set[Node], down: set[Node]
) -> set[tuple[Node | SyncNode, Node | SyncNode]]:
    to_remove = set()
    for u in up:
        to_remove |= set(SP.out_edges(u))
    for d in down:
        to_remove |= set(SP.in_edges(d))
    return to_remove


def edges_to_add(
    up: set[Node], down: set[Node], sync: SyncNode
) -> set[tuple[Node | SyncNode, Node | SyncNode]]:
    to_add: set[tuple[Node | SyncNode, Node | SyncNode]] = set()
    for u in up:
        to_add.add((u, sync))
    for d in down:
        to_add.add((sync, d))
    return to_add


def spanish_strata_sync(g: DiGraph) -> DiGraph:
    assert is_2_terminal_dag(g) and is_compatible_graph(g)

    g = add_dummy_nodes(g)
    depth_map: dict[Node, int] = longest_path_lengths_from_source(g)
    SP = DiGraph()
    root: Node = get_only(sources(g))
    SP.add_node(root)
    for node in strata_sort(g):
        if node == root:
            continue
        SP.add_node(node)
        SP.add_edges_from(g.in_edges(node))
        SP = nx.transitive_reduction(SP)
        max_depth: int = max(
            {d for n, d in depth_map.items() if n in SP.nodes() & g.nodes()}
        )

        component: set[Node] = get_component(SP, node, depth_map)
        handle: Node = lowest_common_ancestor(SP, component)
        forest: set[Node] = get_forest(SP, handle, component)
        up, down = get_up_and_down(forest, depth_map, max_depth)

        sync = SyncNode()
        SP.remove_edges_from(edges_to_remove(SP, up, down))
        SP.add_edges_from(edges_to_add(up, down, sync))

    SP = nx.transitive_reduction(delete_dummy_nodes(SP))
    SP = ttspg_to_spg(SP)
    return SP
