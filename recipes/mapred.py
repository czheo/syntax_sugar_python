from syntax_sugar import *
from functools import reduce

(pipe(10)
    | range
    | (map, lambda x: x ** 2)
    | sum
    | print
    | END)
