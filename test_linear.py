#!/usr/bin/env python
from sympy import *

x = Symbol('x')

eqs = [
'(x + 4)',
-9*x + 8 -10*x + 2,
4*x + 7 - -3 - 5+x,
6*x,
2*x + 3,
]

for i, eq in enumerate(eqs):
    print 40*"="
    print '=== Equation_'+str(i)+': ' + str(eq)
    roots(eval(str(eq)))