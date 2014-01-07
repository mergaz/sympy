#!/usr/bin/env python
from sympy import *

x = Symbol('x')

eqs = [
6*x - 12 - 5*x - 4,
-9*x + 8 - -10*x + 2,
7*x + 1 - 8*x - 9,
-12*x - 3 - 11*x + 3,
4 + 25*x - 6 - 24*x,
11 - 5*x - 12 + 6*x,
4*x + 7 - -3 - 5+x,
6 - 2*x - 8 + 3*x,
6*x,
2*x + 3,
2*x**2 - 4*x - 3
]

for i,eq in enumerate(eqs):
    print 20*"="
    print '=== Equation_'+str(i)+': ' + latex(eq)
    roots(eq)