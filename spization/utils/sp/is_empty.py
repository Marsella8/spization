from .nodes import get_nodes
from .serial_parallel_decomposition import SerialParallelDecomposition


def is_empty(sp: SerialParallelDecomposition) -> bool:
    return len(get_nodes(sp)) == 0
