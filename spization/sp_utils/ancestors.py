from .serial_parallel_decomposition import SerialParallelDecomposition, Serial, Parallel
from .nodes import get_nodes
from multimethod import multimethod


@multimethod
def perform_traversal(serial: Serial, starting_node: int, ancestors: set[int]) -> bool:
    for child in serial.children:
        found_starting_node = perform_traversal(child, starting_node, ancestors)
        if found_starting_node:
            return True
    return False


@multimethod
def perform_traversal(
    parallel: Parallel, starting_node: int, ancestors: set[int]
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
def perform_traversal(node: int, starting_node: int, ancestors: set[int]) -> bool:
    if starting_node != node:
        ancestors.add(node)
        return False
    return True


def get_ancestors(sp: SerialParallelDecomposition, starting_node: int) -> set[int]:
    assert starting_node in get_nodes(sp), "Starting node must be in the graph"
    ancestors: set[int] = set()
    perform_traversal(sp, starting_node, ancestors)
    return ancestors
