from networkx import DiGraph

from .serial_parallel_decomposition import SyncNode


def ttspg_to_spg(g: DiGraph) -> DiGraph:
    c = g.copy()

    for node in g.nodes():
        if isinstance(node, SyncNode):
            for pred in list(c.predecessors(node)):
                for succ in list(c.successors(node)):
                    c.add_edge(pred, succ)
            c.remove_node(node)

    return c
