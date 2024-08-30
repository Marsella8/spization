from sp_utilities import serial_composition, parallel_composition
from spization.sp_utils.serial_parallel_decomposition import SerialParallelDecomposition, Serial, Parallel
from networkx import DiGraph

def digraph_from_sp(node : int):
    g = DiGraph()
    g.add_node(node)
    return g

def digraph_from_sp(parallel : Parallel):
    return parallel_composition(digraph_from_sp(sp) for sp in parallel)

def digraph_from_sp(serial : Serial):
    return serial_composition(digraph_from_sp(sp) for sp in serial)
