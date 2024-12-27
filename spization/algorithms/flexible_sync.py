import itertools
import random

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
    spg_to_sp,
    ttspg_to_spg,
)


def get_component(SP: DiGraph, node: Node) -> set[Node]:
    parents = set(SP.predecessors(node))
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
    main_node: Node, SP: DiGraph, forest: set[Node], cost_map: dict[Node, float]
) -> tuple[set[Node], set[Node]]:
    SP: DiGraph = ttspg_to_spg(SP)

    base_up = {main_node}
    base_down = set(SP.predecessors(main_node))
    assert all(p in forest for p in base_down)
    assignable_nodes = forest - (base_up | base_down)

    def random_subsets(assignable_nodes):
        s = sorted(assignable_nodes)
        while True:
            r = random.randint(0, len(s))
            subset = random.sample(s, r)
            yield subset

    bipartitions = set()
    for subset in itertools.islice(random_subsets(assignable_nodes), 10000):
        subset = set(subset) | base_up  # up
        complement = (assignable_nodes | base_down) - subset  # down
        assert (subset & complement == set()) and (subset | complement == forest)
        bipartitions.add((frozenset(subset), frozenset(complement)))
        bipartitions.add((frozenset(complement), frozenset(subset)))

    def is_valid_bipartition(up: set[Node], down: set[Node]) -> bool:
        if main_node not in down:
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

    def partition_cost(partition: tuple[set[Node], set[Node]]) -> float:
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


def get_next_node(SP: DiGraph, g: DiGraph, cost_map: dict[Node, float]) -> Node:
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

    return min(
        critical_path_costs.keys(),
        key=lambda node: (critical_path_costs.get(node), node),
    )  # split ties with smallest node, for testing purposes


# TODO: remove in_single_sourced restruiction by adding dummy node
def flexible_sync(g: DiGraph, cost_map: dict[Node, float]) -> DiGraph:
    assert is_single_sourced(g) and is_compatible_graph(g)
    g = nx.transitive_reduction(g)
    SP = DiGraph()
    cost_map = cost_map.copy()
    root: Node = get_only(sources(g))
    SP.add_node(root)
    node = root
    for _ in range(g.number_of_nodes() - 1):
        node = get_next_node(SP, g, cost_map)
        SP.add_node(node)
        SP.add_edges_from(g.in_edges(node))

        component: set[Node] = get_component(SP, node)
        handle: Node = lowest_common_ancestor(SP, component)
        forest: set[Node] = get_forest(SP, handle, component)
        up, down, up_frontier, down_frontier = get_up_and_down(
            node, SP, forest, cost_map
        )
        # print(f"{component=}")
        # print(f"{handle=}")
        # print(f"{forest=}")
        # print(f"{up=}, {down=}")
        sync = SyncNode()
        cost_map[sync] = 0
        SP.remove_edges_from(edges_to_remove(SP, up, down))
        SP.add_edges_from(edges_to_add(up_frontier, down_frontier, sync))
    SP = ttspg_to_spg(SP)
    decomp = spg_to_sp(SP)
    assert decomp is not None
    return decomp


# TODO ? IMPLEMENT the change where all the dependencies of a guy up in the tree are pushed down
