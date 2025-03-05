from collections import Counter

from multimethod import multimethod

from spization.objects import Node, Parallel, Serial


@multimethod
def get_node_counter(node: Node) -> Counter[Node]:
    return Counter({node: 1})


@multimethod
def get_node_counter(parallel: Parallel) -> Counter[Node]:
    return sum((get_node_counter(child) for child in parallel), start=Counter())


@multimethod
def get_node_counter(serial: Serial) -> Counter[Node]:
    return sum((get_node_counter(child) for child in serial), start=Counter())
