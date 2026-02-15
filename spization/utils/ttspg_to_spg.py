from typing import Mapping

from networkx import DiGraph

from spization.objects import Node, NodeRole


def contract_out_nodes_of_role(
    g: DiGraph, role: NodeRole, node_roles: Mapping[Node, NodeRole]
) -> DiGraph:
    c = g.copy()

    for node in list(g.nodes()):
        if node_roles[node] == role:
            for pred in list(c.predecessors(node)):
                for succ in list(c.successors(node)):
                    c.add_edge(pred, succ)
            c.remove_node(node)

    return c


def ttspg_to_spg(g: DiGraph, node_roles: Mapping[Node, NodeRole]) -> DiGraph:
    assert set(node_roles.keys()) == set(g.nodes())
    return contract_out_nodes_of_role(g, NodeRole.SYNC, node_roles)
