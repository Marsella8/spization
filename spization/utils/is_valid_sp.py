from multimethod import multimethod
from networkx import DiGraph, ancestors

from spization.objects import SerialParallelDecomposition

from .ancestors import get_ancestors
from .nodes import get_nodes


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


# TODO: how to change this to account for duplicate nodes, might be fine already
