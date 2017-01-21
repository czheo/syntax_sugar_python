from syntax_sugar.pipe import *
from functools import reduce
import os

def test_empty_pipe():
    assert pipe() | 10 | ret == 10

def test_pipe_with_number():
    assert pipe(10) | ret == 10

def test_pipe_with_list():
    assert pipe([1,2,3,4]) | ret == [1,2,3,4]

def test_print():
    assert pipe(10) | print | ret == None

def test_puts():
    assert pipe(10) | puts | ret == 10

def test_each():
    assert pipe(range(10)) | each(lambda x: x**2) | ret \
        == [x**2 for x in range(10)]

def test_where():
    assert pipe(range(10)) | where(lambda x: x<5) | ret \
        == [0,1,2,3,4]

def test_concat():
    assert pipe() | ["hello", " world!", " Guido"] | concat | ret \
        == "hello world! Guido"

def test_symple_partial():
    assert (pipe(range(10))
            | (map, lambda x: x ** 2) 
            | (reduce, lambda acc, x: acc + x)
            | ret ) == sum([x ** 2 for x in range(10)])

def test_file_read():
    assert (pipe(__file__) | open | read | ret) \
        == open(__file__).read()

def test_file_readlines():
    assert (pipe(__file__) | open | readlines | ret) \
        == open(__file__).readlines()

def test_redirect():
    result = pipe(range(10)) | (map, str) | concat | ret
    # test file
    filename = 'testfile.txt'
    (pipe(range(10)) | (map, str) | concat) > filename
    assert open(filename).read() == result
    (pipe(range(10)) | (map, str) | concat) >> filename
    assert open(filename).read() == result * 2
    # clean test file
    os.remove(filename)
