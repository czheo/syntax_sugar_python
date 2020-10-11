# syntax_sugar [![travis_status](https://travis-ci.org/czheo/syntax_sugar_python.svg?branch=master)](https://travis-ci.org/czheo/syntax_sugar_python) [![PyPI](https://img.shields.io/pypi/v/syntax_sugar.svg)](https://pypi.python.org/pypi/syntax_sugar)

This lib adds some anti-Pythonic "syntactic sugar" to Python.

NOTE: This is merely an experimental prototype to show some potential of operator overloading in Python. Only tested under Python 3.6.0. Anything may evolve without announcement in advance.

Inspired by https://github.com/matz/streem. 

Also, you can watch the last part of this Matz's talk to understand the intuition behind this project.

[![Stream Model](https://img.youtube.com/vi/48iKjUcENRE/0.jpg)](https://youtu.be/48iKjUcENRE?t=39m29s)

# Install
```
pip install syntax_sugar
```

# Use

To test out this lib, you can simply do.

``` python
from syntax_sugar import *
```

For serious use, you can explicitly import each component as explained below ... if you dare to use this lib. 

### pipe
``` python
from syntax_sugar import pipe, END
from functools import partial

pipe(10) | range | partial(map, lambda x: x**2) | list | print | END
# put 10 into the pipe and just let data flow.
# output: [0, 1, 4, 9, 16, 25, 36, 49, 64, 81]
# remember to call END at the end
# NOTE: everything in the middle of the pipe is just normal Python functions

pipe(10) | range | (map, lambda x: x**2) | list | print | END
# Tuples are shortcuts for partial functions

from syntax_sugar import each
x = pipe(10) | range | each(lambda x: x ** 2) | END
# `each` is just a shortcut of the partial function of `map`
# We can also save the result in a variable

pipe(10) | range | each(str) | ''.join > 'test.txt'
# wanna write to a file? Why not!
# write "0123456789" to test.txt
# We don't need to put END here.
```

We can connect multiple pipes to create a longer pipe

``` python
from syntax_sugar import pipe, each, END
from functools import reduce

p1 = pipe(10) | range | each(lambda x: x/2)
# head pipe can have input value
p2 = pipe() | (reduce, lambda acc, x: (acc + x)/2)
p3 = pipe() | int | range | sum
# middle pipes can have no input value

p1 | p2 | p3 | END
# returns 6

# you can also put a different value in the pipe
p = p1 | p2 | p3
p(20)
# returns 36
```

### pipe with parallelism

By default, pipe works with threads.

You can have a function running in a seperate thread with pipe. Just put it in a `[]` or more explicitly `t[]`. Threads and processes are also available.

``` python
from syntax_sugar import (thread_syntax as t,
                          process_syntax as p)

pipe(10) | [print] | END   # print run in a thread
pipe(10) | t[print] | END  # print run in a thread
pipe(10) | p[print] | END  # print run in a process
```

What makes this syntax good is that you can specify how many threads you want to spawn, by doing `[function] * n` where `n` is the number of threads.

``` python
pipe([1,2,3,4,5]) | [print] * 3 | END # print will run in a ThreadPool of size 3
```

Here is an example of requesting a list of urls in parallel

``` python
import requests
(pipe(['google', 'twitter', 'yahoo', 'facebook', 'github'])
    | each(lambda name: 'http://' + name + '.com')
    | [requests.get] * 3   # !! `requests.get` runs in a ThreadPool of size 3
    | each(lambda resp: (resp.url, resp.headers.get('Server')))
    | list
    | END)

# returns
# [('http://www.google.com/', 'gws'),
#  ('https://twitter.com/', 'tsa_a'),
#  ('https://www.yahoo.com/', 'ATS'),
#  ('https://www.facebook.com/', None),
#  ('https://github.com/', 'GitHub.com')]
```

### infix function
``` python
from syntax_sugar import is_a, has, to, step, drop

1 /is_a/ int
# equivalent to `isinstance(1, int)`

range(10) /has/ '__iter__'
# equivalent to `hasattr(range(10), "__iter__")`

1 /to/ 10
# An iterator similar to `range(1, 11)`.
# Python's nasty range() is right-exclusive. This is right-inclusive.

10 /to/ 1
# We can go backward.

'0' /to/ '9'
# We can also have a range of characters :)

1 /to/ 10 /step/ 2
# We can also specify step sizes.
# Similar to `range(1, 11, 2)`

10 /to/ 1 /step/ 2
# Go backward.
# Similar to `range(10, 0, -2)`

1 /to/ 10 /drop/ 5
# there is a `drop` functon which drop N items from the head
# An iterator similar to [6, 7, 8, 9, 10]
```

`/to/` has some advanced features

- lazy evaluation.
- support infinity.
- support product operation.
- support pipe.

``` python
from syntax_sugar import INF, take, each

# CAUTION: this will infinitely print numbers
for i in 1 /to/ INF:
    print(i)

1 /to/ INF /take/ 5 /as_a/ list
# there is a `take` functon which is similar to itertools.islice
# return [1, 2, 3, 4, 5]

0 /to/ -INF /step/ 2 /take/ 5 /as_a/ list
# also works with negative infinity.
# return [0, -2, -4, -6, -8]

(1 /to/ 3) * (4 /to/ 6) /as_a/ list
# all combinations of [1..3] * [4..6]
# return [(1, 4), (1, 5), (1, 6), (2, 4), (2, 5), (2, 6), (3, 4), (3, 5), (3, 6)]

1 /to/ 10 /take/ 5 | each(lambda x: x **2) | list | END
# These infix functions can also be piped.
# [1, 4, 9, 16, 25]
```

Make your own infix function, so you can append multiple items to a list in one line.

``` python
from syntax_sugar import infix

@infix
def push(lst, x):
    lst.append(x)
    return lst

[] /push/ 1 /push/ 2 /push/ 3
# returns [1,2,3]
```

You can also do

``` python
def push(lst, x):
    lst.append(x)
    return lst

ipush = push /as_a/ infix

[] /ipush/ 1 /ipush/ 2 /ipush/ 3
# returns [1,2,3]
```

<!---
### stream

``` python
from syntax_sugar import stream, take

list(stream() << [1,2,3] << range(5))
# [1,2,3,0,1,2,3,4]
# stream will connect all sequences together

list((stream() << [1, 1] << (lambda x, y: x + y)) /take/ 10)
# [1, 1, 2, 3, 5, 8, 13, 21, 34, 55]
# This is the first 10 items of an infinite fibonacci stream
# If a function is met, stream will infinitely take the last N previous items as the input of the lambda to generate the next item.
```
-->


### function composition

In math, `(f * g) (x) = f(g(x))`. This is called function composition.

``` python
# lmap equivalent to `list(map(...))`
lmap = compose(list, map)
lmap(lambda x: x ** 2, range(10))
```

Let's say we want to represent `f * g * h` in a program, i.e. `fn(x) = f(g(h(x)))`

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

Sometimes you may prefer the decorator way.

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

More receipes: https://github.com/czheo/syntax_sugar_python/tree/master/recipes
