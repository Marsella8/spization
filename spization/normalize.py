from serial_parallel_decomposition import SerialParallelDecomposition, Serial, Parallel
from multipledispatch import dispatch as overload
from utilities import is_empty, get_nodes, serial_composition, parallel_composition
from itertools import filterfalse
@overload(Parallel)
def normalize(sp : Parallel) -> SerialParallelDecomposition:
    if is_empty(sp): return sp
    if len(get_nodes(sp)) == 1:
        return get_nodes(sp).pop()
    children = filterfalse(is_empty, sp.children)
    children = map(normalize, children)
    return parallel_composition(children)


@overload(Serial)
def normalize(sp : Serial) -> SerialParallelDecomposition:
    if is_empty(sp): return sp
    if len(get_nodes(sp)) == 1:
        return get_nodes(sp).pop()
    children = filterfalse(is_empty, sp.children)
    children = map(normalize, children)
    return serial_composition(children)


@overload(int)
def normalize(sp : int) -> SerialParallelDecomposition:
    return sp