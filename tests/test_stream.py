from syntax_sugar import *

def test_stream_collection():
    assert list(stream() << [1,2,3] << [4,5,6]) == list([1,2,3,4,5,6])
    assert list(stream() << [1,2,3] << range(4,7)) == list([1,2,3,4,5,6])

def test_stream_function():
    assert list((stream() << [1,2,3] << (lambda x: x+1)) /take/ 5) == list([1,2,3,4,5])
    assert list((stream() << [1,2,3] << (lambda x: x+1)) /drop/ 3 /take/ 5) == list([4,5,6,7,8])
    assert list((stream() << range(1,10) << (lambda x: x+1)) /drop/ 3 /take/ 5) == list([4,5,6,7,8])
