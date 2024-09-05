from multimethod import multimethod

from spization.objects import (
    Node,
    Parallel,
    Serial,
    SerialParallelDecomposition,
)

from .get_nodes import get_nodes


@multimethod
def perform_traversal(
    serial: Serial, starting_node: Node, ancestors: set[Node]
) -> bool:
    for child in serial.children:
        found_starting_node = perform_traversal(child, starting_node, ancestors)
        if found_starting_node:
            return True
    return False


@multimethod
def perform_traversal(
    parallel: Parallel, starting_node: Node, ancestors: set[Node]
) -> bool:
    if starting_node in get_nodes(parallel):
        branch_with_starting_node = next(
            child for child in parallel.children if starting_node in get_nodes(child)
        )
        perform_traversal(branch_with_starting_node, starting_node, ancestors)
        return True

    for child in parallel.children:
        perform_traversal(child, starting_node, ancestors)
    return False


@multimethod
def perform_traversal(node: Node, starting_node: Node, ancestors: set[Node]) -> bool:
    if starting_node != node:
        ancestors.add(node)
        return False
    return True


def get_ancestors(sp: SerialParallelDecomposition, starting_node: Node) -> set[Node]:
    assert starting_node in get_nodes(sp)
    # TODO: assert has no duplicate nodes
    ancestors: set[Node] = set()
    perform_traversal(sp, starting_node, ancestors)
    return ancestors
