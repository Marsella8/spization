from spization.objects import Parallel, Serial
from spization.utils import get_ancestors


def test_ancestors():
    input = Serial((1, Parallel((2, 3)), 4))
    correct = {1, 2, 3}
    result = get_ancestors(input, 4)
    assert correct == result
