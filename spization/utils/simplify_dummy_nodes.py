# If a sync node has 1 either in or out you can simplify
from spization.objects import DummyNode, SerialParallelDecomposition

from .get_nodes import get_nodes


def simplify_dummy_nodes(g: SerialParallelDecomposition):
    for node in [n for n in get_nodes(g) if isinstance(g, DummyNode)]:
        ...
