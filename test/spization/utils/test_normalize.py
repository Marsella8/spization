from spization.objects import (
    Parallel,
    Serial,
)
from spization.utils import normalize


def test_normalize_parallel_basic():
    sp = Parallel((1, 2, 3))
    result = normalize(sp)
    correct = Parallel((1, 2, 3))
    assert result == correct


def test_normalize_parallel_single_node():
    sp = Parallel((1,))
    result = normalize(sp)
    correct = 1
    assert result == correct


def test_normalize_parallel_empty():
    sp = Parallel(())
    result = normalize(sp)
    correct = Parallel(())
    assert result == correct


def test_normalize_parallel_nested():
    sp = Parallel((Serial((1,)), Parallel((2, 3))))
    result = normalize(sp)
    correct = Parallel((1, 2, 3))
    assert result == correct


def test_normalize_serial_basic():
    sp = Serial((1, 2, 3))
    result = normalize(sp)
    correct = Serial((1, 2, 3))
    assert result == correct


def test_normalize_serial_single_node():
    sp = Serial((1,))
    result = normalize(sp)
    correct = 1
    assert result == correct


def test_normalize_serial_empty():
    sp = Serial(())
    result = normalize(sp)
    correct = Serial(())
    assert result == correct


def test_normalize_serial_nested():
    sp = Serial((Parallel((1, 2)), 3))
    result = normalize(sp)
    correct = Serial((Parallel((1, 2)), 3))
    assert result == correct


def test_normalize_int():
    sp = 5
    result = normalize(sp)
    correct = 5
    assert result == correct
