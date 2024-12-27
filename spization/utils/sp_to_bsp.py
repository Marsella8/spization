from multimethod import multimethod
from multiset import Multiset

from spization.__internals.general import get_any
from spization.objects import (
    BinParallel,
    BinSerial,
    BinSerialParallelDecomposition,
    Node,
    Parallel,
    Serial,
)
from spization.utils.normalize import normalize


@multimethod
def sp_to_bsp(node: Node) -> Node:
    return node


@multimethod
def sp_to_bsp(parallel: Parallel) -> BinSerialParallelDecomposition:
    parallel = normalize(parallel)
    print(parallel)
    if isinstance(parallel, (Node, Serial)):
        return sp_to_bsp(parallel)
    if len(parallel) == 0:
        raise ValueError("Requested sp_to_bsp for Parallel object with 0 nodes")
    t1 = get_any(parallel)
    rest = Parallel(Multiset(parallel) - {t1})
    return BinParallel(sp_to_bsp(t1), sp_to_bsp(rest))


@multimethod
def sp_to_bsp(serial: Serial) -> BinSerialParallelDecomposition:
    serial = normalize(serial)
    if isinstance(serial, (Node, Parallel)):
        return sp_to_bsp(serial)
    if len(serial) == 0:
        raise ValueError("Requested sp_to_bsp for Serial object with 0 nodes")
    t1 = serial[0]
    rest = Serial(serial[1:])
    return BinSerial(sp_to_bsp(t1), sp_to_bsp(rest))
