#!/usr/bin/env python

from sympy import *
from sympy.utilities.solution import *

x = Symbol('x')
y = Function('y')
eqs = [
    Derivative(y(x), x) - 3*y(x)*x, # separable
    y(x).diff(x, 4) + 2*y(x).diff(x, 3) - 2*y(x).diff(x, 2) - 6*y(x).diff(x) + 5*y(x), # LHDE with CC
    y(x).diff(x) - y(x) - y(x)**2 * exp(x), # Bernoulli eq
    y(x).diff(x, 2)*x**2 - 4*y(x).diff(x)*x + 6*y(x), # Euler eq
    cos(y(x)) - (x*sin(y(x)) - y(x)**2)*y(x).diff(x), # exact
    y(x).diff(x, 2) + 2*y(x).diff(x) + y(x) - 4*exp(-x)*x**2 + cos(2*x),
    y(x).diff(x, 3) - 3*y(x).diff(x, 2) + 3*y(x).diff(x) - y(x) - exp(x)*log(x),
]

for eq in eqs:
    print '===================================================='
    print '=== Equation: ' + latex(eq) + ' = 0'

    reset_solution()
    res = dsolve(eq, y(x))
    R = last_solution()
    for r in R: 
        print r
    print '=== Answer:'
    print latex(res)
