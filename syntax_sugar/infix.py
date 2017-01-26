from functools import partial, reduce
from itertools import product, islice
from .util import flip
from .composable import compose
from .pipe import Iterator

class infix(partial):
    def __truediv__(self, right):
        return self(right)

    def __rtruediv__(self, left):
        return infix(self.func, left)

is_a = of = infix(isinstance)
contains = infix(lambda lst, item: item in lst)
pair = infix(lambda a, b: (a, b))
join = infix(lambda lst, s: s.join(lst))
hasattr = infix(hasattr)
fmap = infix(flip(map))
ffilter = infix(flip(filter))
freduce = infix(flip(reduce))
take = infix(compose(list, islice))
drop = infix(lambda seq, idx: islice(seq, idx, None))

@infix
def to(start, end):
    return Iterator(start, end)

@infix
def by(iterator, step):
    if iterator.end >= iterator.start and step < 0:
        iterator.step = -step
    elif iterator.end <= iterator.start and step > 0:
        iterator.step = -step
    else:
        iterator.step = step

    return iterator


__all__ = [
    'infix',
    'of',
    'is_a',
    'contains',
    'pair',
    'join',
    'to',
    'by',
    'hasattr',
    'fmap',
    'freduce',
    'ffilter',
    'take',
    'drop',
]
