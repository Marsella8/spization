from multimethod import multimethod
from multiset import FrozenMultiset

from spization.objects import Node, Parallel, Serial


@multimethod
def get_nodes(parallel: Parallel) -> FrozenMultiset[Node]:
    return FrozenMultiset().combine(*[get_nodes(child) for child in parallel.children])


@multimethod
def get_nodes(serial: Serial) -> FrozenMultiset[Node]:
    return FrozenMultiset().combine(*[get_nodes(child) for child in serial.children])


@multimethod
def get_nodes(node: Node) -> FrozenMultiset[Node]:
    return FrozenMultiset({node})
