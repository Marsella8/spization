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
from spization.objects import DummyNode, Node, SerialParallelDecomposition, SyncNode
from spization.utils import get_serial_parallel_decomposition, ttspg_to_spg


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


def edges_to_add(up: set[Node], down: set[Node]) -> set[tuple[Node, Node]]:
    to_add: set[tuple[Node, Node]] = set()
    sync = SyncNode()
    for u in up:
        to_add.add((u, sync))
    for d in down:
        to_add.add((sync, d))
    return to_add


def spanish_strata_sync(g: DiGraph) -> SerialParallelDecomposition:
    assert is_2_terminal_dag(g) and is_compatible_graph(g)
    g = nx.transitive_reduction(g)
    g = add_dummy_nodes(g)
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
        SP.add_edges_from(edges_to_add(up, down))

    SP = nx.transitive_reduction(delete_dummy_nodes(SP))
    SP = ttspg_to_spg(SP)
    decomp: SerialParallelDecomposition | None = get_serial_parallel_decomposition(SP)
    assert decomp is not None
    return decomp


# TODO: how to get around the dummy nodes ?
# TODO: check does changing around the order in which we parse the strata change the final result?
