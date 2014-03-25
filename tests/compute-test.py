#!/usr/bin/env python

from sympy.utilities.compute import compute
from sympy.utilities.solution import *

user_inputs = [
    "x**2+2 = 5",
    "3 + 5",
    "x**2 - 4",
    "integrate(x**2*dx)"
]

for user_input in user_inputs:
    print '===================================================='
    reset_solution()
    res = compute(user_input)
    R = last_solution()
    for r in R:
        print r
    print res