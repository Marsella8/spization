from spization.sp_utils.serial_parallel_decomposition import Serial, Parallel
from spization.sp_utils.ancestors import get_ancestors


def test_ancestors():
    input = Serial((1, Parallel((2, 3)), 4))
    correct = {1, 2, 3}
    result = get_ancestors(input, 4)
    assert correct == result
