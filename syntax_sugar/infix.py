from functools import partial
from .iter import Iterator, Range

__all__ = [
    'infix',
    'is_a',
    'to',
    'step',
    'INF',
    'NEGINF',
    'has',
    'take',
    'drop',
]

INF = float('inf')
NEGINF = float('-inf')

class infix(partial):
    def __truediv__(self, right):
        return self(right)

    def __rtruediv__(self, left):
        return infix(self.func, left)

is_a = infix(isinstance)
has = infix(hasattr)

@infix
def to(start, end):
    return Iterator(Range(start, end))

@infix
def step(obj, step):
    # ex. -2 step -> 2 step
    step = abs(step)
    obj = Iterator(obj) if not obj /is_a/ Iterator else obj
    return obj.slice(step=step)

@infix
def take(obj, n):
    # ex. n = 3
    # [0, 1, 2, 3, 4, 5, 6] =>
    # [0, 1, 2]
    obj = Iterator(obj) if not obj /is_a/ Iterator else obj
    return obj.slice(stop=n)

@infix
def drop(obj, n):
    # ex. n = 3
    # [0, 1, 2, 3, 4, 5, 6] =>
    # [3, 4, 5, 6]
    obj = Iterator(obj) if not obj /is_a/ Iterator else obj
    return obj.slice(start=n)
