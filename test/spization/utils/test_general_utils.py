from spization.utils.general_utils import get_only

def test_get_only():
    input = [1]
    correct = 1
    result = get_only(input)
    assert correct == result
