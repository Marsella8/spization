from .compositions import graph_serial_composition, graph_parallel_composition
from .serial_parallel_decomposition import Serial, Parallel, Node
from networkx import DiGraph
from multimethod import multimethod


@multimethod
def sp_to_digraph(node: Node) -> DiGraph:
    g = DiGraph()
    g.add_node(node)
    return g


# TODO: add logic to handle duplicate nodes within SPDs
@multimethod
def sp_to_digraph(parallel: Parallel) -> DiGraph:
    return graph_parallel_composition(sp_to_digraph(sp) for sp in parallel)


@multimethod
def sp_to_digraph(serial: Serial) -> DiGraph:
    return graph_serial_composition(sp_to_digraph(sp) for sp in serial)
