from dataclasses import dataclass
from typing import Optional

import bidict
import networkx as nx
from networkx import DiGraph, MultiDiGraph

from spization.__internals.general import get_only
from spization.__internals.sp.inverse_line_graph import inverse_line_graph
from spization.objects import DiEdge, MultiDiEdge, Node, SerialParallelDecomposition
from spization.utils.compositions import sp_parallel_composition, sp_serial_composition


@dataclass
class ParallelReduction:
    e1: MultiDiEdge
    e2: MultiDiEdge

    def __post_init__(self) -> None:
        # for edge commutativity
        if self.e1 > self.e2:
            self.e1, self.e2 = self.e2, self.e1


@dataclass
class SeriesReduction:
    fst: MultiDiEdge
    snd: MultiDiEdge

    def __post__init__(self) -> None:
        if self.fst[1] != self.snd[0]:
            raise ValueError(
                f"SeriesReduction({self.fst},{self.snd}) must have same center node"
            )


def find_parallel_reduction(mg: MultiDiGraph) -> Optional[ParallelReduction]:
    seen: dict[DiEdge, MultiDiEdge] = {}
    for u, v, key in mg.edges(keys=True):
        directed_edge = (u, v)
        if directed_edge in seen:
            return ParallelReduction(seen[directed_edge], (u, v, key))
        seen[directed_edge] = (u, v, key)
    return None


def find_series_reduction(mg: MultiDiGraph) -> Optional[SeriesReduction]:
    for node in mg.nodes():
        in_edges = list(mg.in_edges(node, keys=True))
        out_edges = list(mg.out_edges(node, keys=True))

        if len(in_edges) == 1 and len(out_edges) == 1:
            u, v, in_key = get_only(in_edges)
            v, w, out_key = get_only(out_edges)
            return SeriesReduction((u, v, in_key), (v, w, out_key))

    return None


def apply_parallel_reduction(mg: MultiDiGraph, r: ParallelReduction) -> MultiDiEdge:
    mg.remove_edge(*r.e1)
    return r.e2


def apply_series_reduction(mg: MultiDiGraph, r: SeriesReduction) -> MultiDiEdge:
    pre = r.fst[0]
    center = r.fst[1]
    post = r.snd[1]

    mg.remove_node(center)
    idx = mg.add_edge(pre, post)
    return (pre, post, idx)


def spg_to_sp(
    g: DiGraph,
) -> Optional[SerialParallelDecomposition]:
    g = nx.transitive_reduction(g)

    inverse_line_graph_result = inverse_line_graph(g)
    if inverse_line_graph_result is None:
        return None
    ttsp: MultiDiGraph = inverse_line_graph_result.graph
    ttsp_edge_to_sp_tree: bidict[MultiDiEdge, Node] = (
        inverse_line_graph_result.inverse_edge_to_line_node_map
    )
    while True:
        parallel_reduction = find_parallel_reduction(ttsp)
        if parallel_reduction:
            e1, e2 = parallel_reduction.e1, parallel_reduction.e2
            merged: MultiDiEdge = apply_parallel_reduction(ttsp, parallel_reduction)
            new_tree: SerialParallelDecomposition = sp_parallel_composition(
                (ttsp_edge_to_sp_tree[e1], ttsp_edge_to_sp_tree[e2])
            )
            del ttsp_edge_to_sp_tree[e1]
            del ttsp_edge_to_sp_tree[e2]
            ttsp_edge_to_sp_tree[merged] = new_tree
            continue

        series_reduction = find_series_reduction(ttsp)
        if series_reduction:
            e1, e2 = series_reduction.fst, series_reduction.snd
            merged: MultiDiEdge = apply_series_reduction(ttsp, series_reduction)
            new_tree: SerialParallelDecomposition = sp_serial_composition(
                (ttsp_edge_to_sp_tree[e1], ttsp_edge_to_sp_tree[e2])
            )
            del ttsp_edge_to_sp_tree[e1]
            del ttsp_edge_to_sp_tree[e2]
            ttsp_edge_to_sp_tree[merged] = new_tree
            continue

        if ttsp.number_of_nodes() != 2 or ttsp.number_of_edges() != 1:
            return None
        e: MultiDiEdge = get_only(ttsp.edges)
        if e[0] != e[1]:
            return ttsp_edge_to_sp_tree[e]
