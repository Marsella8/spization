import networkx as nx
from networkx import DiGraph

from spization.objects import PureNode

from .sinks import sinks
from .sources import sources


def is_2_terminal_dag(g: DiGraph) -> bool:
    if not nx.is_directed_acyclic_graph(g):
        return False

    return len(sources(g)) == 1 and len(sinks(g)) == 1


def is_compatible_graph(g: DiGraph) -> bool:
    return all(isinstance(node, PureNode) for node in g.nodes())


def is_single_sourced(g: DiGraph) -> bool:
    return len(sources(g)) == 1


def is_transitively_closed(g: DiGraph) -> bool:
    for node in g.nodes():
        for descendant in nx.descendants(g, node):
            if not g.has_edge(node, descendant):
                return False
    return True


def is_transitively_closed_dag(g: DiGraph) -> bool:
    return nx.is_directed_acyclic_graph(g) and is_transitively_closed(g)
