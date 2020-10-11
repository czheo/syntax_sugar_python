from .pipe import pipe
from itertools import tee, islice

INF = float('inf')
NEGINF = float('-inf')

class Iterator:
    def __init__(self, data):
        if hasattr(data, '__iter__'):
            self.data = iter(data)
        else:
            raise TypeError('input must be iterable data')

    def __or__(self, rhs):
        return pipe(self) | rhs

    def __iter__(self):
        return self

    def __mul__(self, rhs):
        def product(rhs):
            for e1 in self:
                rhs, rhs_copy = tee(rhs)
                for e2 in rhs_copy:
                    yield (e1, e2)
        return Iterator(product(rhs))

    def __next__(self):
        return next(self.data)

    def slice(self, start=0, stop=None, step=1):
        return Iterator(islice(self.data, start, stop, step))

class Range:
    def __init__(self, start, end):
        if start in {INF, NEGINF}:
            raise ValueError('Cannot start range from infinity')

        valid_char = lambda c: isinstance(c, str) and len(c) == 1
        valid_integer = lambda i: isinstance(i, int) or i == INF or i == NEGINF

        if valid_integer(start) and valid_integer(end):
            self.type = 'number'
        elif valid_char(start) and valid_char(end):
            self.type = 'char'
        else:
            raise TypeError('Unknown range: %s to %s' % (start, end))

        self.start = start
        self.curr = self.start
        self._step = 1 if end > start else -1
        self.end = end

    @property
    def step(self):
        return self._step

    @step.setter
    def step(self, value):
        if not isinstance(value, int):
            raise TypeError('Step must be int')
        elif value == 0:
            raise ValueError('Step cannot be zero')
        elif self.start < self.end and value < 0:
            raise ValueError('Increasing range with negative step')
        elif self.start > self.end and value > 0:
            raise ValueError('Decreasing range with positive step')
        
        self._step = value

    def __iter__(self):
        return self
    
    def __next__(self):
        def next_number():
            too_big = self.step > 0 and self.curr > self.end
            too_small = self.step < 0 and self.curr < self.end

            if too_big or too_small: raise StopIteration

            ret = self.curr
            self.curr += self.step
            return ret

        def next_char():
            too_big = self.step > 0 and ord(self.curr) > ord(self.end)
            too_small = self.step < 0 and ord(self.curr) < ord(self.end)

            if too_big or too_small: raise StopIteration
            
            ret = self.curr
            self.curr = chr(ord(self.curr) + self.step)
            return ret
            
        if self.type == 'number':
            return next_number()
        elif self.type == 'char':
            return next_char()
        else:
            raise StopIteration
    
    def __str__(self):
        if self.type == 'number':
            return super(Range, self).__str__()
        elif self.type == 'char':
            return ''.join(self)
        else:
            raise NotImplementedError
