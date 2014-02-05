#!/usr/bin/env python

from sympy import *

x = Symbol('x')
y = Symbol('y')
print solve([x+1 > x*2, x >0], x)