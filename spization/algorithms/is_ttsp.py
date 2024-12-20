import networkx as nx
from networkx import DiGraph
from typing import Optional
from spization.objects import Node
from spization.__internals.general import get_only

Edge = tuple[Node, Node]


def find_serial_split(g: DiGraph) -> Optional[tuple[Edge, Edge]]:
    for node in list(g.nodes()):
        if g.in_degree(node) == 1 and g.out_degree(node) == 1:
            incoming_edge = get_only(g.in_edges(node))
            outgoing_edge = get_only(g.out_edges(node))
            return (incoming_edge, outgoing_edge)
    return None


def find_parallel_split(g: DiGraph) -> Optional[tuple[Node, Node, Node]]:
    for n1 in g.nodes():
        p = list(g.predecessors(n1))
        s = list(g.successors(n1))
        if len(p) == 1 and len(s) == 1:
            return (get_only(p), Node, get_only(s))
    return None


def is_ttsp(g: DiGraph) -> bool:
    reduced_graph = g.copy()

    while True:
        maybe_serial_split = find_serial_split(reduced_graph)
        if maybe_serial_split is not None:
            (u, v), (w, x) = maybe_serial_split
            intermediate_node = v
            reduced_graph.remove_node(intermediate_node)
            reduced_graph.add_edge(u, x)

            continue

        maybe_parallel_split = find_parallel_split(reduced_graph)
        if maybe_parallel_split is not None:
            src, dest, intermediate_node = maybe_parallel_split
            edges_to_remove = [
                edge for edge in reduced_graph.out_edges(src) if edge[1] == dest
            ]
            reduced_graph.remove_edge(edges_to_remove[0][0], edges_to_remove[0][1])

            continue

        if maybe_parallel_split is None and maybe_serial_split is None:
            break

    return (reduced_graph.number_of_nodes() == 2) and (
        reduced_graph.number_of_edges() == 1
    )
