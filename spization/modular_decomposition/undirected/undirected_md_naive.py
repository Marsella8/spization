import networkx as nx

from spization.__internals.general import get_only
from spization.modular_decomposition.undirected.objects import (
    MDParallelUndirected,
    MDPrimeUndirected,
    MDSeriesUndirected,
    ModularDecompositionTreeUndirected,
)
from spization.modular_decomposition.utils import get_maximal_strong_modules


def leaf_modular_decomposition(G: nx.Graph) -> ModularDecompositionTreeUndirected:
    node = get_only(G.nodes())
    return node


def parallel_modular_decomposition(G: nx.Graph) -> ModularDecompositionTreeUndirected:
    children = set()
    for comp in nx.connected_components(G):
        sub = G.subgraph(comp)
        children.add(undirected_md_naive(sub))
    return MDParallelUndirected(children)


def series_modular_decomposition(G: nx.Graph) -> ModularDecompositionTreeUndirected:
    children = set()
    for comp in nx.connected_components(nx.complement(G)):
        sub = G.subgraph(comp)
        children.add(undirected_md_naive(sub))
    return MDSeriesUndirected(children)


def prime_modular_decomposition(G: nx.Graph) -> ModularDecompositionTreeUndirected:
    maximal_strong_modules = get_maximal_strong_modules(G)
    print(maximal_strong_modules)
    components = [G.subgraph(module) for module in maximal_strong_modules]
    children = [undirected_md_naive(component) for component in components]
    return MDPrimeUndirected(children)


def undirected_md_naive(G: nx.Graph) -> ModularDecompositionTreeUndirected:
    nodes = set(G.nodes())
    n = len(nodes)
    assert n > 0

    if n == 1:
        return leaf_modular_decomposition(G)

    if not nx.is_connected(G):
        return parallel_modular_decomposition(G)

    if not nx.is_connected(nx.complement(G)):
        return series_modular_decomposition(G)

    return prime_modular_decomposition(G)
