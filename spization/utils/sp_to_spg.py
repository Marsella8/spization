from multimethod import multimethod
from networkx import DiGraph

from spization.objects import Node, Parallel, Serial

from .compositions import graph_parallel_composition, graph_serial_composition
from .has_no_duplicate_nodes import has_no_duplicate_nodes


@multimethod
def sp_to_spg(node: Node) -> DiGraph:
    g = DiGraph()
    g.add_node(node)
    return g


@multimethod
def sp_to_spg(parallel: Parallel) -> DiGraph:
    assert has_no_duplicate_nodes(parallel)
    return graph_parallel_composition(sp_to_spg(sp) for sp in parallel)


@multimethod
def sp_to_spg(serial: Serial) -> DiGraph:
    assert has_no_duplicate_nodes(serial)
    return graph_serial_composition(sp_to_spg(sp) for sp in serial)
