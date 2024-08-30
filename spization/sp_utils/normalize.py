from .serial_parallel_decomposition import SerialParallelDecomposition, Serial, Parallel
from multimethod import multimethod
from itertools import filterfalse
from .is_empty import is_empty
from .compositions import parallel_composition, serial_composition
from .nodes import get_nodes

@multimethod
def normalize(sp : Parallel) -> SerialParallelDecomposition:
    if is_empty(sp): return sp
    if len(get_nodes(sp)) == 1:
        return get_nodes(sp).pop()
    children = filterfalse(is_empty, sp.children)
    children = [normalize(c) for c in children]
    return parallel_composition(children)


@multimethod
def normalize(sp : Serial) -> SerialParallelDecomposition:
    if is_empty(sp): return sp
    if len(get_nodes(sp)) == 1:
        return get_nodes(sp).pop()
    children = filterfalse(is_empty, sp.children)
    children = [normalize(c) for c in children]
    return serial_composition(children)

@multimethod
def normalize(sp : int) -> SerialParallelDecomposition:
    return sp
