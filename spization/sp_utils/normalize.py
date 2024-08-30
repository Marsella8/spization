from .serial_parallel_decomposition import SerialParallelDecomposition, Serial, Parallel
from multimethod import multimethod
from itertools import filterfalse
from .is_empty import is_empty
from .compositions import sp_parallel_composition, sp_serial_composition
from spization.utils.general_utils import get_only


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
def normalize(sp: int) -> SerialParallelDecomposition:
    return sp
