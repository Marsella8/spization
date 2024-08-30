from networkx import DiGraph, topological_sort, transitive_reduction
import networkx as nx
from spization.utils.graph import single_source_longest_dag_path_length
from spization.utils.utils import get_only
from spization.utils.graph import sources


def get_subtree(G: DiGraph, root: int) -> set[int]:
    return set(nx.descendants(G, root)) | {root}


def spanish_algo(G: DiGraph) -> DiGraph:
    SP = DiGraph()
    s: int = get_only(sources(G))
    SP.add_node(s)
    for node in list(topological_sort(G))[1:]:
        SP.add_node(node)
        SP.add_edges_from(G.in_edges(node))
        SP = transitive_reduction(SP)
        sssp = single_source_longest_dag_path_length(SP, s)
        S = DiGraph(
            G.subgraph(
                [n for n in SP.nodes() if sssp[n] in [sssp[node], sssp[node] - 1]]
            )
        )

        component: set[int] = get_only(
            c for c in nx.weakly_connected_components(S) if node in c
        )

        lca = next(iter(component))
        for c in component:
            lca = nx.lowest_common_ancestor(G, lca, c)
        subtrees = [get_subtree(SP, succ) for succ in SP.successors(lca)]
        valid_subtrees = [subtree for subtree in subtrees if subtree & component]
        forest = set().union(*valid_subtrees)
        mx = max(sssp.values())
        down = [node for node in forest if sssp[node] == mx]
        up = [node for node in forest if sssp[node] == mx - 1]

        for u in up:
            for d in down:
                SP.add_edge(u, d)
        print(node, forest, lca, down)

    return SP
