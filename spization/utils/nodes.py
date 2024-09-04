from multiset import Multiset

from multimethod import multimethod

from spization.objects import Node, Parallel, Serial


@multimethod
def get_nodes(parallel: Parallel) -> set[Node]:
    return set().union(*[get_nodes(child) for child in parallel.children])


@multimethod
def get_nodes(serial: Serial) -> set[Node]:
    return set().union(*[get_nodes(child) for child in serial.children])


@multimethod
def get_nodes(node: Node) -> set[Node]:
    return {node}


@multimethod
def get_node_counter(node: Node):
    return Multiset({node})


@multimethod
def get_node_counter(sp: Serial | Parallel):
    return -1


# TODO return union of counter
