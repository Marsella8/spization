from multiset import Multiset

from spization.objects import Parallel, Serial
from spization.utils import get_nodes


def test_get_nodes_single_node():
    result = get_nodes(0)
    expected = Multiset({0})
    assert result == expected


def test_get_nodes_parallel_unique():
    parallel = Parallel([0, 1, 2])
    result = get_nodes(parallel)
    expected = Multiset([0, 1, 2])
    assert result == expected


def test_get_nodes_serial_unique():
    serial = Serial([0, 1, 2])
    result = get_nodes(serial)
    expected = Multiset([0, 1, 2])
    assert result == expected


def test_get_nodes_complex():
    complex_structure = Serial([0, Parallel([1, 2]), 3])
    result = get_nodes(complex_structure)
    expected = Multiset([0, 1, 2, 3])
    assert result == expected


def test_get_nodes_parallel_duplicates():
    parallel = Parallel([0, 0, 1, 1])
    result = get_nodes(parallel)
    expected = Multiset([0, 0, 1, 1])
    assert result == expected


def test_get_nodes_serial_duplicates():
    serial = Serial([0, 0, 1, 1])
    result = get_nodes(serial)
    expected = Multiset([0, 0, 1, 1])
    assert result == expected
