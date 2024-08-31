from networkx import ancestors, DiGraph
from .serial_parallel_decomposition import SerialParallelDecomposition
from .nodes import get_nodes
from .ancestors import get_ancestors
from multimethod import multimethod


@multimethod
def is_valid_sp(g: DiGraph, sp: SerialParallelDecomposition) -> bool:
    if set(g.nodes()) != get_nodes(sp):
        return False
    for node in get_nodes(sp):
        if not (ancestors(g, node) <= get_ancestors(sp, node)):
            return False
    return True


@multimethod
def is_valid_sp(g: DiGraph, sp: DiGraph) -> bool:
    if set(g.nodes()) != set(sp.nodes()):
        return False
    for node in sp.nodes():
        if not (ancestors(g, node) <= ancestors(sp, node)):
            return False
    return True
