from pytest import raises
from syntax_sugar._iter import Range, Iterator, INF
from syntax_sugar._util import take, to
from itertools import product


def test_range_bad_step():
    range_obj = Range(1, 2)
    for bad_step in ["x", [], 1.5]:
        with raises(TypeError):
            range_obj.step = bad_step

    with raises(ValueError):
        range_obj.step = 0

    with raises(ValueError):
        range_obj.step = -1

    range_obj = Range(2, 1)
    with raises(ValueError):
        range_obj.step = 1

def test_iterator():
    assert list(Iterator(Range(1, 10))) == list(range(1, 11))
    assert list(Iterator(range(1, 10))) == list(range(1, 10))
    assert list(Iterator([1,2,3,4])) == [1,2,3,4]
    assert list((1 /to/ INF) * (2 /to/ 4) /take/ 5) == list(product([1,2,3], [2,3,4]))[:5]
