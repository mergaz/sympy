#!/usr/bin/env python

from sympy import *
from sympy.derivative.manualderivative import derivative
from sympy.utilities.solution import *

x = Symbol('x')

exs = [
    sin(x),
    sin(tan(x)),
    cos(x) + sin(x) + tan(exp(x)),
    sin(sin(sin(x))),
    2**x,
    x**2,
    x**x,
    sin(x)**2,
    2**exp(x),
    x**sin(x),
    log(x),
    log(sin(x)),
    log(x, 2),
    sin(x) / exp(x),
    exp(x) / x,
    cos(4) * cos(x) * 4 * sin(x),
    sin(3),
    x

]

for ex in exs:
    print '===================================================='
    print '=== Expression ' + latex(ex)

    reset_solution()
    res = derivative(ex, x)
    R = last_solution()
    for r in R:
        print r
    print '=== Answer:'
    print latex(res)

