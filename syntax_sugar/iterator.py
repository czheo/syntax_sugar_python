from itertools import product

INF = float('inf')
NEGINF = float('-inf')

class Iterator:
    def __init__(self, start, end, step=None):
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
        self._step = step if step != None else 1 if end > start else -1
        self.end = end

        validate_range(self.start, self.end, self._step)


    @property
    def step(self):
        return self._step

    @step.setter
    def step(self, value):
        validate_range(self.start, self.end, value)
        self._step = value

    def __mul__(self, rhs):
        return product(self, rhs)

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
            return super(Iterator, self).__str__()
        elif self.type == 'char':
            return ''.join(self)
        else:
            raise NotImplementedError

def validate_range(start, end, step):
    if not isinstance(step, int):
        raise TypeError('Step must be int')
    elif step == 0:
        raise ValueError('Step cannot be zero')
    elif start < end and step < 0:
        raise ValueError('Increasing range with negative step')
    elif start > end and step > 0:
        raise ValueError('Decreasing range with positive step')

__all__ = [
    'INF',
    'NEGINF',
    'Iterator',
]
