from functools import partial
from functools import reduce


__all__ = [
    'composable',
    'compose',
]

class composable(partial):
    def __mul__(self, rhs):
        return lambda *args, **kwargs: self(rhs(*args, **kwargs))

    def __rmul__(self, lhs):
        return lambda *args, **kwargs: lhs(self(*args, **kwargs))

def compose(*args):
    return reduce(lambda acc, fn:
        (lambda *ag, **kwag: acc(fn(*ag, **kwag))),
    args)
