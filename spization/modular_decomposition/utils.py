from itertools import chain, combinations
from typing import Iterable

import networkx as nx
from multimethod import multimethod
from networkx import DiGraph, Graph

from spization.modular_decomposition.directed.objects import ModularDecompositionTree
from spization.objects import Node

type Module = frozenset[Node]
type StrongModule = frozenset[Node]
type MaximalStrongModule = frozenset[Node]


def is_module(M: set[Node], G: nx.Graph) -> bool:
    """Module: each m in M has a uniform relation with the nodes not in M"""
    if M == set() or M == set(
        G.nodes()
    ):  # conventionally, we dont consider them modules
        return False
    for u in set(G.nodes()) - M:
        nbrs = set(G.adj[u])
        if not (nbrs & M == set() or M.issubset(nbrs)):
            return False
    return True


def is_strong_module(M: Module, modules: frozenset[Module]) -> bool:
    """Strong Module: for each module N, M is either disjoint from N, or subset of N, or superset of N"""
    return all(M.isdisjoint(N) or M.issubset(N) or N.issubset(M) for N in modules)


def is_maximal_strong_module(M: StrongModule, modules: frozenset[StrongModule]) -> bool:
    """Maximal Strong Module: for each strong module N, M is either disjoint from N, or it contains N"""
    return all(M >= N or M & N == set() for N in modules)


def _get_candidate_modules(G: nx.Graph) -> Iterable[Module]:
    nodes = set(G.nodes())
    return map(
        frozenset,
        chain.from_iterable(combinations(nodes, r) for r in range(len(nodes) + 1)),
    )


def get_maximal_strong_modules(G: nx.Graph) -> frozenset[MaximalStrongModule]:
    candidate_modules = _get_candidate_modules(G)
    modules = frozenset(filter(lambda module: is_module(module, G), candidate_modules))
    strong_modules = frozenset(
        filter(lambda module: is_strong_module(module, modules), modules)
    )
    maximal_strong_modules = frozenset(
        filter(
            lambda module: is_maximal_strong_module(module, strong_modules),
            strong_modules,
        )
    )
    return maximal_strong_modules


@multimethod
def have_directed_edge(
    M: ModularDecompositionTree, N: ModularDecompositionTree, G: DiGraph | Graph
) -> bool:
    M = M.nodes if not isinstance(M, Node) else {M}
    N = N.nodes if not isinstance(N, Node) else {N}

    for m in M:
        for n in N:
            if G.has_edge(m, n):
                return True

    return False
