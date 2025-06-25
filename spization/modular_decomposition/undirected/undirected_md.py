from spization.modular_decomposition.undirected.objects import (
    ModularDecompositionTreeUndirected,
    MDParallelUndirected,
    MDSeriesUndirected,
    MDPrimeUndirected,
)
from sage.graphs.graph import Graph as SageGraph
from sage.graphs.graph_decompositions.modular_decomposition import NodeType
from networkx import Graph as NxGraph

def _from_nx_graph_to_sage_graph(G: NxGraph) -> SageGraph:
    """Convert a NetworkX graph to a Sage graph."""
    sage_graph = SageGraph(list(G.edges()))
    # Add any isolated nodes that might not be included in the edge list
    for node in G.nodes():
        sage_graph.add_vertex(node)
    return sage_graph


def _from_sage_md_to_nx_md(md) -> ModularDecompositionTreeUndirected:
    """Convert Sage modular decomposition result to our ModularDecompositionTreeUndirected format."""
    if isinstance(md, int):
        # Leaf node - just return the integer as a node
        return md
    
    if not isinstance(md, tuple) or len(md) != 2:
        raise ValueError(f"Expected tuple of length 2 or int, got {md}")
    
    node_type, children = md
    
    # Convert children recursively
    converted_children = []
    for child in children:
        if isinstance(child, int):
            converted_children.append(child)
        else:
            converted_children.append(_from_sage_md_to_nx_md(child))
    
    children_set = frozenset(converted_children)
    
    if node_type == NodeType.SERIES:
        return MDSeriesUndirected(children_set)
    elif node_type == NodeType.PARALLEL:
        return MDParallelUndirected(children_set)
    elif node_type == NodeType.PRIME:
        return MDPrimeUndirected(children_set)
    else:
        raise ValueError(f"Unknown node type: {node_type}")


def undirected_md(G: NxGraph) -> ModularDecompositionTreeUndirected:
    """Compute modular decomposition of an undirected graph using Sage."""
    sage_graph = _from_nx_graph_to_sage_graph(G)
    sage_md = sage_graph.modular_decomposition()
    md = _from_sage_md_to_nx_md(sage_md)
    return md
