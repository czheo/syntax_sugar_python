from syntax_sugar import *

def test_int_to_int():
    assert list(1 /to/ 10) == list(range(1, 11))

def test_str_to_str():
    assert str('A' /to/ 'Z') == 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
def test_take():
    assert 1 /to/ INF /take/ 5 == [1,2,3,4,5]
