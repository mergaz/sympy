from sympy import solve, simplify, sympify
from sympy import Symbol, sin, cot, pi, E, Abs, tan, S, Rational, log, Eq, sqrt, cos, ln, asin, acos, acot, atan, root, \
    And, oo, Or, Derivative, exp, dsolve, Dummy, limit, Integral, integrate
try:
    from sympy.derivative.manualderivative import derivative
except ImportError:
    from sympy import diff as derivative

x = Symbol("x", real=True)
y = Symbol("y")
z = Symbol("z")
a = Symbol("a")
b = Symbol("b")
t = Symbol("t")
k = Dummy('k')
n = Dummy('n')

def diff_(expr):
    """this is a workaround to make dsolve output pickleable"""
    return derivative(expr, x)

#def test_basecamp():
def test_28(s):
    assert s(solve, '(2 ** (3 * log(x, 10))) * (5 ** log(x, 10)) - 1600',  [100])
def test_29(s):
    assert s(solve, '(2 ** (log(x ** 2, 3))) * (5 ** (log(x, 3))) - 400',  [9])
def test_30(s):
    assert s(solve, '2 / (3 ** x - 1) <= 7 / (9 ** x - 2)',  Or(And(-log(2) / log(3) <= x, x < 0), And(log(2) / (2 * log(3)) < x, x <= 1)))
def test_31(s):
    assert s(solve, 'log(log(x ** 2, 2), 1 / 3) > 0',  Or(And(-sqrt(2) < x, x < -1), And(1 < x, x < sqrt(2))))
def test_32(s):
    assert s(solve, 'log((3 * x - 2) / (x ** 2 + 1), 5) > 0',  And(2 / 3 < x, x < oo))
def test_33(s):
    assert s(solve, '4 * log(x, 4) - 33 * log(4, x) <= 1',  Or(And(0 < x, x <= 4 ** ((1 - sqrt(265)) / 8)), And(1 < x, x <= 4 ** ((1 + sqrt(265)) / 8))))
def test_34(s):
    assert s(solve, 'root((81 - x), 3) < 3',  '???')
def test_35(s):
    assert s(solve, 'root((69 - 5 * x), 3) < 5',  '???')
def test_36(s):
    assert s(solve, 'root((x ** 2 - 9), 5) < 2',  '???')
def test_37(s):
    assert s(solve, 'sqrt((x + 1) ** 2) - x - 1',  '???')
def test_38(s):
    assert s(solve, 'x ** 4 - 2 * (x ** 3) - 11 * (x ** 2) - 4 * x - 4',  '???')
def test_39(s):
    assert s(solve, '(2 * x) / (4 * (x ** 2) + 3 * x + 8) + (3 * x) / (4 * (x ** 2) - 6 * x + 8) - 1 / 6',  '???')
def test_40(s):
    assert s(solve, '[x - 2 * y - 6, 5 * x + 2 - 1]',  '???')
def test_41(s):
    assert s(solve, '[7 * x - 2 * y - 5, x ** 2 - y ** 2 - (12 * (x - y))]',  '???')
def test_42(s):
    assert s(solve, '[x ** 2 - 2 * x * y - 7, x - 3 * y + 2]',  '???')
def test_43(s):
    assert s(solve, '[2 * (x ** 2) - x * y + 3 * (y ** 2) - 7 * x - 12 * y - 1, x - y - 1]',  '???')
def test_44(s):
    assert s(solve, '[x ** 2 + 2 * (y ** 2) - 208, 3 * (x ** 2) - y ** 2 - 1]',  '???')
def test_45(s):
    assert s(solve, '[(2 * x - 5) ** 2 + (3 * y - 2) ** 2 - 17, (2 * x - 5) * (3 * y - 2) - 4]',  '???')
def test_46(s):
    assert s(solve, '[x ** 4 + y ** 4 + x ** 2 + y ** 2 - 92, x * y - 3]',  '???')
def test_47(s):
    assert s(solve, '[x ** 2 + y ** 2 - 10, x ** 3 + y ** 3 - (6 * (x + y))]',  '???')
def test_48(s):
    assert s(solve, '[x ** 2 - 4 * (y ** 2) - 9, x * y + 2 * (y ** 2) - 18]',  '???')
def test_49(s):
    assert s(solve, '[(x + 2 * y) / (x - y) + (x - 2 * y) / (x + y) - 4, x ** 2 + x * y + y ** 2 - 21]',  '???')
def test_50(s):
    assert s(solve, 'root((x + 1) / x, 3) > -1',  '???')
def test_51(s):
    assert s(solve, 'sqrt(7 - 2 * x) > x - 2',  '???')
def test_52(s):
    assert s(solve, 'sin(t) + sin(3 * t) - (2 * sin(2 * t) * cos(t))',  '???')
def test_53(s):
    assert s(solve, 'cos(5 * t) * cos(2 * t) - cos(7 * t) * cos(4 * t)',  '???')
def test_54(s):
    assert s(solve, 'sin(t) > 0',  '???')
def test_55(s):
    assert s(solve, 'log(5, x) > log(6, x)',  '???')
def test_56(s):
    assert s(solve, '(1 / 4) ** x < 1 / 16',  '???')
def test_57(s):
    assert s(solve, 'log(1 / 2) * (4 * x - 14) <= -1',  '???')
def test_58(s):
    assert s(solve, 'x ** (sqrt(x)) - x ** (x / 2)',  '???')
def test_59(s):
    assert s(solve, 'root(2 * x - 1, 3) + root(x - 1, 3) - 1',  [1])
def test_60(s):
    assert s(simplify, sin(3 / 2 * pi), -1)
def test_61(s):
    assert s(diff_, root(x, 4), 1 / (4 * x ** (3 / 4)))
def test_62(s):
    assert s(diff_, x ** 3, 3 * x ** 2)
def test_63(s):
    assert s(diff_, 1 / (cos(x) ** 2), 2 * sin(x) / cos(x) ** 3)
def test_64(s):
    assert s(diff_, x ** 4 / (1 + x ** 2), 0)
def test_65(s):
    assert s(diff_, 1 / sqrt(25 - x ** 2), 0)
def test_66(s):
    assert s(limit, (1 / (4 + log(x))), x, 0, 0)
def test_67(s):
    assert s(diff_, exp(-3 * x), -3 * exp(-3 * x))
def test_68(s):
    assert s(diff_, (-9 * x), -9)
def test_69(s):
    assert s(diff_, 3 * (x - 4), 3)
