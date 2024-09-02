from networkx import DiGraph
from .longest_path_lengths_from_source import longest_path_lengths_from_source
from spization.utils.sp.serial_parallel_decomposition import Node


def strata_sort(g: DiGraph) -> list[Node]:
    depth_map: dict[Node, int] = longest_path_lengths_from_source(g)
    return sorted(depth_map.keys(), key=lambda node: depth_map[node])
