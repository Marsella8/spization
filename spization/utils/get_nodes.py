from multimethod import multimethod
from multiset import Multiset

from spization.objects import Node, Parallel, Serial


@multimethod
def get_nodes(parallel: Parallel) -> Multiset[Node]:
    return Multiset().combine(*[get_nodes(child) for child in parallel.children])


@multimethod
def get_nodes(serial: Serial) -> Multiset[Node]:
    return Multiset().combine(*[get_nodes(child) for child in serial.children])


@multimethod
def get_nodes(node: Node) -> Multiset[Node]:
    return Multiset({node})
