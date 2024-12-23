from multimethod import multimethod

from spization.objects import Node, Parallel, Serial, SerialParallelDecomposition


@multimethod
def replace_node(
    sp: Node, node: Node, replacer: SerialParallelDecomposition
) -> SerialParallelDecomposition:
    if sp == node:
        return replacer
    return sp


@multimethod
def replace_node(
    sp: Serial, node: Node, replacer: SerialParallelDecomposition
) -> SerialParallelDecomposition:
    return Serial((replace_node(child, node, replacer) for child in sp))


@multimethod
def replace_node(
    sp: Parallel, node: Node, replacer: SerialParallelDecomposition
) -> SerialParallelDecomposition:
    return Parallel((replace_node(child, node, replacer) for child in sp))
