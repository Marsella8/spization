import networkx as nx
from networkx import DiGraph

from spization.__internals.general import get_only
from spization.__internals.graph import (
    is_compatible_graph,
    is_single_sourced,
    longest_path_lengths_from_source,
    lowest_common_ancestor,
    sources,
)
from spization.objects import Node, PureNode, SyncNode
from spization.utils import (
    critical_path_cost,
    dependencies_are_maintained,
    get_critical_path_cost_map,
    spg_to_sp,
    ttspg_to_spg,
)


def get_component(SP: DiGraph, nodes: Node) -> set[Node]:
    parents = set().union(*[SP.predecessors(node) for node in nodes])
    children = set().union(*[nx.descendants(SP, p) for p in parents])
    other_parents = set().union(*[SP.predecessors(c) for c in children])
    return parents | children | other_parents


def get_forest(SP: DiGraph, handle: Node, component: set[Node]) -> set[Node]:
    subtrees = [
        (set(nx.descendants(SP, node)) | {node}) for node in SP.successors(handle)
    ]
    subtrees = [subtree for subtree in subtrees if subtree & component]
    forest = set().union(*subtrees) | {handle}
    forest = {node for node in forest if isinstance(node, PureNode)}
    return forest


def get_up_and_down(
    nodes: Node, SP: DiGraph, forest: set[Node], cost_map: dict[Node, float]
) -> tuple[set[Node], set[Node]]:
    SP: DiGraph = ttspg_to_spg(SP)

    base_down = set(nodes)
    base_up = set().union(*[nx.ancestors(SP, node) for node in nodes]) & forest
    assignable_nodes = forest - (base_up | base_down)
    critical_path_cost_map = get_critical_path_cost_map(
        SP.subgraph(forest), cost_map
    )
    def get_partitions():
        bipartitions = set()
        bipartitions.add((frozenset(base_up), frozenset(base_down | assignable_nodes)))
        for node in assignable_nodes:
            reference_cost = critical_path_cost_map.get(node)
            up = base_up | {
                node
                for node in assignable_nodes
                if critical_path_cost_map.get(node) <= reference_cost
            }
            down = (base_down | assignable_nodes) - up
            bipartitions.add((frozenset(up), frozenset(down)))
        return bipartitions

    bipartitions = get_partitions()

    def is_valid_bipartition(up: set[Node], down: set[Node]) -> bool:
        for node in nodes:
            if node not in down:
                return False

        for node in SP.nodes():
            if node in down:
                if any(child in up for child in SP.successors(node)):
                    return False
        parents = SP.predecessors(node)
        if any(p not in up for p in parents):
            return False
        return True

    valid_partitions = [
        (up, down) for up, down in bipartitions if is_valid_bipartition(up, down)
    ]

    assert valid_partitions

    def partition_cost(
        partition: tuple[set[Node], set[Node]],
    ) -> tuple[float, float, float]:
        up, down = partition
        up_cost = critical_path_cost(SP.subgraph(up), cost_map)
        down_cost = critical_path_cost(SP.subgraph(down), cost_map)
        return (up_cost + down_cost, down_cost, len(down))

    best_up, best_down = min(valid_partitions, key=partition_cost)
    up_subgraph = SP.subgraph(best_up)
    up_frontier = {node for node in best_up if up_subgraph.out_degree(node) == 0}

    down_subgraph = SP.subgraph(best_down)
    down_frontier = {node for node in best_down if down_subgraph.in_degree(node) == 0}

    return best_up, best_down, up_frontier, down_frontier


def edges_to_remove(
    SP: DiGraph, up: set[Node], down: set[Node]
) -> set[tuple[Node | SyncNode, Node | SyncNode]]:
    to_remove = set()
    for u in up:
        for v in SP.successors(u):
            if v in down:
                to_remove.add((u, v))
    for node in list(SP.nodes()):
        if (
            isinstance(node, SyncNode)
            and all(p in up for p in SP.predecessors(node))
            and all(s in down for s in SP.successors(node))
        ):
            SP.remove_node(node)
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


def get_next_nodes(SP: DiGraph, g: DiGraph, cost_map: dict[Node, float]) -> Node:
    sp_longest_paths = longest_path_lengths_from_source(SP, cost_map)

    candidate_nodes: set[Node] = {
        node
        for node in g.nodes()
        if node not in SP.nodes()
        and all(parent in SP.nodes() for parent in g.predecessors(node))
    }

    assert candidate_nodes

    critical_path_costs = {}
    for node in candidate_nodes:
        parent_costs = {sp_longest_paths[parent] for parent in g.predecessors(node)}
        critical_path_costs[node] = cost_map[node] + max(parent_costs)

    ref_node = min(
        critical_path_costs.keys(),
        key=lambda node: (critical_path_costs.get(node), node),
    )

    nodes = {ref_node}
    for node in candidate_nodes:
        if g.predecessors(node) == g.predecessors(ref_node):
            nodes.add(node)
    return nodes


def flexible_sync(g: DiGraph, cost_map: dict[Node, float]) -> DiGraph:
    assert is_single_sourced(g) and is_compatible_graph(g)
    g = nx.transitive_reduction(g)
    SP = DiGraph()
    cost_map = cost_map.copy()
    root: Node = get_only(sources(g))
    SP.add_node(root)
    node = root
    while not set(g.nodes).issubset(SP.nodes):
        nodes = get_next_nodes(SP, g, cost_map)
        SP.add_nodes_from(nodes)
        for node in nodes:
            SP.add_edges_from(g.in_edges(node))
        SP = nx.transitive_reduction(
            SP
        )  # TODO this can be improved, simply selectively remove the previously added edges

        component: set[Node] = get_component(SP, nodes)
        handle: Node = lowest_common_ancestor(SP, component)
        forest: set[Node] = get_forest(SP, handle, component)
        up, down, up_frontier, down_frontier = get_up_and_down(
            nodes, SP, forest, cost_map
        )

        sync = SyncNode()
        cost_map[sync] = 0
        SP.remove_edges_from(edges_to_remove(SP, up, down))
        SP.add_edges_from(edges_to_add(up_frontier, down_frontier, sync))
    SP = ttspg_to_spg(SP)
    decomp = spg_to_sp(SP)
    assert decomp is not None
    assert dependencies_are_maintained(g, decomp)
    return decomp

# TODO ? IMPLEMENT the change where all the dependencies of a guy up in the tree are pushed down
