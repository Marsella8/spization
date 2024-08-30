from spization.sp_utils.compositions import serial_composition, parallel_composition
from spization.sp_utils.serial_parallel_decomposition import Parallel, Serial 

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
    result = parallel_composition((Parallel(()), ))
    expected = Parallel(())
    assert result == expected

def test_serial_composition_empty():
    result = serial_composition((Serial(()), ))
    expected = Serial(())
    print(type(result), type(expected), type(result)==type(expected))
    assert result == expected
