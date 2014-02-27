#!/usr/bin/env python

from sympy import *
from sympy.utilities.solution import *

x = Symbol("x")

a = Symbol("a")
b = Symbol("b")

eqs = [
    5*x**2 + 2,
    4*x**2 + 3*x,
    2*x**2 - 10*x + 12,
    3*x**3 + 5*x**2 + 2*x - 4,
	6*x**3 - 11*x**2 - 2*x + 8,
    x**4 + 5*x**2 + 1,
	x**4 + x**3 - 11*x**2 - 5*x + 30,
	36*x**4 - 13*x**2 + 1,
	179*x**5 - 12351*x**4 + 22557*x**3 + 95737*x**2 + 378*x + 1608,
    (x + 1)**4 + 5*(x + 1)**2 + 1*(x + 1),
    (x**2 + 6*x + 2)*(x**2 - 4*x + 2),
    ((x + 1)**4)**2 + 5*(x + 1)**4 + 1,
	(3*x + 2)**4 - 13*(3*x + 2)**2 + 36,
	(x + 1) * (x + 2) * (x + 3) * (x + 4) - 24,
    (8*x + 7)**2 * (4*x + 3) * (x + 1) - Rational(9, 2),
]

for eq in eqs:
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