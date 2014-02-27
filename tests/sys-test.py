#!/usr/bin/env python

from sympy import *
from sympy.utilities.solution import *

x = Symbol("x")
y = Symbol("y")
z = Symbol("z")

eqs = [
    [x**2 + x*y + y**2 - 4, x + x*y + y - 2],
    [(x + 1)*(y + 1) - 10, (x + y)*(x*y + 1) - 25],
    [x + y - 1, x**4 + y**4 - 7],
    [x**2 + y**2 - 5*x*y / 2, x - y - x*y / 4],
    [3*x - 2*y - 5, 81*x**4 + 16*y**4 - 6817],
    [x**2 + y**2 - 1, x - y],
    [x + x*y + y - 11, x**2*y + x*y**2 - 30],
    [2*x**2 - 3*x*y + y**2, y**2 - x**2 - 12],
    [x**2 + y**4 - 20, 2*x**4 + 2*y**2 - 40],
]

for eq in eqs:
    print '===================================================='
    reset_solution()
    res = solve(eq)
    R = last_solution()
    for r in R:
        print r
    print '=== Answer:'
    if len(res) == 0:
        print "There is no solution"
    else:
        for r in res:
            print latex(r)