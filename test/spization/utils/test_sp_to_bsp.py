import pytest

from spization.objects import BinParallel, BinSerial, Parallel, Serial
from spization.utils import sp_to_bsp


def test_sp_to_bsp_single_node():
    input = 1
    result = sp_to_bsp(input)
    correct = 1
    assert result == correct


def test_sp_to_bsp_empty_parallel():
    input = Parallel()
    with pytest.raises(ValueError):
        sp_to_bsp(input)


def test_sp_to_bsp_empty_serial():
    input = Serial()
    with pytest.raises(ValueError):
        sp_to_bsp(input)


def test_sp_to_bsp_single_node_parallel():
    input = Parallel((1,))
    result = sp_to_bsp(input)
    correct = 1
    assert result == correct


def test_sp_to_bsp_three_nodes_parallel():
    input = Parallel((1, 2, 3))
    result = sp_to_bsp(input)
    correct = BinParallel(1, BinParallel(2, 3))
    assert result == correct


def test_sp_to_bsp_single_node_serial():
    input = Serial((1,))
    result = sp_to_bsp(input)
    correct = 1
    assert result == correct


def test_sp_to_bsp_three_nodes_serial():
    input = Serial((1, 2, 3))
    result = sp_to_bsp(input)
    correct = BinSerial(1, BinSerial(2, 3))
    assert result == correct


def test_sp_to_bsp_nested_parallel_in_serial():
    input = Serial((1, Parallel((2, 3))))
    result = sp_to_bsp(input)
    correct = BinSerial(1, BinParallel(2, 3))
    assert result == correct


def test_sp_to_bsp_nested_serial_in_parallel():
    input = Parallel((1, Serial((2, 3))))
    result = sp_to_bsp(input)
    correct = BinParallel(1, BinSerial(2, 3))
    assert result == correct


def test_sp_to_bsp_duplicate_nodes_parallel():
    input = Parallel((1, 1, 2))
    result = sp_to_bsp(input)
    correct = BinParallel(1, BinParallel(1, 2))
    assert result == correct


def test_sp_to_bsp_empty_parallel_in_serial():
    input = Serial((1, Parallel(())))
    result = sp_to_bsp(input)
    correct = 1
    assert result == correct


def test_sp_to_bsp_empty_serial_in_parallel():
    input = Parallel((1, Serial(())))
    result = sp_to_bsp(input)
    correct = 1
    assert result == correct


def test_sp_to_bsp_deep_nesting():
    input = Serial((1, 2, Parallel((3, 4, Serial((5,))))))
    result = sp_to_bsp(input)
    correct = BinSerial(1, BinSerial(2, BinParallel(3, BinParallel(4, 5))))
    assert result == correct


def test_sp_to_bsp_serial_with_2_parallel():
    input = Serial((Parallel((1, 2, 3)), Parallel((4, 5, 6))))
    result = sp_to_bsp(input)
    correct = BinSerial(
        BinParallel(1, BinParallel(2, 3)), BinParallel(4, BinParallel(5, 6))
    )
    assert result == correct
