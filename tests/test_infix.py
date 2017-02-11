from pytest import raises
import random
from syntax_sugar import *
from syntax_sugar.iter import Iterator

def _assert_iter(expr, expected):
    assert expr /is_a/ Iterator == True
    assert list(expr) == list(expected)

def test_int_to_int():
    _assert_iter(1 /to/ 1, [1])
    _assert_iter(2 /to/ 1, [2, 1])
    for i in range(100):
        start, end = random.randint(1, 1e3), random.randint(1, 1e3)
        end += start
        _assert_iter(start /to/ end, range(start, end + 1))

        start, end = end, start
        _assert_iter(start /to/ end, range(start, end - 1, -1))

def test_int_to_int_with_step():
    _assert_iter(1 /to/ 1 /step/ 2, [1])
    _assert_iter(2 /to/ 1 /step/ 2, [2])
    for i in range(100):
        start, end = random.randint(1, 1e3), random.randint(1, 1e3)
        s = random.randint(1, 10)
        end += start
        _assert_iter(start /to/ end /step/ s, range(start, end + 1, s))
        _assert_iter(start /to/ end /step/ -s, range(start, end + 1, s))

        start, end = end, start
        _assert_iter(start /to/ end /step/ -s, range(start, end - 1, -s))
        _assert_iter(start /to/ end /step/ s, range(start, end - 1, -s))

def test_str_to_str():
    _assert_iter('A' /to/ 'Z', 'ABCDEFGHIJKLMNOPQRSTUVWXYZ')
    _assert_iter('Z' /to/ 'A', 'ZYXWVUTSRQPONMLKJIHGFEDCBA')
    _assert_iter('a' /to/ 'z', 'abcdefghijklmnopqrstuvwxyz')
    _assert_iter('z' /to/ 'a', 'zyxwvutsrqponmlkjihgfedcba')
    _assert_iter('D' /to/ 'V', 'DEFGHIJKLMNOPQRSTUV')
    _assert_iter('V' /to/ 'D', 'VUTSRQPONMLKJIHGFED')
    _assert_iter('v' /to/ 'd', 'vutsrqponmlkjihgfed')

def test_str_to_str_with_step():
    _assert_iter('A' /to/ 'Z' /step/ 3, 'ADGJMPSVY')
    _assert_iter('A' /to/ 'Z' /step/ -3, 'ADGJMPSVY')
    _assert_iter('Z' /to/ 'A' /step/ -3, 'ZWTQNKHEB')
    _assert_iter('Z' /to/ 'A' /step/ 3, 'ZWTQNKHEB')
    _assert_iter('a' /to/ 'z' /step/ 4, 'aeimquy')
    _assert_iter('a' /to/ 'z' /step/ -4, 'aeimquy')
    _assert_iter('z' /to/ 'a' /step/ -4, 'zvrnjfb')
    _assert_iter('z' /to/ 'a' /step/ 4, 'zvrnjfb')
    _assert_iter('D' /to/ 'V' /step/ 5, 'DINS')
    _assert_iter('D' /to/ 'V' /step/ -5, 'DINS')
    _assert_iter('V' /to/ 'D' /step/ -5, 'VQLG')
    _assert_iter('V' /to/ 'D' /step/ 5, 'VQLG')
    _assert_iter('v' /to/ 'd' /step/ -3, 'vspmjgd')
    _assert_iter('v' /to/ 'd' /step/ 3, 'vspmjgd')

def test_infinity():
    with raises(ValueError):
        INF /to/ 100

    with raises(ValueError):
        NEGINF /to/ 1

    _assert_iter(1 /to/ INF /take/ 10, range(1, 11))
    _assert_iter(1 /to/ NEGINF /take/ 10, range(1, -9, -1))

    _assert_iter(1 /to/ INF /step/ 2 /take/ 10, list(range(1, 100, 2))[:10])
    _assert_iter(1 /to/ NEGINF /step/ 2 /take/ 10, list(range(1, -100, -2))[:10])

    _assert_iter(1 /to/ NEGINF /step/ 2 /take/ 10 /drop/ 2, list(range(1, -100, -2))[2:10])
    _assert_iter(1 /to/ NEGINF /step/ 2 /drop/ 5 /take/ 3, [-9, -11, -13])


def test_take():
    _assert_iter(1 /to/ INF /take/ 5, [1,2,3,4,5])
    _assert_iter(range(10) /take/ 5, [0,1,2,3,4])
    _assert_iter([1,2,3,4,5,6,7] /take/ 5, [1,2,3,4,5])

def test_drop():
    _assert_iter(1 /to/ 10 /drop/ 2 /take/ 3, [3, 4, 5])
    _assert_iter(1 /to/ INF /drop/ 2 /take/ 3, [3, 4, 5])
    _assert_iter(10 /to/ 1 /drop/ 3 /take/ 2, [7, 6])

def test_iter_pipe():
    assert 0 /to/ 9 | each(lambda x: x**2) | list | END == [x**2 for x in range(10)]
    assert 0 /to/ 9 /take/ 2 | each(lambda x: x**2) | list | END == [x**2 for x in range(10)][:2]
    assert 0 /to/ 9 /drop/ 2 | each(lambda x: x**2) | list| END == [x**2 for x in range(10)][2:]

def test_is_a():
    values_types_right = [
        (2, int),
        ('strings', str),
        ({}, dict),
        ([], list),
        ((), tuple)
    ]

    values_types_wrong = [
        (2, [str, dict, list, tuple]),
        ('strings', [int, dict, list, tuple]),
        ({}, [int, str, list, tuple]),
        ([], [int, str, dict, tuple]),
        ((), [int, str, dict, list])
    ]

    for value, type in values_types_right:
        assert value /is_a/ type
            
    for value, types in values_types_wrong:
        for type in types:
            assert not value /is_a/ type
