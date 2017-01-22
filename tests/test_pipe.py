from syntax_sugar.pipe import *
from functools import reduce
import os

def test_empty_pipe():
    assert pipe() | 10 | dump() == 10

def test_pipe_with_number():
    assert pipe(10) | dump() == 10

def test_pipe_with_list():
    assert pipe([1,2,3,4]) | dump() == [1,2,3,4]

def test_print():
    assert pipe(10) | print | dump() == None

def test_puts():
    assert pipe(10) | puts | dump() == 10

def test_each():
    assert pipe(range(10)) | each(lambda x: x**2) | dump() \
        == [x**2 for x in range(10)]

def test_where():
    assert pipe(range(10)) | where(lambda x: x<5) | dump() \
        == [0,1,2,3,4]

def test_concat():
    assert pipe() | ["hello", " world!", " Guido"] | concat | dump() \
        == "hello world! Guido"

def test_simple_partial():
    assert (pipe(range(10))
            | (map, lambda x: x ** 2) 
            | (reduce, lambda acc, x: acc + x)
            | dump()) == sum([x ** 2 for x in range(10)])

def test_file_read():
    assert (pipe(__file__) | open | read | dump()) \
        == open(__file__).read()

def test_file_readlines():
    assert (pipe(__file__) | open | readlines | dump()) \
        == open(__file__).readlines()

def test_redirect():
    result = pipe(range(10)) | (map, str) | concat | dump() 
    # test file
    filename = 'testfile.txt'
    (pipe(range(10)) | (map, str) | concat) > filename
    assert open(filename).read() == result
    (pipe(range(10)) | (map, str) | concat) >> filename
    assert open(filename).read() == result * 2
    # clean test file
    os.remove(filename)
