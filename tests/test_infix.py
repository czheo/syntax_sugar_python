from syntax_sugar import *

def test_int_to_int():
    assert list(1 /to/ 10) == list(range(1, 11))

def test_str_to_str():
    assert str('A' /to/ 'Z') == 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
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
