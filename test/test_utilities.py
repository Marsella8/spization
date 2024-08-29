import pytest
from serial_parallel_decomposition import Serial, Parallel, SerialParallelDecomposition
from utilities import parallel_composition, serial_composition

def test_parallel_composition_basic():
    result = parallel_composition((1, 2, 3))
    expected = Parallel((1, 2, 3))
    assert result == expected

def test_parallel_composition_nested():
    result = parallel_composition((
        Parallel((1, 2)),
        Serial((3 ,4)),
        5
    ))
    expected = Parallel((1, 2, 5, Serial((3, 4))))
    assert result == expected

def test_serial_composition_basic():
    result = serial_composition((1, 2, 3))
    expected = Serial((1, 2, 3))
    assert result == expected

def test_serial_composition_nested():
    result = serial_composition((
        Serial((1, 2)),
        Parallel((3, 4)),
        5
    ))
    expected = Serial((1, 2, Parallel((3, 4)), 5))
    assert result == expected

def test_parallel_composition_empty():
    result = parallel_composition(())
    expected = Parallel(())
    assert result == expected

def test_serial_composition_empty():
    result = serial_composition(())
    expected = Serial(())
    print(type(result), type(expected), type(result)==type(expected))
    assert result == expected
