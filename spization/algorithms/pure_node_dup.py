from typing import Iterator, Sequence
from networkx import DiGraph
import networkx as nx
from spization import (
    SerialParallelDecomposition,
    Serial,
    Node,
)
from spization.utils.sp.compositions import (
    sp_serial_composition,
    sp_parallel_composition,
)
from spization.utils.sp.normalize import normalize
from spization.utils.graph import sources, sinks
from spization.utils.graph import is_2_terminal_dag, is_integer_graph

from itertools import groupby
from spization.utils.general import get_only


def tree_pure_node_dup(g: DiGraph) -> SerialParallelDecomposition:
    assert is_2_terminal_dag(g) and is_integer_graph(g)
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
        match sp:
            case Node():
                return Serial([])
            case Serial():
                return sp[1:]
            case _:
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
    assert is_2_terminal_dag(g) and is_integer_graph(g)
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
