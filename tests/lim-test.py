#!/usr/bin/env python

from sympy import *
from sympy.utilities.solution import *

x = Symbol('x')

exs = [
    ((x**2 - 1) / (2*x**2 - x - 1), oo),
    ((x**2 - 5*x + 6) / (x**2 - 8*x + 15), 3),
    (sin(10 * x) / tan(3 * x), 0),
    ((tan(x) - sin(x)) / sin(x)**3, 0),
    ((sqrt(1 + 2*x) - 3) / (sqrt(x) - 2), 4),
    ((sqrt(1 + x) - sqrt(1 - x)) / ((1 + x)**Rational(1, 3) - (1 - x)**Rational(1, 3)), 0),
    ((1 + sin(x))**(1 / x), 0)
]

for ex in exs:
    print '===================================================='
    print '=== Expression ' + latex(ex)

    reset_solution()
    res = lim(ex[0], x, ex[1])
    R = last_solution()
    for r in R:
        print r
    print '=== Answer:'
    print latex(res)

