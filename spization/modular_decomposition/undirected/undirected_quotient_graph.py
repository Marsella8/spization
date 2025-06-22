import networkx as nx
from multimethod import multimethod
from networkx import Graph
from networkx.algorithms import isomorphism as iso

from spization.modular_decomposition import (
    MDParallelUndirected,
    MDPrimeUndirected,
    MDSeriesUndirected,
    undirected_md_naive,
)
from spization.modular_decomposition.utils import have_directed_edge
from spization.objects import Node

type UndirectedQuotientGraph = Graph[Node | UndirectedQuotientGraph]


def are_equivalent(G: UndirectedQuotientGraph, H: UndirectedQuotientGraph) -> bool:
    """Check if two UndirectedQuotientGraph objects are structurally equivalent."""
    if isinstance(G, Node) and isinstance(H, Node):
        return G == H
    if isinstance(G, Node) or isinstance(H, Node):
        return False

    if (
        G.number_of_nodes() != H.number_of_nodes()
        or G.number_of_edges() != H.number_of_edges()
    ):
        return False

    gm = iso.GraphMatcher(G, H)
    if not gm.is_isomorphic():
        return False

    for u, v in gm.mapping.items():
        if isinstance(u, nx.Graph) or isinstance(v, nx.Graph):
            if not (isinstance(u, nx.Graph) and isinstance(v, nx.Graph)):
                return False
            if not are_equivalent(u, v):
                return False
    return True


@multimethod
def _md_to_quotient_graph(md: Node, G: Graph) -> UndirectedQuotientGraph:
    """Convert a single node to its quotient graph representation."""
    quotient = Graph()
    quotient.add_node(md)
    return quotient


@multimethod
def _md_to_quotient_graph(
    md: MDParallelUndirected, G: Graph
) -> UndirectedQuotientGraph:
    """Convert a parallel module to its quotient graph representation."""
    child_quotients = [_md_to_quotient_graph(child, G) for child in md.children]

    quotient = Graph()
    quotient.add_nodes_from(child_quotients)
    return quotient


@multimethod
def _md_to_quotient_graph(md: MDSeriesUndirected, G: Graph) -> UndirectedQuotientGraph:
    """Convert a series module to its quotient graph representation."""
    quotient = Graph()
    child_quotients = {}

    # Create quotient graphs for each child
    for child in md.children:
        child_quotient = _md_to_quotient_graph(child, G)
        child_quotients[child] = child_quotient
        quotient.add_node(child_quotient)

    # Connect consecutive children in series
    children_list = list(md.children)
    for i in range(len(children_list) - 1):
        current_quotient = child_quotients[children_list[i]]
        next_quotient = child_quotients[children_list[i + 1]]
        quotient.add_edge(current_quotient, next_quotient)

    return quotient


@multimethod
def _md_to_quotient_graph(md: MDPrimeUndirected, G: Graph) -> UndirectedQuotientGraph:
    """Convert a prime module to its quotient graph representation."""
    quotient = Graph()
    child_quotients = {}

    # Create quotient graphs for each child
    for child in md.children:
        child_quotient = _md_to_quotient_graph(child, G)
        child_quotients[child] = child_quotient
        quotient.add_node(child_quotient)

    # Connect children based on original graph relationships
    children_list = list(md.children)
    for i, child1 in enumerate(children_list):
        for j, child2 in enumerate(children_list):
            if i < j and have_directed_edge(child1, child2, G):
                quotient1 = child_quotients[child1]
                quotient2 = child_quotients[child2]
                quotient.add_edge(quotient1, quotient2)

    return quotient


def undirected_quotient_graph(G: Graph) -> UndirectedQuotientGraph:
    md = undirected_md_naive(G)
    return _md_to_quotient_graph(md, G)
