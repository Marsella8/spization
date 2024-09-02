from spization.utils.sp.serial_parallel_decomposition import Node
from networkx import DiGraph


def sources(g: DiGraph) -> set[Node]:
    return {node for node, in_degree in g.in_degree() if in_degree == 0}
