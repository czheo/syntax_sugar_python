from functools import partial
from .composable import compose

__all__ = [
    'ret',
    'pipe',
    'each',
    'where',
    'concat',
    'puts',
]

ret = None

def puts(data):
    print(data, end='')
    return data

def each(fn):
    return partial(compose(list, map), fn)

def where(fn):
    return partial(compose(list, filter), fn)

def concat(lst):
    return ''.join(lst)

class pipe:
    def __init__(self, data = None):
        self.data = data

    def __or__(self, right):
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
