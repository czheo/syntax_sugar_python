from functools import partial
from functools import reduce


__all__ = [
    'composable',
    'compose',
]

class composable(partial):
    def __mul__(self, func):
        return lambda *args, **kwargs: self(func(*args, **kwargs))

    def __rmul__(self, func):
        return lambda *args, **kwargs: func(self(*args, **kwargs))

def compose(*args):
    return reduce(lambda acc, fn:
        (lambda *ag, **kwag: acc(fn(*ag, **kwag))),
    args)
