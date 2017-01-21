from functools import partial
from .composable import compose

__all__ = [
    'ret',
    'dump',
    'pipe',
    'each',
    'where',
    'concat',
    'puts',
    'read',
    'readlines',
]

dump, ret = None, None

def puts(data):
    print(data, end='')
    return data

def each(fn):
    return partial(compose(list, map), fn)

def where(fn):
    return partial(compose(list, filter), fn)

def concat(lst):
    return ''.join(lst)

def read(fd):
    return fd.read()

def readlines(fd):
    return fd.readlines()

class pipe:
    def __init__(self, data = None):
        self.data = data

    def __or__(self, right):
        "pipe | action"
        if right is ret:
            return self.data
        elif isinstance(right, tuple):
            if self.data is None:
                return pipe(partial(*right)())
            else:
                return pipe(partial(*right)(self.data))
        elif hasattr(right, '__call__'):
            if self.data is None:
                return pipe(right())
            else:
                return pipe(right(self.data))
        elif self.data is None:
            return pipe(right)
        else:
            raise TypeError(right)

    def __gt__(self, right):
        "pipe > 'filename'"
        with open(right, 'w') as f:
            f.write(str(self.data))
    
    def __rshift__(self, right):
        "pipe >> 'filename'"
        with open(right, 'a') as f:
            f.write(str(self.data))
