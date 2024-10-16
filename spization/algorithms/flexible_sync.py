import itertools

import networkx as nx
from networkx import DiGraph

from spization.__internals.general import get_only
from spization.__internals.graph import (
    is_2_terminal_dag,
    is_compatible_graph,
    longest_path_lengths_from_source,
    lowest_common_ancestor,
    sources,
)
from spization.objects import Node, SyncNode
from spization.utils import critical_path_cost, ttspg_to_spg


def get_component(SP: DiGraph, node: Node) -> set[Node]:
    parents = set(SP.predecessors(node))
    children = set().union(*{SP.successors(p) for p in parents})
    other_parents = set().union(*{SP.predecessors(c) for c in children})
    # other_other_parents = set().union(*{SP.predecessors(p) for p in other_parents if isinstance(p, SyncNode)})
    return parents | children | other_parents


def get_forest(SP: DiGraph, handle: Node, component: set[Node]) -> set[Node]:
    subtrees = [
        (set(nx.descendants(SP, node)) | {node}) for node in SP.successors(handle)
    ]
    subtrees = [subtree for subtree in subtrees if subtree & component]
    forest = set().union(*subtrees) | {handle}
    forest = {node for node in forest if not isinstance(node, SyncNode)}
    return forest


def get_up_and_down(
    main_node, SP: DiGraph, forest: set[Node], cost_map: dict[Node, float]
) -> tuple[set[Node], set[Node]]:
    all_subsets = list(
        itertools.chain.from_iterable(
            itertools.combinations(forest, r) for r in range(len(forest) + 1)
        )
    )

    SP: DiGraph = ttspg_to_spg(SP)

    bipartitions = set()
    for subset in all_subsets:
        subset = set(subset)
        complement = forest - subset
        bipartitions.add((frozenset(subset), frozenset(complement)))

    def is_valid_bipartition(up: set[Node], down: set[Node]) -> bool:
        if main_node not in down or len(down) == 0:
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

    if not valid_partitions:
        return set(), set()

    def partition_cost(partition: tuple[set[Node], set[Node]]) -> float:
        up, down = partition
        up_cost = critical_path_cost(SP.subgraph(up), cost_map)
        down_cost = critical_path_cost(SP.subgraph(down), cost_map)
        return up_cost + down_cost

    best_up, best_down = min(valid_partitions, key=partition_cost)
    print(best_up, best_down)
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


def get_next_node(SP: DiGraph, g: DiGraph, cost_map: dict[Node, float]) -> Node:
    sp_longest_paths = longest_path_lengths_from_source(SP, cost_map)

    candidate_nodes = [
        node
        for node in g.nodes()
        if node not in SP.nodes()
        and all(parent in SP.nodes() for parent in g.predecessors(node))
    ]

    if not candidate_nodes:
        raise ValueError("No candidate nodes found in g with all parents in SP")

    critical_path_costs = {}
    for node in candidate_nodes:
        parent_costs = [sp_longest_paths[parent] for parent in g.predecessors(node)]
        critical_path_costs[node] = cost_map[node] + (
            max(parent_costs) if parent_costs else 0
        )

    return min(critical_path_costs, key=critical_path_costs.get)


def flexible_sync(
    g: DiGraph, cost_map: dict[Node, float], return_ttsp=False
) -> DiGraph:
    assert is_2_terminal_dag(g) and is_compatible_graph(g)
    SP = DiGraph()
    cost_map = cost_map.copy()
    root: Node = get_only(sources(g))
    SP.add_node(root)
    node = root
    for _ in range(g.number_of_nodes() - 1):
        print(SP.edges)
        node = get_next_node(SP, g, cost_map)
        SP.add_node(node)
        SP.add_edges_from(g.in_edges(node))
        SP = nx.transitive_reduction(SP)

        component: set[Node] = get_component(SP, node)
        handle: Node = lowest_common_ancestor(SP, component)
        forest: set[Node] = get_forest(SP, handle, component)
        print("FOREST", forest)
        up, down, up_frontier, down_frontier = get_up_and_down(
            node, SP, forest, cost_map
        )
        print("UPDOWN", up, down)
        sync = SyncNode()
        cost_map[sync] = 0
        SP.remove_edges_from(edges_to_remove(SP, up, down))
        SP.add_edges_from(edges_to_add(up_frontier, down_frontier, sync))
        for node in list(SP.nodes):
            if isinstance(node, SyncNode) and SP.in_degree(node) == 0:
                SP.remove_node(node)
        for sync_node in list(SP.nodes):
            if isinstance(sync_node, SyncNode):
                in_edges = list(SP.in_edges(sync_node))
                out_edges = list(SP.out_edges(sync_node))

                if len(in_edges) == 1 and len(out_edges) == 1:
                    pred = in_edges[0][0]
                    succ = out_edges[0][1]

                    SP.remove_node(sync_node)
                    SP.add_edge(pred, succ)

    SP = nx.transitive_reduction(SP)
    SP = ttspg_to_spg(SP)
    return SP


# TODO IMPLEMENT the change where all the dependencies of a guy up in the tree are pushed down
