#!/usr/bin/env python

from sympy import *
from sympy.utilities.solution import *

x = Symbol('x')

exs = [
    x**2,
    0,
    x + 1,
    sqrt(x),
    exp(x),
    log(x),
    exp(x) * sin(x),
    2 * x * cos(x**2),
    (1 - x)**6,
    1/(x + 5),
    x**2 * (5 - x)**4,
    x * cos(x),
    1 / (2 + x**2),
    sqrt(1+x**2) / sqrt(1 - x**4),
    1 / sqrt(25 - x**2),
    1 / sqrt(4 - 9*x**2),
    1 / sqrt(9*x**2 - 4),
]

for ex in exs:
    print '===================================================='
    print '=== Expression ' + latex(ex)

    reset_solution()
    res = integrate(ex, x)
    R = last_solution()
    for r in R:
        print r
    print '=== Answer:'
    print latex(res)

