#!/usr/bin/env python


from sympy import *
from sympy.utilities.solution import *

x = Symbol('x')


eqs = [
    Eq(cos(5*x - pi/6), sqrt(2) / 2),
    Eq(tan(x**2 + 4*x + pi/4), 1),
    Eq(sin(6*x - pi/3), sin(2*x + pi/4)),
    Eq(cos(x**2), cos(4*x - 3)),
    Eq(6*sin(x)**2 - 5*sin(x) + 1, 0),
    Eq(cos(6*x + pi/6)**2, Rational(1, 2)),
    Eq(cos(3*x**2)**2, Rational(3, 4)),
    Eq(5*sin(x)**2 + 3*sin(x) + 4*cos(x)**2, 5 + Rational(3, 4)),
    Eq(sin(x)**4 + 3*cos(x) - cos(x)**4 - 2, 0),
]

for eq in eqs:
    print '===================================================='

    reset_solution()
    res = solve(eq)
    R = last_solution()
    for r in R: 
        print r
    print '=== Answer:'
    for r in res:
        print latex(r)