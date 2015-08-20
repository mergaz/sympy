from sympy import *
from time import sleep

x = Symbol('x')
y = Symbol('y')
z = Symbol('z')

def test_one(s):
    assert s(solve, x**2+2*x-2, [-1 + sqrt(3), -1 - sqrt(3)])

def test_two(s):
    assert s('solve', 'x**2+2*x-2', '[-1 + sqrt(3), -1 - sqrt(3)]')

def test_timeout(s):
    s(sleep, 10, None)
