import networkx as nx
from multimethod import multimethod
from networkx import DiGraph
from networkx.algorithms import isomorphism as iso

from spization.__internals.graph import is_transitively_closed_dag
from spization.modular_decomposition.directed.directed_md import (
    transitively_closed_dag_md_naive,
)
from spization.modular_decomposition.directed.objects import (
    MDParallel,
    MDPrime,
    MDSeries,
    ModularDecompositionTree,
)
from spization.modular_decomposition.utils import have_directed_edge
from spization.objects import Node

type DirectedQuotientGraph = DiGraph[Node | DirectedQuotientGraph]


def are_equivalent(G: DirectedQuotientGraph, H: DirectedQuotientGraph) -> bool:
    if isinstance(G, Node) and isinstance(H, Node):
        return True
    if isinstance(G, Node) or isinstance(H, Node):
        return False

    if (
        G.number_of_nodes() != H.number_of_nodes()
        or G.number_of_edges() != H.number_of_edges()
    ):
        return False

    gm = iso.DiGraphMatcher(G, H)
    if not gm.is_isomorphic():
        return False
    for u, v in gm.mapping.items():
        if isinstance(u, nx.DiGraph) or isinstance(v, nx.DiGraph):
            if not (isinstance(u, nx.DiGraph) and isinstance(v, nx.DiGraph)):
                return False
            if not are_equivalent(u, v):
                return False
    return True


@multimethod
def _md_todirected_quotient_graph(md: Node, G: DiGraph) -> DirectedQuotientGraph:
    factorized = DiGraph()
    factorized.add_node(md)
    return factorized


@multimethod
def _md_todirected_quotient_graph(md: MDParallel, G: DiGraph) -> DirectedQuotientGraph:
    factorized_children = [
        _md_todirected_quotient_graph(child, G) for child in md.children
    ]

    factorized = DiGraph()
    factorized.add_nodes_from(factorized_children)
    return factorized


@multimethod
def _md_todirected_quotient_graph(md: MDSeries, G: DiGraph) -> DirectedQuotientGraph:
    factorized = DiGraph()

    # Recursively factorize each child
    child_graphs = {}
    for child in md.children:
        child_factorized = _md_todirected_quotient_graph(child, G)
        child_graphs[child] = child_factorized
        factorized.add_node(child_factorized)

    # Add edges between consecutive children in the series
    children_list = list(md.children)
    for i in range(len(children_list) - 1):
        current_child = children_list[i]
        next_child = children_list[i + 1]
        current_graph = child_graphs[current_child]
        next_graph = child_graphs[next_child]
        factorized.add_edge(current_graph, next_graph)

    return factorized


@multimethod
def _md_todirected_quotient_graph(md: MDPrime, G: DiGraph) -> DirectedQuotientGraph:
    factorized = DiGraph()

    # Recursively factorize each child
    child_graphs = {}
    for child in md.children:
        child_factorized = _md_todirected_quotient_graph(child, G)
        child_graphs[child] = child_factorized
        factorized.add_node(child_factorized)

    # Add edges between children based on the original graph relationships
    children_list = list(md.children)
    for i, child1 in enumerate(children_list):
        for j, child2 in enumerate(children_list):
            if i != j and have_directed_edge(child1, child2, G):
                graph1 = child_graphs[child1]
                graph2 = child_graphs[child2]
                factorized.add_edge(graph1, graph2)

    return factorized


def transitively_closed_dag_quotient_graph(G: DiGraph) -> DirectedQuotientGraph:
    assert is_transitively_closed_dag(G)
    md: ModularDecompositionTree = transitively_closed_dag_md_naive(G)
    return _md_todirected_quotient_graph(md, G)
