from itertools import groupby
from typing import Iterator, Sequence

import networkx as nx
from networkx import DiGraph

from spization.__internals.general import get_only
from spization.__internals.graph import (
    is_2_terminal_dag,
    is_compatible_graph,
    sinks,
    sources,
)
from spization.objects import (
    Node,
    Serial,
    SerialParallelDecomposition,
)
from spization.utils import normalize, sp_parallel_composition, sp_serial_composition


def tree_pure_node_dup(g: DiGraph) -> SerialParallelDecomposition:
    assert is_2_terminal_dag(g) and is_compatible_graph(g)
    root = get_only(sources(g))
    node_to_sp: dict[Node, SerialParallelDecomposition] = {root: root}
    for node in nx.topological_sort(g):
        if node == root:
            continue
        predecessors: Iterator[Node] = g.predecessors(node)
        node_to_sp[node] = normalize(
            sp_serial_composition(
                (
                    sp_parallel_composition(node_to_sp[p] for p in predecessors),
                    node,
                )
            )
        )
    sink: Node = get_only(sinks(g))
    final: SerialParallelDecomposition = normalize(node_to_sp[sink])
    return final


def sp_parallel_composition_with_coalescing(
    elements: Sequence[Serial | Node],
) -> SerialParallelDecomposition:
    if len(elements) == 1:
        sp: SerialParallelDecomposition = get_only(elements)
        return sp

    def get_head(sp: Serial | Node) -> SerialParallelDecomposition:
        return sp if isinstance(sp, Node) else sp[0]

    def cut_off_head(sp: SerialParallelDecomposition) -> Serial:
        if isinstance(sp, Node):
            return Serial([])
        elif isinstance(sp, Serial):
            return sp[1:]
        raise TypeError

    groups = groupby(elements, key=get_head)

    result = []
    for head, group in groups:
        tails = [cut_off_head(e) for e in group]
        non_empty_tails: Sequence[Serial] = [t for t in tails if t]
        if not non_empty_tails:
            result.append(head)
        else:
            coalesced_tails = sp_parallel_composition_with_coalescing(non_empty_tails)
            result.append(normalize(sp_serial_composition((head, coalesced_tails))))

    sp: SerialParallelDecomposition = normalize(sp_parallel_composition(result))
    return sp


def pure_node_dup(g: DiGraph) -> SerialParallelDecomposition:
    assert is_2_terminal_dag(g) and is_compatible_graph(g)
    root = get_only(sources(g))
    node_to_sp: dict[Node, Serial | Node] = {root: root}
    for node in nx.topological_sort(g):
        if node == root:
            continue
        predecessors: Iterator[Node] = g.predecessors(node)
        node_to_sp[node] = normalize(
            sp_serial_composition(
                (
                    sp_parallel_composition_with_coalescing(
                        [node_to_sp[p] for p in predecessors]
                    ),
                    node,
                )
            )
        )
    sink: Node = get_only(sinks(g))
    final: SerialParallelDecomposition = normalize(node_to_sp[sink])
    return final
