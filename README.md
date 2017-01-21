# syntax_sugar

This lib adds some syntax sugar to Python.

NOTE: This is merely a prototype. Everything is evolving.

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

# wanna write to a file? Why not!
pipe(10) | range | (map, str) | concat > 'test.txt'
# write "0123456789" to test.txt
```

### infix function
``` python
1 /of/ int
# equivalent to `isinstance(1, int)`
[1,2,3,4,5] /contains/ 3
# equivalent to `3 in [1,2,3,4,5]`

# make your own infix functions
@infix
def plus(a, b):
    return a + b

1 /plus/ 2
# returns 3
```

### composable function
``` python
lmap = compose(list, map)
# lmap equivalent to `list(map(...))`
lmap(lambda x: x ** 2, range(10))

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
