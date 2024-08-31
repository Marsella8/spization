from .compositions import graph_serial_composition, graph_parallel_composition
from .serial_parallel_decomposition import Serial, Parallel, Node
from networkx import DiGraph
from multimethod import multimethod


@multimethod
def digraph_from_sp(node: Node) -> DiGraph:
    g = DiGraph()
    g.add_node(node)
    return g


@multimethod
def digraph_from_sp(parallel: Parallel) -> DiGraph:
    return graph_parallel_composition(digraph_from_sp(sp) for sp in parallel)


@multimethod
def digraph_from_sp(serial: Serial) -> DiGraph:
    return graph_serial_composition(digraph_from_sp(sp) for sp in serial)
