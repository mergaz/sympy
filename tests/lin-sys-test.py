#!/usr/bin/env python

from sympy import *
from sympy.utilities.solution import *

x = Symbol("x")
y = Symbol("y")
z = Symbol("z")

a = Symbol("a")

eqs = [
    [x - 3*y + z - 4, 2*x - 8*y + 8*z + 2, -6*x + 3*y - 15*z - 9],
    [x - 3*y + z - 4, 2*x - 8*y + 8*z + 2,],
    [x - 3*y + z - 4, 2*x - 8*y + 8*z + 2, 2*x - 8*y + 8*z + 3],
#    [y + z - 1, x - y + z, 2*x - 2*y + 2*z, 2 * x + y, 2 * x + y, y + z - 1, y + z - 1],
#    [y + z - 1, y + z, 2*x - 2*y + 2*z, 2 * x + y, 2 * x + y, y + z - 1, 2 * y + z - 1],
    [x - y + 2*z + 3, 4*x + 4*y - 2*z - 1, -2*x + 2*y - 4*z - 6],
    [x - y, x + y + a],
    [x - y, 2*x - 2*y, -x + y - 3]
]

for eq in eqs:
    print '===================================================='
    reset_solution()
    res = solve(eq, [x, y, z])
    R = last_solution()
    for r in R:
        print r
    print '=== Answer:'
    if len(res) == 0:
        print "There is no solution"
    else:
        for r, s in res.items():
            print latex(r), '=',  latex(s)