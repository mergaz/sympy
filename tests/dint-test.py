#!/usr/bin/env python

from sympy import *
from sympy.utilities.solution import *

x = Symbol('x')

exs = [
    (x**2, 1, 3),
    (sin(x), 0, 1)
]

for ex in exs:
    print '===================================================='
    print '=== Expression ' + latex(ex)

    reset_solution()
    res = integrate(ex[0], (x, ex[1], ex[2]))
    R = last_solution()
    for r in R:
        print r
    print '=== Answer:'
    print latex(res)

