from __future__ import annotations

from functools import cmp_to_key

import networkx as nx
from multimethod import multimethod

from spization.__internals.graph.properties import is_transitively_closed_dag
from spization.modular_decomposition.directed.objects import (
    MDParallel,
    MDPrime,
    MDSeries,
    ModularDecompositionTree,
)
from spization.modular_decomposition.undirected.objects import (
    MDParallelUndirected,
    MDPrimeUndirected,
    MDSeriesUndirected,
    ModularDecompositionTreeUndirected,
)
from spization.modular_decomposition.undirected.undirected_md_naive import (
    undirected_md_naive,
)
from spization.objects.nodes import Node


def _nodes(module: ModularDecompositionTree) -> frozenset[Node]:
    if isinstance(module, Node):
        return {module}
    return module.nodes


def _module_precedes(
    m1: ModularDecompositionTree, m2: ModularDecompositionTree, G: nx.DiGraph
) -> bool:
    nodes_m1 = _nodes(m1)
    nodes_m2 = _nodes(m2)

    for n1 in nodes_m1:
        descendants_n1 = nx.descendants(G, n1)
        if nodes_m2 & descendants_n1:
            return True
    return False


def _get_topological_order(
    modules: frozenset[ModularDecompositionTree], G: nx.DiGraph
) -> list[ModularDecompositionTree]:
    return sorted(
        modules,
        key=cmp_to_key(
            lambda m1, m2: -1
            if _module_precedes(m1, m2, G)
            else (1 if _module_precedes(m2, m1, G) else 0)
        ),
    )


@multimethod
def undirected_md_to_directed_md(md: Node, G: nx.DiGraph) -> Node:
    return md


@multimethod
def undirected_md_to_directed_md(md: MDParallelUndirected, G: nx.DiGraph) -> MDParallel:
    converted_children = [
        undirected_md_to_directed_md(child, G) for child in md.children
    ]
    return MDParallel(converted_children)


@multimethod
def undirected_md_to_directed_md(md: MDPrimeUndirected, G: nx.DiGraph) -> MDPrime:
    converted_children = [
        undirected_md_to_directed_md(child, G) for child in md.children
    ]
    return MDPrime(converted_children)


@multimethod
def undirected_md_to_directed_md(md: MDSeriesUndirected, G: nx.DiGraph) -> MDSeries:
    converted_children = (
        undirected_md_to_directed_md(child, G) for child in md.children
    )
    converted_children = frozenset(
        child for child in converted_children if child is not None
    )
    ordered_children = _get_topological_order(converted_children, G)
    return MDSeries(ordered_children)


@multimethod
def undirected_md_to_directed_md(
    md: ModularDecompositionTreeUndirected, G: nx.DiGraph
) -> ModularDecompositionTree:
    """Disclaimer! This is not a general method (i.e. ModularDecompositionTreeUndirected and ModularDecompositionTree are pretty differernt, this only makes sense when we are mapping the Undirected MD of the undirected view of a transitively closed graph"""
    return undirected_md_to_directed_md(md, G)


def transitively_closed_dag_md_naive(G: nx.DiGraph) -> ModularDecompositionTree:
    assert is_transitively_closed_dag(G)
    uG = G.to_undirected()
    undirected_md = undirected_md_naive(uG)
    return undirected_md_to_directed_md(undirected_md, G)
