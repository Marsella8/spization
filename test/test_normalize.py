import pytest
from serial_parallel_decomposition import Serial, Parallel, SerialParallelDecomposition
from utilities import is_empty, get_nodes, parallel_composition, serial_composition
from normalize import normalize

def test_normalize_parallel_basic():
    sp = Parallel((1, 2, 3))
    result = normalize(sp)
    expected = Parallel((1, 2, 3))
    assert result == expected

def test_normalize_parallel_single_node():
    sp = Parallel((1,))
    result = normalize(sp)
    expected = 1
    assert result == expected

def test_normalize_parallel_empty():
    sp = Parallel(())
    result = normalize(sp)
    expected = Parallel(())
    assert result == expected

def test_normalize_parallel_nested():
    sp = Parallel((Serial((1,)), Parallel((2, 3))))
    result = normalize(sp)
    expected = Parallel((1,2,3))
    assert result == expected

def test_normalize_serial_basic():
    sp = Serial((1, 2, 3))
    result = normalize(sp)
    expected = Serial((1, 2, 3))
    assert result == expected

def test_normalize_serial_single_node():
    sp = Serial((1,))
    result = normalize(sp)
    expected = 1
    assert result == expected

def test_normalize_serial_empty():
    sp = Serial(())
    result = normalize(sp)
    expected = Serial(())
    assert result == expected

def test_normalize_serial_nested():
    sp = Serial((Parallel((1, 2)), 3))
    result = normalize(sp)
    expected = Serial((Parallel((1, 2)), 3))
    assert result == expected

def test_normalize_int():
    sp = 5
    result = normalize(sp)
    expected = 5
    assert result == expected
