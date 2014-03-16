#!/usr/bin/env python

from sympy import *
from sympy.utilities.solution import *

x = Symbol("x", real=True)

a = Symbol("a")
b = Symbol("b")
c = Symbol("c")


eqs = [
#    [x**2 - 5*x + 3 > 0],
#    [x**2 - 5*x + 3 <= 0],
    [x**2 - 5*x + 3 < 0],
#    [x**2 - 5*x + 3 >= 0, x > 0],
    [(x**2 - 5*x + 3) / (x - 3) >= 0],
#    [Abs(4 * x + 1) - 4 > 0]

]

for eq in eqs:
    print '===================================================='
    print '=== Inequality: ' + latex(eq)

    reset_solution()
    res = solve(eq, x)
    R = last_solution()
    for r in R:
        print r
    print '=== Answer:'
    print latex(res)