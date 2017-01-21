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
        if hasattr(args[0], '__iter__'):
            return reduce(lambda acc, x: acc * x, map(composable, args[0]))
        elif hasattr(args[0], '__call__'):
            return composable(args[0])
        else:
            raise TypeError('Unknown Args: %s' % args)
    else:
        return reduce(lambda acc, x: acc * x, map(composable, args))
