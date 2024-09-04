from spization.__internals.general import get_any, get_only


def test_get_only():
    input = [1]
    correct = 1
    result = get_only(input)
    assert correct == result


def test_get_any():
    input = {1, 2, 3}
    result = get_any(input)
    assert result in input
