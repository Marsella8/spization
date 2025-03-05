from random import choice, random

from spization.objects import (
    Parallel,
    PureNode,
    Serial,
    SerialParallelDecomposition,
)
from spization.utils.get_nodes import get_nodes
from spization.utils.normalize import normalize
from spization.utils.replace_node import replace_node


def get_random_node(sp: SerialParallelDecomposition) -> PureNode:
    return choice(list(get_nodes(sp)))


def random_sp(num_nodes: int, prob_serial: float = 0.5) -> SerialParallelDecomposition:
    assert 0 <= prob_serial <= 1 and num_nodes > 0
    sp: SerialParallelDecomposition = PureNode(0)
    for node in range(1, num_nodes):
        node_to_sub = get_random_node(sp)
        if random() < prob_serial:
            sp = replace_node(sp, node_to_sub, Serial((node_to_sub, node)))
        else:
            sp = replace_node(sp, node_to_sub, Parallel((node_to_sub, node)))
    return normalize(sp)
