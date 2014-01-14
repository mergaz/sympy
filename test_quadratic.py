#!/usr/bin/env python
from sympy import *

x = Symbol('x')

eqs = [
    2*x**2 - 4*x - 3,
    2*(x**2 -1),
    x**2 - 3*x**2 - 13*x**2 + 15,
    x**2 + 1
]

for i, eq in enumerate(eqs):
    print 40*"="
    print '=== Equation_'+str(i) + ":"
    roots(eval(str(eq)))