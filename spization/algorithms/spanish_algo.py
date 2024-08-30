from networkx import DiGraph, topological_sort, transitive_reduction
import networkx as nx

def single_source_longest_dag_path_length(graph, s):
    assert(graph.in_degree(s) == 0)
    dist = dict.fromkeys(graph.nodes, -float('inf'))
    dist[s] = 0
    topo_order = nx.topological_sort(graph)
    for n in topo_order:
        if n==s: continue
        dist[n] = 1+max(dist[p] for p in graph.predecessors(n))
    return dist

def get_subtree(G, root):
    return set(nx.descendants(G, root)) | {root}

def spanish_algo(G: DiGraph):
    SP = DiGraph()
    s = next(node for node, in_degree in G.in_degree() if in_degree == 0)
    SP.add_node(s)
    for node in list(topological_sort(G))[1:]:
        SP.add_node(node)
        SP.add_edges_from(G.in_edges(node))
        SP = transitive_reduction(SP)
        sssp = single_source_longest_dag_path_length(SP, s)
        S = DiGraph(G.subgraph([n for n in SP.nodes() if sssp[n] in [sssp[node], sssp[node] - 1]]))
        
        wcc = nx.weakly_connected_components(S)
        component = next(c for c in wcc if node in c)
        
        lca = next(iter(component))
        for c in component:
            lca = nx.lowest_common_ancestor(G, lca, c)
        subtrees = [get_subtree(SP, succ) for succ in SP.successors(lca)]        
        valid_subtrees = [subtree for subtree in subtrees if subtree & component]
        forest = set().union(*valid_subtrees)
        mx = max(sssp.values())
        down = [node for node in forest if sssp[node] == mx]
        up = [node for node in forest if sssp[node] == mx-1]

        for u in up:
            for d in down:
                SP.add_edge(u, d)
        print(node, forest, lca, down)

    return SP

# Test the algorithm
edges = [(1, 2), (1, 3), (2, 4), (2, 5), (3, 5), (4, 6), (5, 6), (6, 7), (6, 8)]
G = nx.DiGraph(edges)
result = spanish_algo(G)
print("Nodes:", result.nodes())
print("Edges:", result.edges())



edges = [
    (1, 2), (1, 3),
    (2, 4), (2, 5),
    (3, 11), (3, 12), (3, 13),
    (4, 6), (4, 7),
    (5, 7), (5, 8), (5, 11),
    (6, 9),
    (7, 9), (7, 10),
    (8, 9),
    (9, 18),
    (10, 18), (10, 11),
    (11, 17),
    (12, 17),
    (13, 15), (13, 14),
    (14, 16),
    (15, 16),
    (16, 17),
    (17, 18)
]
G = nx.DiGraph(edges)
result = spanish_algo(G)
print("Nodes:", result.nodes())
print("Edges:", result.edges())

