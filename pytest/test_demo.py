from sympy import *
from time import sleep

x = Symbol('x')
y = Symbol('y')
z = Symbol('z')

"""
def test_1(s):
    assert s(solve, '-x**2+x+2>0', 'And(x < 2, x > -1)')
def test_2(s):
    assert s(solve, 'x**2+2*x-48<0', 'And(x < 6, x > -8)')
def test_3(s):
    assert s(solve, '0.01*x**2<=1', 'And(x <= 10, x >= -10)')
def test_4(s):
    assert s(solve, '4*x <= -x**2', 'And(x <= 0, x >= -4)')
def test_5(s):
    assert s(solve, '-0.3*x < 0.6*x**2', 'Or(And(-oo < x, x < -0.5), And(x < oo, x > 0))')
def test_6(s):
    assert s(solve, '(x-14)*(x+10)<0', 'And(x<14, x>-10)')
def test_7(s):
    assert s(solve, '(x+0.1)*(x+6.3)>=0', 'Or(And(-oo<x, x<=-6.3), And(x<oo, x>=-0.1))')
def test_8(s):
    assert s(solve, '(x-12)*(x-5)*(x-2)>0', 'Or(And(x<5, x>2), And(x<oo, x>12))')
def test_9(s):
    assert s(solve, '(-4*x-3.6)*(x-3.2)<0', 'Or(And(-oo<x, x<-0.9), And(x<oo, x>3.2))')
def test_10(s):
    assert s(solve, '(x-21)/(x+7)<0', 'And(x<21, x>-7)')
"""
def test_11(s):
    #assert s(solve, '3**(-x+6)-3**(3*x-2)', '[2]')
    assert s(solve, '(1 / 5) ** (1 - x) - (1 / 5) ** x - 4.96', [2])

#def test_timeout(s):
#    s(sleep, 10, None)
