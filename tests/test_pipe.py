from syntax_sugar.pipe import *
from functools import partial, reduce
import os

def test_pipe_with_number():
    assert pipe(10) | END == 10

def test_pipe_with_list():
    assert pipe([1,2,3,4]) | END == [1,2,3,4]

def test_each():
    assert pipe(range(10)) | each(lambda x: x**2) | list | END \
        == [x**2 for x in range(10)]

def test_puts():
    assert pipe(10) | range | puts | END == range(10)

def test_short_partial():
    assert pipe(range(10)) | (map, lambda x: x**2) | list | END \
        == [x**2 for x in range(10)]

def test_pipe_connect():
    p1 = pipe(10) | range | each(lambda x: x**2)
    p2 = pipe() | partial(reduce, lambda acc, x: acc + x)
    assert p1 | p2 | END == reduce(lambda acc,x : acc + x, map(lambda x: x**2, range(10)))

    p3 = pipe() | range | sum
    assert p1 | p2 | p3 | END == sum(range(reduce(lambda acc,x : acc + x, map(lambda x: x**2, range(10)))))

# not all processes in the pool are necessarily used 
# 
def test_pipe_multiprocess():
    assert pipe(10) | p[lambda x: x**2] | END == 10**2
    assert pipe(10) | p[lambda x: x**2] * 2 | END == 10**2
    assert pipe(100) | range | p[lambda x: x**2] * 3 | sorted | END == [x ** 2 for x in range(100)]

def test_pipe_multithread():
    assert pipe(10) | t[lambda x: x**2] | END == 10**2
    assert pipe(10) | t[lambda x: x**2] * 2 | END == 10**2
    assert pipe(100) | range | t[lambda x: x**2] * 3 | sorted | END == [x ** 2 for x in range(100)]

def test_pipe_multigreenthread():
    assert pipe(10) | [lambda x: x**2] | END == 10**2
    assert pipe(10) | [lambda x: x**2] * 2 | END == 10**2
    assert pipe(10) | g[lambda x: x**2] | END == 10**2
    assert pipe(10) | g[lambda x: x**2] * 2 | END == 10**2
    assert pipe(10000) | range | [lambda x: x**2] * 10000 | sorted | END == [x ** 2 for x in range(10000)]
    assert pipe(10000) | range | g[lambda x: x**2] * 10000 | sorted | END == [x ** 2 for x in range(10000)]

def test_redirect():
    p = pipe(range(10)) | each(str) | ''.join
    result = p | END
    # test file
    filename = 'testfile.txt'
    p > filename
    assert open(filename).read() == result
    p >> filename
    assert open(filename).read() == result * 2
    # clean test file
    os.remove(filename)
