from .serial_parallel_decomposition import (
    SerialParallelDecomposition,
    Serial,
    Parallel,
    Node,
)
from collections import Counter
from typing import Iterable, Union
from networkx import DiGraph
import networkx as nx
from functools import reduce
from spization.utils.graph import sources, sinks


def sp_parallel_composition(
    elements: Iterable[SerialParallelDecomposition],
) -> Parallel:
    children: Counter[Union[Serial, Node]] = Counter()
    for element in elements:
        if isinstance(element, Parallel):
            children += element.children
        else:
            children[element] += 1
    return Parallel(children)


def sp_serial_composition(elements: Iterable[SerialParallelDecomposition]) -> Serial:
    children: list[Union[Parallel, Node]] = []
    for element in elements:
        if isinstance(element, Serial):
            children.extend(element)
        else:
            children.append(element)
    return Serial(children)


def graph_parallel_composition(elements: Iterable[DiGraph]) -> DiGraph:
    return reduce(nx.union, elements)


def graph_serial_composition(elements: Iterable[DiGraph]) -> DiGraph:
    def binary_spg_serial_composition(g1: DiGraph, g2: DiGraph) -> DiGraph:
        g = nx.union(g1, g2)
        for n1 in sinks(g1):
            for n2 in sources(g2):
                g.add_edge([n1, n2])

    return reduce(binary_spg_serial_composition, elements)