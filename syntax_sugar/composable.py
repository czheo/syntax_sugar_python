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
    if len(args) == 1:
        return args[0]
    if len(args) == 2:
        return lambda *ag, **kwag: args[0](args[1](*ag, **kwag))
    else:
        return compose(compose(args[:-1]), args[-1])
