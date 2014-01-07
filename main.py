#!/usr/bin/env python

from sympy import *

x = Symbol('x')
y = Symbol('y')
print solve(x*6 + y*2, x, y)