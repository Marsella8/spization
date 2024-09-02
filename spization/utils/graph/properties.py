from networkx import DiGraph
import networkx as nx
from spization.utils.sp.serial_parallel_decomposition import PureNode
from spization.utils.graph.sinks import sinks
from spization.utils.graph.sources import sources


def is_2_terminal_dag(g: DiGraph) -> bool:
    if not nx.is_directed_acyclic_graph(g):
        return False

    return len(sources(g)) == 1 and len(sinks(g)) == 1


def is_compatible_graph(g: DiGraph) -> bool:
    return all(isinstance(node, PureNode) for node in g.nodes())


def is_single_sourced(g: DiGraph) -> bool:
    return len(sources(g)) == 1
