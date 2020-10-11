from itertools import chain
from inspect import getfullargspec

__all__ = [
    'stream',
]

class StreamIter:
    def __init__(self, fn, data):
        self.fn = fn
        self.fn_argc = len(getfullargspec(fn).args)
        self.data = data
        self.prev = []

    def __iter__(self):
        return self

    def __next__(self):
        try:
            ret = next(self.data)
            self.prev.append(ret)
            while len(self.prev) > self.fn_argc:
                self.prev.pop(0)
            return ret
        except StopIteration:
            ret = self.fn(*self.prev)
            self.prev.append(ret)
            while len(self.prev) > self.fn_argc:
                self.prev.pop(0)
            return ret

class stream:
    def __init__(self, data = None):
        if data is None:
            self.data = iter([])
        else:
            self.data = iter(data)

    def __iter__(self):
        return self

    def __next__(self):
        return next(self.data)
    
    def __lshift__(self, rhs):
        if hasattr(rhs, '__iter__'):
            self.data = chain(self.data, rhs)
        elif hasattr(rhs, '__call__'):
            self.data = StreamIter(rhs, self.data)
        return self
