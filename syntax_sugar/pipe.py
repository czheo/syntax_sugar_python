from functools import partial
from .composable import compose, composable
from multiprocess.pool import ThreadPool, Pool

__all__ = [
    'END',
    'pipe',
    'each',
    'puts',
    'process_syntax',
    'thread_syntax',
    'p',
    't',
]

def puts(data, end="\n"):
    print(data, end=end)
    return data

def each(fn):
    return partial(map, fn)

class end:
    "mark end of pipe"
    pass

END = end()

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

def multiprocess(fn, poolsize, data):
    p = Pool(poolsize)
    if not hasattr(data, '__iter__'):
        data= [data]
        return p.map(fn, data)[0]
    else:
        return p.map(fn, data)

def multithread(fn, poolsize, data):
    p = ThreadPool(poolsize)
    if not hasattr(data, '__iter__'):
        data= [data]
        return p.map(fn, data)[0]
    else:
        return p.map(fn, data)

process_syntax = p = ProcessSyntax()
thread_syntax = t = ThreadSyntax()

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
        if isinstance(rhs, end):
            # end of pipe
            return self.action(self.data)
        elif isinstance(rhs, list):
            if len(set(rhs)) != 1:
                raise SyntaxError('Bad pipe multiprocessing syntax.')
            poolsize = len(rhs)
            new_action = rhs[0]
            self.action = compose(partial(multithread, new_action, poolsize), self.action)
        elif isinstance(rhs, MultiProcess):
            self.action = compose(partial(multiprocess, rhs.func, rhs.poolsize), self.action)
        elif isinstance(rhs, MultiThread):
            self.action = compose(partial(multithread, rhs.func, rhs.poolsize), self.action)
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
