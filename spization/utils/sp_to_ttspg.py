from multimethod import multimethod
from networkx import DiGraph

from spization.objects import Node, Parallel, Serial

from .compositions import graph_parallel_composition


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
def sp_to_digraph(serial: Serial) -> DiGraph: ...
