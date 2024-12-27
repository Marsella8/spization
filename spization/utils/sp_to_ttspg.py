from multimethod import multimethod
from networkx import DiGraph

from spization.objects import (
    Node,
    Parallel,
    Serial,
    SyncNode,
)

from .compositions import graph_parallel_composition, graph_serial_composition
from .has_no_duplicate_nodes import has_no_duplicate_nodes


@multimethod
def sp_to_ttspg(node: Node) -> DiGraph:
    g = DiGraph()
    g.add_node(node)
    return g


@multimethod
def sp_to_ttspg(parallel: Parallel) -> DiGraph:
    assert has_no_duplicate_nodes(parallel)
    return graph_parallel_composition([sp_to_ttspg(sp) for sp in parallel])


@multimethod
def sp_to_ttspg(serial: Serial) -> DiGraph:
    assert has_no_duplicate_nodes(serial)
    zipped = zip(serial.children, (SyncNode() for _ in range(len(serial))))
    children = [a for z in zipped for a in z][:-1]
    if isinstance(children[0], Parallel):
        children.insert(0, SyncNode())
    if isinstance(children[-1], Parallel):
        children.append(SyncNode())
    return graph_serial_composition([sp_to_ttspg(sp) for sp in children])
