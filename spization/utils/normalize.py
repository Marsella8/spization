from itertools import filterfalse

from multimethod import multimethod

from spization.__internals.general import get_only
from spization.objects import (
    Node,
    Parallel,
    Serial,
    SerialParallelDecomposition,
)

from .compositions import sp_parallel_composition, sp_serial_composition
from .is_empty import is_empty


@multimethod
def normalize(sp: Parallel) -> SerialParallelDecomposition:
    if is_empty(sp):
        return Parallel()
    children = filterfalse(is_empty, sp.children)
    children = [normalize(c) for c in children]
    if len(children) == 1:
        return get_only(children)
    return sp_parallel_composition(children)


@multimethod
def normalize(sp: Serial) -> SerialParallelDecomposition:
    if is_empty(sp):
        return Serial()
    children = filterfalse(is_empty, sp.children)
    children = [normalize(c) for c in children]
    if len(children) == 1:
        return get_only(children)
    return sp_serial_composition(children)


@multimethod
def normalize(sp: Node) -> SerialParallelDecomposition:
    return sp
