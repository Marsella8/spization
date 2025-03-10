from networkx import DiGraph

from spization.objects import SyncNode


def ttspg_to_spg(g: DiGraph) -> DiGraph:
    c = g.copy()

    for node in g.nodes():
        if isinstance(node, SyncNode):
            for pred in list(c.predecessors(node)):
                for succ in list(c.successors(node)):
                    c.add_edge(pred, succ)
            c.remove_node(node)

    return c


# TODO put the conversions into their own thing
