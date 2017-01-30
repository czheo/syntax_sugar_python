from functools import partial
from .composable import compose, composable
from multiprocess.pool import ThreadPool, Pool
from eventlet import GreenPool

__all__ = [
    'END',
    'DEBUG',
    'pipe',
    'each',
    'puts',
    'process_syntax',
    'thread_syntax',
    'green_thread_syntax',
    'p',
    't',
    'g',
]

def puts(data, end="\n"):
    print(data, end=end)
    return data

def each(fn):
    return partial(map, fn)

class End:
    "mark end of pipe"
    pass

END = End()

class Debug:
    "mark end of pipe for debug"
    pass

DEBUG = Debug()

class MultiTaskSyntax:
    def __init__(self):
        self.poolsize = 1
    def __mul__(self, other):
        self.poolsize = other
        return self
    def __getitem__(self, func):
        self.func = func
        return self

class ProcessSyntax(MultiTaskSyntax):
    pass

class ThreadSyntax(MultiTaskSyntax):
    pass

class GreenThreadSyntax(MultiTaskSyntax):
    pass

class EventSyntax(MultiTaskSyntax):
    pass

def multitask(fn, poolsize, data, pool_constructor):
    with pool_constructor(poolsize) as p:
        if not hasattr(data, '__iter__'):
            data= [data]
            return p.map(fn, data)[0]
        else:
            return p.map(fn, data)

def multiprocess(fn, poolsize, data):
    return multitask(fn, poolsize, data, Pool)

def multithread(fn, poolsize, data):
    return multitask(fn, poolsize, data, ThreadPool)

def multigreenthread(fn, poolsize, data):
    p = GreenPool(poolsize)
    if not hasattr(data, '__iter__'):
        data= [data]
        return next(p.imap(fn, data))
    else:
        return list(p.imap(fn, data))


process_syntax = p = ProcessSyntax()
thread_syntax = t = ThreadSyntax()
green_thread_syntax = g = GreenThreadSyntax()

class pipe:
    def __init__(self, data = None):
        # default action does nothing
        self.action = lambda x: x
        self.data = data

    def __call__(*args):
        self = args[0]
        args = args[1:]
        if len(args) == 1:
            return self.action(args[0])
        elif len(args) == 0:
            return self.action(self.data)
        else:
            raise TypeError('pipe takes 0 or 1 argument but %d are given' % len(args))

    def start(self, rhs):
        # pipe start
        self.data = rhs
        self.pipein = True

    def function(self, rhs):
        self.data = rhs(self.data)

    def __or__(self, rhs):
        if rhs is END:
            # end of pipe
            return self.action(self.data)
        elif rhs is DEBUG:
            # debug end of pipe
            try:
                return self.action(self.data)
            except Exception as e:
                return e
        elif isinstance(rhs, list):
            if len(set(rhs)) != 1:
                raise SyntaxError('Bad pipe multiprocessing syntax.')
            poolsize = len(rhs)
            new_action = rhs[0]
            self.action = compose(partial(multigreenthread, new_action, poolsize), self.action)
        elif isinstance(rhs, ProcessSyntax):
            self.action = compose(partial(multiprocess, rhs.func, rhs.poolsize), self.action)
        elif isinstance(rhs, ThreadSyntax):
            self.action = compose(partial(multithread, rhs.func, rhs.poolsize), self.action)
        elif isinstance(rhs, GreenThreadSyntax):
            self.action = compose(partial(multigreenthread, rhs.func, rhs.poolsize), self.action)
        elif isinstance(rhs, tuple):
            self.action = compose(partial(*rhs), self.action)
        elif isinstance(rhs, pipe):
            # connect another pipe
            new_pipe = pipe(self.data) | compose(rhs.action, self.action)
            return new_pipe
        elif hasattr(rhs, '__call__'):
            # middle of pipe
            self.action = compose(rhs, self.action)
        else:
            raise SyntaxError('Bad pipe %s' % rhs)
        return self

    def __gt__(self, rhs):
        "pipe > 'filename'"
        with open(rhs, 'w') as f:
            f.write(str(self.action(self.data)))
    
    def __rshift__(self, rhs):
        "pipe >> 'filename'"
        with open(rhs, 'a') as f:
            f.write(str(self.action(self.data)))
