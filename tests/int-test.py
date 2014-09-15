#!/usr/bin/env python

from sympy import *
from sympy.utilities.solution import *

x = Symbol('x')
a = Symbol('a')
exs = [
    "x**2/sqrt(x + 1)",
    "(2*x + 2)/(1 + 2*x)^(1/3)",
    "1 / (3 + 2*x**2)",
    E**(x) * sin(x),
    x * cos(x**2),
    (1 - x)**6,
    1/(x + 5),
    x**2 * (5 - x)**4,
    x * cos(x),
    1 / (2 + x**2),
    sqrt(1+x**2) / sqrt(1 - x**4),
    "2 - x**3 + 1/x**3",
    "x - 2/x**5 + cos(x)",
    "1/x**2 - sin(x)",
    "5*x**2 - 1",
    "(2*x - 3)**5",
    "3*sin(2*x)",
    "(4 - 5*x)**7",
    "-1/3*cos(x/3 - pi/4)",
    "1/(4 - 15*x)**4",
    "1/sqrt(2-x)",
    "(cos(x/4) + sin(x/4))**2",
    "x + sqrt(x)/x",
    "x*sqrt(1 + x**2)",
    "x*sqrt(1 + x)",
    "1/sqrt(2*x+3)",
    "cot(x)",
    "x*(1 - x/2)**(1/3)",
    "x/sqrt(2*x + 1)",
    "1/(cos(pi/3 - x))**2",
    "1/(cos(4*x))**2",
    "1/(sin(x + 1))**2",
    "x*exp(x**2)",
    "x*exp(-x**2)",
    "(x**2 + x + 1)**2",
    "(x**2 - 1) / (x**2 + 1)"
]

for ex in exs:
    print "\\rule{10cm}{0.4pt} \n"
#    print '=== Expression ' + latex(ex)

    reset_solution()
    res = integrate(ex, x)
    R = last_solution()
    for r in R:
        print r
#    print '=== Answer:'
#    print latex(res)

