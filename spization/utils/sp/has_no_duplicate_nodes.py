from serial_parallel_decomposition import SerialParallelDecomposition
from nodes import get_node_counter


def has_no_duplicate_nodes(sp: SerialParallelDecomposition) -> bool:
    return all(c == 1 for _, c in get_node_counter(sp))
