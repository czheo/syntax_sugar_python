from pytest import raises
import random
from syntax_sugar import *
from syntax_sugar.infix import To

def test_int_to_int():
    assert list(1 /to/ 1) == [1]
    assert list(2 /to/ 1) == [2, 1]
    for i in range(100):
        start, end = random.randint(1, 1e3), random.randint(1, 1e3)
        end += start
        assert list(start /to/ end) == list(range(start, end + 1))

        start, end = end, start
        assert list(start /to/ end) == list(range(start, end - 1, -1))

def test_int_to_int_with_step():
    assert list(1 /to/ 1 /by/ 2) == [1]
    assert list(2 /to/ 1 /by/ 2) == [2]
    for i in range(100):
        start, end = random.randint(1, 1e3), random.randint(1, 1e3)
        step = random.randint(1, 10)
        end += start
        assert list(start /to/ end /by/ step) == list(range(start, end + 1, step))
        assert list(start /to/ end /by/ -step) == list(range(start, end + 1, step))

        start, end = end, start
        assert list(start /to/ end /by/ -step) == list(range(start, end - 1, -step))
        assert list(start /to/ end /by/ step) == list(range(start, end - 1, -step))

def test_str_to_str():
    assert str('A' /to/ 'Z') == 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
    assert str('Z' /to/ 'A') == 'ZYXWVUTSRQPONMLKJIHGFEDCBA'
    assert str('a' /to/ 'z') == 'abcdefghijklmnopqrstuvwxyz'
    assert str('z' /to/ 'a') == 'zyxwvutsrqponmlkjihgfedcba'
    assert str('D' /to/ 'V') == 'DEFGHIJKLMNOPQRSTUV'
    assert str('V' /to/ 'D') == 'VUTSRQPONMLKJIHGFED'
    assert str('v' /to/ 'd') == 'vutsrqponmlkjihgfed'

def test_str_to_str_with_step():
    assert str('A' /to/ 'Z' /by/ 3) == 'ADGJMPSVY'
    assert str('A' /to/ 'Z' /by/ -3) == 'ADGJMPSVY'
    assert str('Z' /to/ 'A' /by/ -3) == 'ZWTQNKHEB'
    assert str('Z' /to/ 'A' /by/ 3) == 'ZWTQNKHEB'
    assert str('a' /to/ 'z' /by/ 4) == 'aeimquy'
    assert str('a' /to/ 'z' /by/ -4) == 'aeimquy'
    assert str('z' /to/ 'a' /by/ -4) == 'zvrnjfb'
    assert str('z' /to/ 'a' /by/ 4) == 'zvrnjfb'
    assert str('D' /to/ 'V' /by/ 5) == 'DINS'
    assert str('D' /to/ 'V' /by/ -5) == 'DINS'
    assert str('V' /to/ 'D' /by/ -5) == 'VQLG'
    assert str('V' /to/ 'D' /by/ 5) == 'VQLG'
    assert str('v' /to/ 'd' /by/ -3) == 'vspmjgd'
    assert str('v' /to/ 'd' /by/ 3) == 'vspmjgd'

def test_bad_step():
    to_obj = To(1, 2)
    for bad_step in ["x", [], 1.5]:
        with raises(TypeError):
            to_obj.step = bad_step

    with raises(ValueError):
        to_obj.step = 0

    with raises(ValueError):
        to_obj.step = -1

    to_obj = To(2, 1)
    with raises(ValueError):
        to_obj.step = 1

def test_infinity():
    with raises(ValueError):
        INF /to/ 100

    with raises(ValueError):
        NEGINF /to/ 1

    assert 1 /to/ INF /take/ 10 == list(range(1, 11))
    assert 1 /to/ NEGINF /take/ 10 == list(range(1, -9, -1))

    assert 1 /to/ INF /by/ 2 /take/ 10 == list(range(1, 100, 2))[:10]
    assert 1 /to/ NEGINF /by/ 2 /take/ 10 == list(range(1, -100, -2))[:10]

def test_take():
    assert 1 /to/ INF /take/ 5 == [1,2,3,4,5]

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
