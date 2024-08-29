from serial_parallel_decomposition import SerialParallelDecomposition, Serial, Parallel
from collections import Counter
from multipledispatch import dispatch as overload
from typing import Iterable, Union

@overload(Parallel)
def get_nodes(parallel : Parallel) -> set[int]:
    return set().union(*[get_nodes(child) for child in parallel.children])

@overload(Serial)
def get_nodes(serial : Serial) -> set[int]:
    return set().union(*[get_nodes(child) for child in serial.children])

@overload(int)
def get_nodes(node : int) -> set[int]:
    return {node}

def is_empty(sp : SerialParallelDecomposition) -> bool:
    return len(get_nodes(sp)) == 0

def parallel_composition(elements : Iterable[SerialParallelDecomposition]) -> Parallel:
    children : Counter[Union[Parallel, int]] = Counter()
    for element in elements:
        if isinstance(element, Parallel):
            print(type(element.children))
            children += element.children
        else:
            children[element] += 1
    return Parallel(children)

def serial_composition(elements : Iterable[SerialParallelDecomposition]) -> Serial:
    children : list[Union[Serial, int]] = []
    for element in elements:
        if isinstance(element, Serial):
            print(type(element.children))
            children.extend(element)
        else:
            children.append(element)
    return Serial(children)

