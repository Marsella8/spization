from spization.objects import Parallel, PureNode, Serial
from spization.utils import get_ancestors


def test_ancestors_single_node():
    input = PureNode(0)
    correct = set()
    result = get_ancestors(input, 0)
    assert correct == result


def test_ancestors():
    input = Serial((1, Parallel((2, 3)), 4))
    correct = {1, 2, 3}
    result = get_ancestors(input, 4)
    assert correct == result


def test_ancestors_serial():
    input = Serial((1, 2, 3))
    correct = {1, 2}
    result = get_ancestors(input, 3)
    assert correct == result


def test_ancestors_parallel():
    input = Parallel((1, 2, 3))
    correct = set()
    result = get_ancestors(input, 3)
    assert correct == result
