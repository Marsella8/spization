from spization.sp_utils.serial_parallel_decomposition import Serial, Parallel
from multimethod import multimethod

@multimethod
def get_nodes(parallel: Parallel) -> set[int]:
    return set().union(*[get_nodes(child) for child in parallel.children])

@multimethod
def get_nodes(serial: Serial) -> set[int]:
    return set().union(*[get_nodes(child) for child in serial.children])

@multimethod
def get_nodes(node: int) -> set[int]:
    return {node}
