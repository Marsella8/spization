from spization.objects import SerialParallelDecomposition

from .nodes import get_nodes


def is_empty(sp: SerialParallelDecomposition) -> bool:
    return len(get_nodes(sp)) == 0