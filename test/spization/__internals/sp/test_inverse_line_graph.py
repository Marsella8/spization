from typing import Dict

import networkx as nx

from spization.__internals.sp import (
    InverseLineGraphResult,
    inverse_line_graph,
)


def get_edge_counts(g: nx.MultiDiGraph) -> Dict[tuple, int]:
    """Helper function to count edges between pairs of nodes"""
    counts = {}
    for u, v, _ in g.edges:
        edge = (u, v)
        counts[edge] = counts.get(edge, 0) + 1
    return counts


def get_directed_edges_map(result: InverseLineGraphResult) -> Dict[int, tuple]:
    """Convert inverse_edge_to_line_node_map to a map of nodes to edge tuples"""
    return {
        node: (edge[0], edge[1])
        for edge, node in result.inverse_edge_to_line_node_map.items()
    }


def test_diamond_graph():
    r"""Tests that inverse line graph of the diamond graph
        b-d
       /   \
      a     e
       \   /
        c-
    
    is
         2
        / \
     0-1   3-4
        \ /
         -
    """
    g = nx.DiGraph()
    nodes = list(range(5))
    g.add_nodes_from(nodes)

    edges = [(0, 1), (0, 2), (1, 3), (3, 4), (2, 4)]
    g.add_edges_from(edges)

    maybe_result = inverse_line_graph(g)
    assert maybe_result is not None
    result = maybe_result

    assert len(result.graph.nodes()) == 5

    inv = list(nx.topological_sort(result.graph))

    result_edges = get_edge_counts(result.graph)
    correct_edges = {
        (inv[0], inv[1]): 1,
        (inv[1], inv[2]): 1,
        (inv[1], inv[3]): 1,
        (inv[2], inv[3]): 1,
        (inv[3], inv[4]): 1,
    }
    assert result_edges == correct_edges

    result_bidict = get_directed_edges_map(result)
    correct_bidict = {
        nodes[0]: (inv[0], inv[1]),
        nodes[1]: (inv[1], inv[2]),
        nodes[2]: (inv[1], inv[3]),
        nodes[3]: (inv[2], inv[3]),
        nodes[4]: (inv[3], inv[4]),
    }
    assert result_bidict == correct_bidict


def test_duplicate_edges():
    r"""Tests that inverse line graph of the two-node graph
    a b  (no edges)
    
    is
     /\
    0  1
     \/
    """
    g = nx.DiGraph()
    nodes = list(range(2))
    g.add_nodes_from(nodes)

    maybe_result = inverse_line_graph(g)
    assert maybe_result is not None
    result = maybe_result

    assert len(result.graph.nodes()) == 2

    inv = list(nx.topological_sort(result.graph))

    result_edges = get_edge_counts(result.graph)
    correct_edges = {(inv[0], inv[1]): 2}
    assert result_edges == correct_edges

    result_bidict = get_directed_edges_map(result)
    correct_bidict = {nodes[0]: (inv[0], inv[1]), nodes[1]: (inv[0], inv[1])}
    assert result_bidict == correct_bidict


def test_sp_n_graph():
    """Tests that the inverse line graph of the sp n-graph
    a-b
     \
    c-d
    
    does not exist
    """
    g = nx.DiGraph()
    nodes = list(range(4))
    g.add_nodes_from(nodes)

    edges = [(0, 2), (1, 2), (1, 3)]
    g.add_edges_from(edges)

    reduced_g = nx.transitive_reduction(g)

    result = inverse_line_graph(reduced_g)
    assert result is None
