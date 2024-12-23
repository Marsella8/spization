from dataclasses import dataclass
from typing import Optional

from bidict import bidict
from networkx import DiGraph, MultiDiGraph

from spization.__internals.graph import add_node, sinks, sources
from spization.__internals.sp.cbc_decomposition import (
    BipartiteComponent,
    cbc_decomposition,
    get_component_containing_node_in_head,
    get_component_containing_node_in_tail,
)
from spization.objects import MultiDiEdge, Node


@dataclass
class InverseLineGraphResult:
    graph: MultiDiGraph
    inverse_edge_to_line_node_map: bidict[MultiDiEdge, Node]


def inverse_line_graph(g: DiGraph) -> Optional[InverseLineGraphResult]:
    cbc_decomp = cbc_decomposition(g)
    if cbc_decomp is None:
        return None

    result_graph = MultiDiGraph()
    alpha: Node = add_node(result_graph)
    omega: Node = add_node(result_graph)

    component_nodes = bidict(
        {bi_comp: add_node(result_graph) for bi_comp in cbc_decomp}
    )

    def h(n: Node) -> BipartiteComponent:
        cmp = get_component_containing_node_in_head(cbc_decomp, n)
        assert cmp is not None
        return cmp

    def t(n: Node) -> BipartiteComponent:
        cmp = get_component_containing_node_in_tail(cbc_decomp, n)
        assert cmp is not None
        return cmp

    srcs = sources(g)
    snks = sinks(g)

    def src_for_node(v: Node) -> Node:
        return alpha if v in srcs else component_nodes[t(v)]

    def dst_for_node(v: Node) -> Node:
        return omega if v in snks else component_nodes[h(v)]

    inverse_edge_to_line_node: bidict[MultiDiEdge, Node] = bidict()

    for v in g.nodes:
        src, dst = src_for_node(v), dst_for_node(v)
        idx = result_graph.add_edge(src, dst)
        edge: MultiDiEdge = (src, dst, idx)
        inverse_edge_to_line_node[edge] = v

    return InverseLineGraphResult(result_graph, inverse_edge_to_line_node)
