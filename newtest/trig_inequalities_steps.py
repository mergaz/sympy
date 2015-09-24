#!/usr/bin/env python

from sympy import *
from sympy.utilities.solution import *
from fractions import Fraction

x = Symbol('x')

ineqs_trig=[
    (cot(x)>=sqrt(3), 53, '161a'),
    (sqrt(3)*cot(-2*x + pi/4) > 1, 54, '161b'),
    (cot(3*x)<=1/sqrt(3), 55, '161v'),
    (3*cot(pi/6+x/2)>-sqrt(3), 56, '161g'),
    (3*sin(x/4) >= 2, 57, '162a'),
    (4*cos(x/3) < -3, 58, '162b'),
    (5*tan(2*x) <= 3, 59, '162v'),
    (Fraction(1,2)*sin(4*x) < Fraction(-1,5), 60, '162g')
]

for ent in ineqs_trig:

    eq = ent[0]
    num_test = ent[1]
    num_taskbook = ent[2]
    print('Inequation: ' + str(eq))
    print('No: ' + str(num_test) + ' in tests, ' + num_taskbook + ' in taskbook')

    reset_solution()

    res = solve(eq, x)
    R = last_solution()

    #TODO: solve() and last_solution() methods
    #should always return iterable values
    if not hasattr(R,'__iter__'):
        R = [R]
    if not hasattr(res,'__iter__'):
        res = [res]

    print 'Solution:'
    for r in R:
        print r

    print 'Answer:'
    for r in res:
        print r

    print '\n************************************************\n'