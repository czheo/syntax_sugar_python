# syntax_sugar [![travis_status](https://travis-ci.org/czheo/syntax_sugar_python.svg?branch=master)](https://travis-ci.org/czheo/syntax_sugar_python)

This lib adds some syntactic sugar to Python.

NOTE: This is merely a prototype. Only tested under Python 3.6.0. Everything is evolving.

Inspired by https://github.com/matz/streem. 

# Install
```
pip install syntax_sugar
```

# Usage
This is the only line you need to use this lib.
```
from syntax_sugar import *
```

### pipe
``` python
# put 10 into the pipe and just let data flow.
pipe(10) | range | each(lambda x: x ** 2) | print
# output: [0, 1, 4, 9, 16, 25, 36, 49, 64, 81]

# save the result to a var
x = pipe(10) | range | each(lambda x: x ** 2) | dump()
# remember to call dump at the end, so the pipe will know you want to dump the value

# wanna write to a file? Why not!
pipe(10) | range | (map, str) | concat > 'test.txt'
# write "0123456789" to test.txt
```

### pipe with thread/process and multiprocessing

You can have a function running in a seperate thread with pipe. Just put it in a `[]` or more explicitly `t[]`.

Because of the notorious GIL(Global Interpret Lock) of Python, people may want processes instead of threads. Just put a function in `p[]`.

``` python
pipe(10) | [print]   # print run in a thread
pipe(10) | t[print]  # print run in a thread
pipe(10) | p[print]  # print run in a process
```

What makes this syntax good is that you can specify how many threads you want to spawn, by doing `[function] * n` where `n` is the number of threads.

``` python
pipe([1,2,3,4,5]) | [print] * 3  # print will run in a ThreadPool of size 3
```

Here is an example of requesting a list of urls in parrallel

``` python
import requests
(
(pipe(['google', 'twitter', 'yahoo', 'facebook', 'github'])
    | each(lambda name: 'http://' + name + '.com')
    | [requests.get] * 3   # !! `requests.get` runs in a ThreadPool of size 3
    | each(lambda resp: (resp.url, resp.headers.get('Server')))
    | dump())
)

# returns
# [('http://www.google.com/', 'gws'),
#  ('https://twitter.com/', 'tsa_a'),
#  ('https://www.yahoo.com/', 'ATS'),
#  ('https://www.facebook.com/', None),
#  ('https://github.com/', 'GitHub.com')]
```

### infix function
``` python
1 /of/ int
# equivalent to `isinstance(1, int)`

[1,2,3,4,5] /contains/ 3
# equivalent to `3 in [1,2,3,4,5]`

1 /to/ 10
# equivalent to `range(1, 11)`
# Python's nasty range() is right-exclusive. This is right-inclusive.

'0' /to/ '9'
# we can also have a range of characters :)
# '0123456789'

# make your own infix functions
@infix
def plus(a, b):
    return a + b

1 /plus/ 2
# returns 3
```

### composable function

In math, `(f * g) (x) = f(g(x))`. This is called function composition.

``` python
# this transfer a map object to list
lmap = compose(list, map)
# lmap equivalent to `list(map(...))`
lmap(lambda x: x ** 2, range(10))
```

Let's try some math.
```
f(x) = x^2 + 1
g(x) = 2x - 1
h(x) = -2x^3 + 3
```
We want to represent `f * g * h` in a program, i.e. `fn(x) = f(g(h(x)))`
``` python
f = lambda x: x**2 + 1
g = lambda x: 2*x - 1
h = lambda x: -2 * x**3 + 3

fn = compose(f, g, h)

fn(5) # 245026
```
or you can do
```python
f = composable(lambda x: x**2 + 1)
g = composable(lambda x: 2*x - 1)
h = composable(lambda x: -2 * x**3 + 3)

fn = f * g * h

fn(5) # 245026
```

Some times you may prefer the decorator way.

``` python
# make your own composable functions
@composable
def add2(x):
    return x + 2

@composable
def mul3(x):
    return x * 3

@composable
def pow2(x):
    return x ** 2
    
fn = add2 * mul3 * pow2
# equivalent to `add2(mul3(pow2(n)))`
fn(5)
# returns 5^2 * 3 + 2 = 77
```

more receipes: https://github.com/czheo/syntax_sugar_python/tree/master/receipes
