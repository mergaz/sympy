#!/usr/bin/env python

# Trigonometric equations reducible to algebraic equations.

from sympy import *
from sympy.utilities.solution import *
from sympy.utilities.solution_log import log_as_latex, log_to_file

x = Symbol('x')

eqs = [
    asin(x) - 1,
    asin(2 * x + 1) - 0,
    asin(x) + 4,
    acos(x - 3) - pi / 2,
    acos(x) + 1,
    atan(x) - pi,
    acot(2 *x - 4) - pi / 3,
    5 * cos(x) ** 2 - 5 * cos(x) + 1,
    8 * cos(x) ** 2 + 6 * sin(x) - 3,
    3 * tan(x) ** 3 + tan(x),
    sin(3 * x) * cos(4 * x),
    sin(x) + sin(2 * x) + sin(3 * x),
    2 * sin(x) + 3 * sin(2 * x) + 2 * sin(3 * x)
]

for i, eq in enumerate(eqs):
    print '===================================================='
    print '=== Equation: ' + latex(eq) + ' = 0'

    reset_solution()
    res = solve(eq, x)
    R = last_solution()
    for r in R: 
        print r
    print '=== Answer:'
    for r in res:
        print latex(r)
    log_to_file('log{}.tex'.format(i), log_as_latex(R))
