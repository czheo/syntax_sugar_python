from functools import partial
from .composable import compose, composable
from multiprocess.pool import ThreadPool, Pool

__all__ = [
    'dump',
    'pipe',
    'each',
    'where',
    'concat',
    'puts',
    'read',
    'readlines',
    'process_syntax',
    'thread_syntax',
    'p',
    't',
    'until',
    'when',
    'lazy_pipe',
]

def puts(data):
    print(data)
    return data

def each(fn):
    return partial(compose(list, map), fn)

def where(fn):
    return partial(compose(list, filter), fn)

def concat(lst):
    return ''.join(lst)

def read(fd):
    return fd.read()

def readlines(fd):
    return fd.readlines()

class dump:
    "mark end of pipe"
    pass

class MultiTask:
    def __init__(self, func):
        self.poolsize = 1
        self.func = func
    def __mul__(self, other):
        self.poolsize = other
        return self

class MultiProcess(MultiTask):
    pass

class MultiThread(MultiTask):
    pass

class ProcessSyntax:
    def __getitem__(self, func):
        return MultiProcess(func)

class ThreadSyntax:
    def __getitem__(self, func):
        return MultiThread(func)

p = ProcessSyntax()
t = ThreadSyntax()
process_syntax = p
thread_syntax = t

class pipe:
    def __init__(self, data = None):
        self.pipein = data is not None
        self.data = data

    def start(self, rhs):
        # pipe start
        self.data = rhs
        self.pipein = True

    def partial(self, rhs):
        # partial function
        self.data = partial(*rhs)(self.data)

    def multiprocess(self, func, poolsize):
        p = Pool(poolsize)
        self.data = p.map(func, [self.data] if poolsize == 1 else self.data)

    def multithread(self, func, poolsize):
        p = ThreadPool(poolsize)
        self.data = p.map(func, [self.data] if poolsize == 1 else self.data)

    def function(self, rhs):
        self.data = rhs(self.data)

    def __or__(self, rhs):
        if isinstance(rhs, dump):
            # pipe end, return/dump data
            return self.data
        elif not self.pipein:
            self.start(rhs)
        elif isinstance(rhs, tuple):
            self.partial(rhs)
        elif isinstance(rhs, list):
            if len(set(rhs)) != 1:
                raise SyntaxError('Bad pipe multiprocessing syntax.')
            poolsize = len(rhs)
            func = rhs[0]
            self.multithread(func, poolsize)
        elif isinstance(rhs, MultiProcess):
            self.multiprocess(rhs.func, rhs.poolsize)
        elif isinstance(rhs, MultiThread):
            self.multithread(rhs.func, rhs.poolsize)
        else:
            self.function(rhs)
        return self

    def __gt__(self, rhs):
        "pipe > 'filename'"
        with open(rhs, 'w') as f:
            f.write(str(self.data))
    
    def __rshift__(self, rhs):
        "pipe >> 'filename'"
        with open(rhs, 'a') as f:
            f.write(str(self.data))

#####
# TODO: experiment
# lazy_pipe
#####

def neg(x):
    return not x

class until:
    def __init__(self, cond):
        self.cond = cond

class when:
    def __init__(self, cond):
        self.cond = cond

class lazy_pipe:
    def __init__(self, source):
        self.source = source
        self.func = composable(lambda x: x)

    def __or__(self, rhs):
        if isinstance(rhs, dump):
            # dump termination
            return self.dump()
        elif isinstance(rhs, when):
            return self.when(rhs.cond)
        elif isinstance(rhs, until):
            return self.when(compose(neg, rhs.cond))
        else:
            # read actions
            self.func = composable(rhs) * self.func
        return self

    def dump(self):
        return self.func(self.source)

    def when(self, cond):
        if hasattr(self.source, '__call__'):
            data = self.source()
            while cond(data):
                self.func(data)
                data = self.source()
            return self
        elif hasattr(self.source, '__iter__'):
            for data in self.source:
                if cond(data):
                    self.func(data)
                else:
                    break
            return self
        else:
            raise TypeError('pipeline source need be callable or iterable with until condition')
