from spization.objects import SerialParallelDecomposition, Serial, Parallel
from spization.utils import replace_node

def test_replace_node_with_itself():
    sp = Serial((1, 2))
    result = replace_node(sp, 1, 1)
    expected = Serial((1, 2))
    assert result == expected

def test_replace_node_with_another_node():
    sp = Parallel((1, 2))
    result = replace_node(sp, 1, 3)
    expected = Parallel((3, 2))
    assert result == expected

def test_replace_node_with_serial():
    sp = 0
    result = replace_node(sp, 0, Serial((1, 2)))
    expected = Serial((1, 2))
    assert result == expected

def test_replace_node_with_parallel():
    sp = 0
    result = replace_node(sp, 0, Parallel((1, 2)))
    expected = Parallel((1, 2))
    assert result == expected

def test_replace_node_complex_case():
    sp = Serial((Parallel((1, 2)), Serial((1, 5))))
    result = replace_node(sp, 1, Parallel((3, 4)))
    expected = Serial((Parallel((Parallel((3, 4)), 2)), Serial((Parallel((3, 4)), 5))))
    assert result == expected

def test_replace_node_with_duplicates():
    sp = Parallel((1, 2, 1))
    result = replace_node(sp, 1, 3)
    expected = Parallel((3, 2, 3))
    assert result == expected
