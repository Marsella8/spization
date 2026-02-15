from networkx import Graph as NxGraph
from sage.graphs.graph import Graph as SageGraph
from sage.graphs.graph_decompositions.modular_decomposition import (  # ty: ignore[unresolved-import]
    NodeType,
)

from spization.modular_decomposition.undirected.objects import (
    MDParallelUndirected,
    MDPrimeUndirected,
    MDSeriesUndirected,
    ModularDecompositionTreeUndirected,
)


def _from_nx_graph_to_sage_graph(G: NxGraph) -> SageGraph:
    sage_graph = SageGraph(list(G.edges()))
    for node in G.nodes():
        sage_graph.add_vertex(node)
    return sage_graph


def _from_sage_md_to_nx_md(md) -> ModularDecompositionTreeUndirected:
    if isinstance(md, int):
        return md
    
    if not isinstance(md, tuple) or len(md) != 2:
        raise ValueError(f"Expected tuple of length 2 or int, got {md}")
    
    node_type, children = md
    
    converted_children = []
    for child in children:
        if isinstance(child, int):
            converted_children.append(child)
        else:
            converted_children.append(_from_sage_md_to_nx_md(child))
    
    children_set = frozenset(converted_children)
    match node_type:
        case NodeType.SERIES:
            return MDSeriesUndirected(children_set)
        case NodeType.PARALLEL:
            return MDParallelUndirected(children_set)
        case NodeType.PRIME:
            return MDPrimeUndirected(children_set)
        case _:
            raise ValueError(f"Unknown node type: {node_type}")

def undirected_md(G: NxGraph) -> ModularDecompositionTreeUndirected:
    sage_graph = _from_nx_graph_to_sage_graph(G)
    sage_md = sage_graph.modular_decomposition()
    md = _from_sage_md_to_nx_md(sage_md)
    return md
