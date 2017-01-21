from syntax_sugar import *

def test_int_to_int():
    assert 1 /to/ 10 == range(1, 11)

def test_str_to_str():
    assert 'A' /to/ 'Z' == 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
