import networkx as nx
from networkx import DiGraph

def sources(G : DiGraph) -> set[int]:
    return {node for node, in_degree in G.in_degree() if in_degree == 0}

def sinks(G : DiGraph) -> set[int]:
    return {node for node, out_degree in G.out_degree() if out_degree == 0}

def is_2_terminal_dag(G : DiGraph) -> bool:
    if not nx.is_directed_acyclic_graph(G):
        return False
    if len(sources(G)) != 1 or len(sinks(G)) != 1:
        return False
    return True

def is_integer_graph(G) -> bool:
    if not all(isinstance(node, int) for node in G.nodes()):
        return False
    return True

def single_source_longest_dag_path_length(graph : DiGraph, s : int) -> dict[int, float]:
    assert(graph.in_degree(s) == 0)
    dist = dict.fromkeys(graph.nodes, -float('inf'))
    dist[s] = 0
    topo_order = nx.topological_sort(graph)
    for n in topo_order:
        if n==s: continue
        dist[n] = 1+max(dist[p] for p in graph.predecessors(n))
    return dist
