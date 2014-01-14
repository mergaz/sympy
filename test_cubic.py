#!/usr/bin/env python
from sympy import *

x = Symbol('x')

eqs = [
    x**3 - 3*x**2 - 13*x + 15,
    5*x**3 - 8*x**2 - 8*x + 5,
    3*x**3 + 4*x**2 + 2*x,
    2*x**3 - 3,
    (x+3)*(x**2 + 5),
    2*x**3 - 11*x**2 + 12*x +9,
]

for i, eq in enumerate(eqs):
    print 40*"="
    print '=== Equation_'+str(i) + ":"
    print roots(eval(str(eq)))