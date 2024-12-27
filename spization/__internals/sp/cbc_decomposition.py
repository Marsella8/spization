from collections import deque
from dataclasses import dataclass
from typing import Optional

from networkx import DiGraph

from spization.__internals.general import get_only
from spization.__internals.graph import sinks, sources
from spization.objects import DiEdge, Node


@dataclass(frozen=True)
class BipartiteComponent:
    head_nodes: frozenset[Node]
    tail_nodes: frozenset[Node]


CompleteBipartiteCompositeDecomposition = set[BipartiteComponent]


def is_complete_bipartite_digraph(g: DiGraph, head: frozenset[Node]) -> bool:
    sinks = set(g.nodes) - head
    for source in head:
        for sink in sinks:
            if not g.has_edge(source, sink):
                return False
    return True


def cbc_decomposition(g: DiGraph) -> Optional[CompleteBipartiteCompositeDecomposition]:
    edges_to_process = deque(sorted(g.edges()))

    already_in_a_head: set[Node] = set()
    already_in_a_tail: set[Node] = set()
    already_processed: set[DiEdge] = set()
    result: CompleteBipartiteCompositeDecomposition = set()

    while edges_to_process:
        e = edges_to_process.pop()
        if e in already_processed:
            continue

        head = frozenset(g.predecessors(e[1]))
        tail = frozenset(g.successors(e[0]))

        if head & tail:
            return None

        from_head_to_tail = {(u, v) for u in head for v in tail if g.has_edge(u, v)}

        subgraph = g.subgraph(head | tail)

        if not is_complete_bipartite_digraph(subgraph, head):
            return None

        for u, v in subgraph.edges():
            if (u, v) not in from_head_to_tail:
                return None

        out_edges = {(u, v) for u in head for v in g.successors(u)}
        if out_edges != from_head_to_tail:
            return None

        in_edges = {(u, v) for v in tail for u in g.predecessors(v)}
        if in_edges != from_head_to_tail:
            return None

        result.add(BipartiteComponent(head, tail))

        already_processed |= from_head_to_tail
        already_in_a_head.update(head)
        already_in_a_tail.update(tail)

    assert already_in_a_head == set(g.nodes) - sinks(g)
    assert already_in_a_tail == set(g.nodes) - sources(g)

    return result


def get_component_containing_node_in_head(
    cbc: CompleteBipartiteCompositeDecomposition, n: Node
) -> Optional[BipartiteComponent]:
    found: set[BipartiteComponent] = set(filter(lambda bc: n in bc.head_nodes, cbc))
    assert len(found) <= 1
    return get_only(found) if found else None


def get_component_containing_node_in_tail(
    cbc: CompleteBipartiteCompositeDecomposition, n: Node
) -> Optional[BipartiteComponent]:
    found: set[BipartiteComponent] = set(filter(lambda bc: n in bc.tail_nodes, cbc))
    assert len(found) <= 1
    return get_only(found) if found else None
