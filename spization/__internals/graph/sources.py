from networkx import DiGraph

from spization.objects import Node


def sources(g: DiGraph) -> set[Node]:
    return {node for node, in_degree in g.in_degree() if in_degree == 0}
