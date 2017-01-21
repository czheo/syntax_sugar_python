from functools import partial, reduce
from .util import flip

class infix(partial):
    def __truediv__(self, right):
        return self(right)

    def __rtruediv__(self, left):
        return infix(self.func, left)

of = infix(isinstance)
contains = infix(lambda lst, item: item in lst)
pair = infix(lambda a, b: (a, b))
join = infix(lambda lst, s: s.join(lst))
to = infix(lambda frm, to: range(frm, to))
x = infix(lambda l1, l2: list(map(lambda x, y: x * y, l1, l2)))
hasattr = infix(hasattr)
fmap = infix(flip(map))
ffilter = infix(flip(filter))
freduce = infix(flip(reduce))

__all__ = [
    'infix',
    'of',
    'contains',
    'pair',
    'join',
    'to',
    'x',
    'hasattr',
    'fmap',
    'freduce',
    'ffilter',
]
