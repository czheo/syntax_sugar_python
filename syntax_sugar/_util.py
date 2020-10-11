from ._infix import infix
from ._iter import Iterator, Range

__all__ = [
    'flip',
    'is_a',
    'as_a',
    'to',
    'step',
    'has',
    'take',
    'drop',
]

def flip(fn):
    def wrapper(*args):
        return fn(args[1], args[0])
    return wrapper

is_a = infix(isinstance)
has = infix(hasattr)

@infix
def as_a(obj, clazz):
    return clazz(obj)

@infix
def to(start, end):
    return Iterator(Range(start, end))

@infix
def step(obj, step):
    step = abs(step)
    obj = Iterator(obj) if not obj /is_a/ Iterator else obj
    return obj.slice(step=step)

@infix
def take(obj, n):
    obj = Iterator(obj) if not obj /is_a/ Iterator else obj
    return obj.slice(stop=n)

@infix
def drop(obj, n):
    obj = Iterator(obj) if not obj /is_a/ Iterator else obj
    return obj.slice(start=n)
