from .pipe import END

__all__ = [
    'match',
]

class match:
    def __init__(self, x):
        self.x = x
        self.done = False
        self.result = None

    def __or__(self, rhs):
        if rhs is END:
            return self.result
        if self.done:
            return self
        if isinstance(rhs, dict):
            result = rhs.get(self.x, None)
            if result:
                self.done = True
                self.result = result
            return self
        if isinstance(rhs, tuple):
            patt, fn = rhs
            if self.x == patt:
                self.done = True
                self.result = fn()
            return self
        else:
            raise SyntaxError('Bad match syntax.')
