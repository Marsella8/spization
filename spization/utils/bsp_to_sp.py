from multimethod import multimethod

from spization.objects import (
    BinParallel,
    BinSerial,
    Node,
    Parallel,
    Serial,
)
from spization.utils.compositions import sp_parallel_composition, sp_serial_composition


@multimethod
def bsp_to_sp(node: Node) -> Node:
    return node


@multimethod
def bsp_to_sp(bin_par: BinParallel) -> Parallel:
    return sp_parallel_composition((bsp_to_sp(bin_par.t1), bsp_to_sp(bin_par.t2)))


@multimethod
def bsp_to_sp(bin_par: BinSerial) -> Serial:
    return sp_serial_composition((bsp_to_sp(bin_par.t1), bsp_to_sp(bin_par.t2)))
