from spization.objects import Parallel, PureNode, Serial
from spization.utils import get_nodes, random_sp


def test_random_sp_single_node():
    sp = random_sp(1)
    expected = PureNode(0)
    assert sp == expected


def test_random_sp_parallel():
    sp = random_sp(5, prob_serial=0)
    expected = Parallel((0, 1, 2, 3, 4))
    assert sp == expected


def test_random_sp_serial():
    sp = random_sp(5, prob_serial=1)
    assert isinstance(sp, Serial)
    result_nodes = get_nodes(sp)
    correct_nodes = {0, 1, 2, 3, 4}
    assert result_nodes == correct_nodes


def test_random_sp_correct_num_nodes():
    sp = random_sp(5, prob_serial=0.5)
    result_nodes = get_nodes(sp)
    correct_nodes = {0, 1, 2, 3, 4}
    assert result_nodes == correct_nodes
