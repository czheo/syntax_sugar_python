from syntax_sugar import pipe, ret

def test_empty_pipe():
    assert pipe() | 10 | ret == 10

def test_pipe_with_number():
    assert pipe(10) | ret == 10

def test_pipe_with_list():
    assert pipe([1,2,3,4]) | ret == [1,2,3,4]
