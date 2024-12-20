from networkx import DiGraph
from typing import Optional
from collections import deque
from dataclasses import dataclass
from spization.objects import Node
from spization.__internals.graph import sources, sinks


@dataclass(frozen=True)
class BipartiteComponent:
    head_nodes: frozenset[Node]
    tail_nodes: frozenset[Node]


CompleteBipartiteCompositeDecomposition = set[BipartiteComponent]


def is_complete_bipartite_digraph(g: DiGraph) -> bool:
    for source in sources(g):
        for sink in sinks(g):
            if not g.has_edge(source, sink):
                return False
    return True


def cbc_decomposition(g: DiGraph) -> Optional[CompleteBipartiteCompositeDecomposition]:
    edges_to_process = deque(sorted(g.edges()))

    already_in_a_head: set[Node] = set()
    already_in_a_tail: set[Node] = set()
    already_processed: set = set()
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

        subgraph_nodes = head.union(tail)
        subgraph = g.subgraph(subgraph_nodes)

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

        already_processed.update(from_head_to_tail)
        already_in_a_head.update(head)
        already_in_a_tail.update(tail)

    if already_in_a_head.union(already_in_a_tail) != set(g.nodes()):
        return None

    return result


# TODO: finish
