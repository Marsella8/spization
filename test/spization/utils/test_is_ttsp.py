from networkx import DiGraph

from spization.utils import is_ttsp


def test_is_ttsp_base_case():
    g = DiGraph(((0, 1),))
    result = is_ttsp(g)
    correct = True
    assert result == correct


def test_is_ttsp_serial_composition():
    g = DiGraph(((0, 1), (1, 2)))
    result = is_ttsp(g)
    correct = True
    assert result == correct


def test_is_ttsp_parallel_composition():
    g = DiGraph(((0, 1), (0, 1)))
    result = is_ttsp(g)
    correct = True
    assert result == correct


def test_is_ttsp_multiple_serial_compositions():
    g = DiGraph(((0, 1), (0, 2), (1, 2)))
    result = is_ttsp(g)
    correct = True
    assert result == correct


def test_is_ttsp_multiple_serial_compositions():
    g = DiGraph(((0, 1), (0, 2), (1, 3), (2, 3)))
    result = is_ttsp(g)
    correct = True
    assert result == correct


def test_is_ttsp_diamond():
    g = DiGraph(((0, 1), (0, 2), (1, 3), (2, 3), (2, 4), (3, 5), (4, 5)))
    result = is_ttsp(g)
    correct = False
    assert result == correct


def test_is_ttsp_extended_rhombus():
    g = DiGraph(((0, 1), (1, 2), (1, 3), (2, 4), (3, 4), (4, 5)))
    result = is_ttsp(g)
    correct = True
    assert result == correct


# TODO add a check to make sure that IS_TTSP <=> get_series_parallel_decomposition is not None
