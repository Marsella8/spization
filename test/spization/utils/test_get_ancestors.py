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


def test_ancestors_nested():
    input = Serial((0, Parallel((Serial((1, 2)), Serial((3, 4)))), 5))
    correct0 = set()
    result0 = get_ancestors(input, 0)
    assert correct0 == result0
    correct4 = {0, 3}
    result4 = get_ancestors(input, 4)
    assert correct4 == result4
    correct5 = {0, 1, 2, 3, 4}
    result5 = get_ancestors(input, 5)
    assert correct5 == result5
