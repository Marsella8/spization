from spization.objects import BinParallel, BinSerial, Parallel, Serial
from spization.utils import bsp_to_sp


def test_bsp_to_sp_single_node():
    input = 1
    result = bsp_to_sp(input)
    correct = 1
    assert result == correct


def test_bsp_to_sp_two_nodes_parallel():
    input = BinParallel(1, 2)
    result = bsp_to_sp(input)
    correct = Parallel((1, 2))
    assert result == correct


def test_bsp_to_sp_two_nodes_serial():
    input = BinSerial(1, 2)
    result = bsp_to_sp(input)
    correct = Serial((1, 2))
    assert result == correct


def test_bsp_to_sp_three_nodes_parallel_multiple_decompositions():
    input1 = BinParallel(1, BinParallel(2, 3))
    input2 = BinParallel(BinParallel(1, 2), 3)

    result1 = bsp_to_sp(input1)
    result2 = bsp_to_sp(input2)
    correct = Parallel((1, 2, 3))

    assert result1 == result2 == correct


def test_bsp_to_sp_three_nodes_serial_multiple_decompositions():
    input1 = BinSerial(1, BinSerial(2, 3))
    input2 = BinSerial(BinSerial(1, 2), 3)

    result1 = bsp_to_sp(input1)
    result2 = bsp_to_sp(input2)
    correct = Serial((1, 2, 3))

    assert result1 == result2 == correct


def test_bsp_to_sp_nested_parallel_in_serial():
    input = BinSerial(1, BinParallel(2, 3))
    result = bsp_to_sp(input)
    correct = Serial((1, Parallel((2, 3))))
    assert result == correct


def test_bsp_to_sp_nested_serial_in_parallel():
    input = BinParallel(1, BinSerial(2, 3))
    result = bsp_to_sp(input)
    correct = Parallel((1, Serial((2, 3))))
    assert result == correct


def test_bsp_to_sp_deep_nesting_multiple_decompositions():
    input1 = BinSerial(1, BinSerial(2, BinParallel(3, BinParallel(4, 5))))
    input2 = BinSerial(BinSerial(1, 2), BinParallel(3, BinParallel(4, 5)))
    input3 = BinSerial(1, BinSerial(2, BinParallel(BinParallel(3, 4), 5)))

    result1 = bsp_to_sp(input1)
    result2 = bsp_to_sp(input2)
    result3 = bsp_to_sp(input3)
    correct = Serial((1, 2, Parallel((3, 4, 5))))

    assert result1 == result2 == result3 == correct


def test_bsp_to_sp_parallel_with_duplicate_nodes():
    input1 = BinParallel(1, BinParallel(1, 2))
    input2 = BinParallel(BinParallel(1, 1), 2)

    result1 = bsp_to_sp(input1)
    result2 = bsp_to_sp(input2)
    correct = Parallel((1, 1, 2))

    assert result1 == result2 == correct


def test_bsp_to_sp_mixed_composition():
    input1 = BinSerial(
        BinParallel(1, BinParallel(2, 3)), BinParallel(4, BinParallel(5, 6))
    )
    input2 = BinSerial(
        BinParallel(BinParallel(1, 2), 3), BinParallel(BinParallel(4, 5), 6)
    )

    result1 = bsp_to_sp(input1)
    result2 = bsp_to_sp(input2)
    correct = Serial((Parallel((1, 2, 3)), Parallel((4, 5, 6))))

    assert result1 == result2 == correct


def test_bsp_to_sp_symmetric_structure():
    input1 = BinParallel(BinSerial(1, 2), BinSerial(3, 4))
    input2 = BinParallel(BinSerial(3, 4), BinSerial(1, 2))

    result1 = bsp_to_sp(input1)
    result2 = bsp_to_sp(input2)
    correct = Parallel((Serial((1, 2)), Serial((3, 4))))

    assert result1 == result2 == correct


def test_bsp_to_sp_four_valid_decompositions():
    # Serial(Parallel(1,2,3), Parallel(4,5,6)) has 4 possible decompositions
    # 2 ways to decompose each parallel of 3 elements: (a,(b,c)) or ((a,b),c)
    # So 2x2 = 4 total possible decompositions

    input1 = BinSerial(
        BinParallel(1, BinParallel(2, 3)), BinParallel(4, BinParallel(5, 6))
    )

    input2 = BinSerial(
        BinParallel(BinParallel(1, 2), 3), BinParallel(4, BinParallel(5, 6))
    )

    input3 = BinSerial(
        BinParallel(1, BinParallel(2, 3)), BinParallel(BinParallel(4, 5), 6)
    )

    input4 = BinSerial(
        BinParallel(BinParallel(1, 2), 3), BinParallel(BinParallel(4, 5), 6)
    )

    result1 = bsp_to_sp(input1)
    result2 = bsp_to_sp(input2)
    result3 = bsp_to_sp(input3)
    result4 = bsp_to_sp(input4)
    correct = Serial((Parallel((1, 2, 3)), Parallel((4, 5, 6))))

    assert result1 == result2 == result3 == result4 == correct
