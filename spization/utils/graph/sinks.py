from networkx import DiGraph
from spization.utils.sp.serial_parallel_decomposition import Node


def sinks(g: DiGraph) -> set[Node]:
    return {node for node, out_degree in g.out_degree() if out_degree == 0}
