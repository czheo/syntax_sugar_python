from functools import partial, reduce
from itertools import product, islice
from .util import flip
from .composable import compose

class infix(partial):
    def __truediv__(self, right):
        return self(right)

    def __rtruediv__(self, left):
        return infix(self.func, left)

of = infix(isinstance)
contains = infix(lambda lst, item: item in lst)
pair = infix(lambda a, b: (a, b))
join = infix(lambda lst, s: s.join(lst))
hasattr = infix(hasattr)
fmap = infix(flip(map))
ffilter = infix(flip(filter))
freduce = infix(flip(reduce))
take = infix(compose(list, islice))

INF = float('inf')

class To:
    def __init__(self, start, end):
        if start /of/ int and (end /of/ int or end == INF):
            self.type = 'number'
            self.start = start
            self.curr = self.start
            self.end = end
        elif start /of/ str and end /of/ str:
            self.type = 'char'
            self.start = start
            self.curr = self.start
            self.end = end
        else:
            raise TypeError('Unknown range: %s to %s' % (start, end))

    def __mul__(self, rhs):
        return product(self, rhs)

    def __iter__(self):
        return self
    
    def __next__(self):
        if self.type == 'number':
            if self.curr <= self.end:
                ret = self.curr
                self.curr += 1
                return ret
            else:
                raise StopIteration
        elif self.type == 'char':
            if ord(self.curr) <= ord(self.end):
                ret = self.curr
                self.curr = chr(ord(self.curr) + 1)
                return ret
            else:
                raise StopIteration
        else:
            raise StopIteration
    
    def __str__(self):
        if self.type == 'number':
            return super(To, self).__str__()
        elif self.type == 'char':
            return ''.join(self)
        else:
            raise NotImplementedError

@infix
def to(start, end):
    return To(start, end)

__all__ = [
    'infix',
    'of',
    'contains',
    'pair',
    'join',
    'to',
    'INF',
    'hasattr',
    'fmap',
    'freduce',
    'ffilter',
    'take',
]
