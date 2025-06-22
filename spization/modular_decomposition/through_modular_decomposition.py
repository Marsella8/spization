from typing import Callable

from multimethod import multimethod

from spization.modular_decomposition.directed.objects import (
    MDParallel,
    MDPrime,
    MDSeries,
)
from spization.modular_decomposition.undirected.objects import (
    Node,
)
from spization.objects import Parallel, Serial, SeriesParallelDecomposition
from spization.utils.compositions import sp_parallel_composition, sp_serial_composition


@multimethod
def md_to_spd(
    md: Node, func_for_prime_module: Callable[[MDPrime], SeriesParallelDecomposition]
) -> Node:
    return md


@multimethod
def md_to_spd(
    md: MDParallel,
    func_for_prime_module: Callable[[MDPrime], SeriesParallelDecomposition],
) -> Parallel:
    converted_children = [
        md_to_spd(child, func_for_prime_module) for child in md.children
    ]
    return sp_parallel_composition(converted_children)


@multimethod
def md_to_spd(
    md: MDSeries,
    func_for_prime_module: Callable[[MDPrime], SeriesParallelDecomposition],
) -> Serial:
    converted_children = [
        md_to_spd(child, func_for_prime_module) for child in md.children
    ]
    return sp_serial_composition(converted_children)


@multimethod
def md_to_spd(
    md: MDPrime,
    func_for_prime_module: Callable[
        [MDPrime], SeriesParallelDecomposition
    ],
) -> SeriesParallelDecomposition:
    return func_for_prime_module(md)
