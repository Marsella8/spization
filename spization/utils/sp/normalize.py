from itertools import filterfalse

from multimethod import multimethod

from spization.utils.general import get_only

from .compositions import sp_parallel_composition, sp_serial_composition
from .is_empty import is_empty
from .serial_parallel_decomposition import (
    Node,
    Parallel,
    Serial,
    SerialParallelDecomposition,
)


@multimethod
def normalize(sp: Parallel) -> SerialParallelDecomposition:
    if is_empty(sp):
        return sp
    if len(sp) == 1:
        return get_only(sp)
    children = filterfalse(is_empty, sp.children)
    children = [normalize(c) for c in children]
    return sp_parallel_composition(children)


@multimethod
def normalize(sp: Serial) -> SerialParallelDecomposition:
    if is_empty(sp):
        return sp
    if len(sp) == 1:
        return get_only(sp)
    children = filterfalse(is_empty, sp.children)
    children = [normalize(c) for c in children]
    return sp_serial_composition(children)


@multimethod
def normalize(sp: Node) -> SerialParallelDecomposition:
    return sp
