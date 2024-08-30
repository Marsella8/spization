from sp_utilities import serial_composition, parallel_composition
from spization.sp_utils.serial_parallel_decomposition import SerialParallelDecomposition, Serial, Parallel
from networkx import DiGraph
from multimethod import multimethod

@multimethod
def digraph_from_sp(node : int) -> DiGraph:
    g = DiGraph()
    g.add_node(node)
    return g

@multimethod
def digraph_from_sp(parallel : Parallel) -> DiGraph:
    return parallel_composition(digraph_from_sp(sp) for sp in parallel)

@multimethod
def digraph_from_sp(serial : Serial) -> DiGraph:
    return serial_composition(digraph_from_sp(sp) for sp in serial)
