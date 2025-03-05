import networkx as nx
from networkx import DiGraph

from spization.__internals.general import get_only
from spization.__internals.graph import (
    is_2_terminal_dag,
    is_compatible_graph,
    longest_path_lengths_from_source,
    lowest_common_ancestor,
    sources,
    strata_sort,
)
from spization.objects import Node, SerialParallelDecomposition, SyncNode, NodeRole, PureNode
from spization.utils import spg_to_sp, ttspg_to_spg
from spization.__internals.graph import add_node

def add_dummy_nodes(g: DiGraph, node_roles : dict[PureNode, NodeRole]) -> tuple[DiGraph, dict[PureNode, NodeRole]]:
    """Fixes the edges spanning across multiple strata by breaking up the edge into a linear graph"""
    new_g = g.copy()
    depth_map: dict[Node, int] = longest_path_lengths_from_source(g)
    for src, dst in list(g.edges()):
        depth_diff = depth_map[dst] - depth_map[src]
        if depth_diff > 1:
            new_g.remove_edge(src, dst)

            prev_node = src
            for i in range(1, depth_diff):
                intermediate_node = add_node(new_g)
                node_roles[intermediate_node] = NodeRole.DUMMY
                new_g.add_edge(prev_node, intermediate_node)
                prev_node = intermediate_node

            new_g.add_edge(prev_node, dst)
    new_depth_map: dict[Node, int] = longest_path_lengths_from_source(new_g)
    assert all(
        new_depth_map[dst] - new_depth_map[src] == 1 for src, dst in new_g.edges()
    )
    return (new_g, node_roles)


def delete_dummy_nodes(g: DiGraph, node_roles) -> DiGraph:
    c = g.copy()

    for node in g.nodes():
        if node_roles[node] == NodeRole.DUMMY:
            for pred in list(c.predecessors(node)):
                for succ in list(c.successors(node)):
                    c.add_edge(pred, succ)
            c.remove_node(node)
    return c


def get_component(
    SP: DiGraph, node: Node, depth_map: dict[Node, int], max_depth: int
) -> set[Node]:
    last_two_layers: DiGraph = SP.subgraph(
        [
            n
            for n in SP.nodes()
            if (depth_map.get(n) in (max_depth, max_depth - 1))
            or (
                isinstance(n, SyncNode)
                and all(depth_map[s] == max_depth for s in SP.successors(n))
            )
        ]
    )
    # assert(all(not isinstance(n, SyncNode) for n in last_two_layers.nodes))
    component: set[Node] = get_only(
        [c for c in nx.weakly_connected_components(last_two_layers) if node in c]
    )
    component = {n for n in component if not isinstance(n, SyncNode)}
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


# TODO make sure we have Node and Concrete Node when needed


def edges_to_remove(
    SP: DiGraph, up: set[Node], down: set[Node]
) -> set[tuple[Node, Node]]:
    to_remove = set()
    for u in up:
        to_remove |= set(SP.out_edges(u))
    for d in down:
        to_remove |= set(SP.in_edges(d))
    return to_remove


def edges_to_add(up: set[Node], down: set[Node], node_roles) -> tuple[set[tuple[Node, Node]], dict]:
    to_add: set[tuple[Node, Node]] = set()
    sync = SyncNode()
    node_roles[sync] = NodeRole.SYNC
    for u in up:
        to_add.add((u, sync))
    for d in down:
        to_add.add((sync, d))
    return (to_add, node_roles)


def spanish_strata_sync(g: DiGraph) -> SerialParallelDecomposition:
    assert is_2_terminal_dag(g) and is_compatible_graph(g)
    g = nx.transitive_reduction(g)
    node_roles = {n : NodeRole.STANDARD for n in g.nodes}
    g, node_roles = add_dummy_nodes(g, node_roles)
    depth_map: dict[Node, int] = longest_path_lengths_from_source(g)
    root: Node = get_only(sources(g))
    SP = DiGraph()
    SP.add_node(root)
    for node in strata_sort(g):
        if node == root:
            continue
        SP.add_node(node)
        SP.add_edges_from(g.in_edges(node))
        max_depth: int = max({d for n, d in depth_map.items() if n in SP.nodes()})

        component: set[Node] = get_component(SP, node, depth_map, max_depth)
        handle: Node = lowest_common_ancestor(SP, component)
        forest: set[Node] = get_forest(SP, handle, component)
        up, down = get_up_and_down(forest, depth_map, max_depth)

        SP.remove_edges_from(edges_to_remove(SP, up, down))
        edges, node_roles = edges_to_add(up, down, node_roles)
        SP.add_edges_from(edges)

    SP = nx.transitive_reduction(delete_dummy_nodes(SP, node_roles))
    SP = ttspg_to_spg(SP)
    decomp: SerialParallelDecomposition | None = spg_to_sp(SP)
    assert decomp is not None
    return decomp
