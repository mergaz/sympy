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

#def test_integrate():
def test_453(s):
    assert s(integrate, x ** 3, (x, 2, 4), 60)
def test_454(s):
    assert s(integrate, x ** 2 + 1, (x, -2, 1), 6)
def test_455(s):
    assert s(integrate, cos(x), (x, -pi / 6, 0), 1 / 2)
def test_456(s):
    assert s(integrate, 4 - x ** 2, (x, -2, 2), 10 + 2 / 3)
def test_457(s):
    assert s(integrate, (-x) ** 2 + 4 * x - 3, (x, 1, 3), 1 + 1 / 3)
def test_458(s):
    assert s(integrate, 1 / (x ** 2), (x, 2, 3), 1 / 6)
def test_459(s):
    assert s(integrate, 1 / (sqrt(x)), (x, 4, 9), 2)
def test_460(s):
    assert s(integrate, sin(2 * x), (x, -2 * pi, pi), -1)
def test_461(s):
    assert s(integrate, 1 - 3 * (x ** 2), (x, -1, 2), -6)
def test_462(s):
    assert s(integrate, 2 * x - (3 / sqrt(x)), (x, 1, 9), 68)
def test_463(s):
    assert s(integrate, (x + 1 / x) ** 2, (x, 1, 2), 4 + 5 / 6)
def test_464(s):
    assert s(integrate, (3 * x - 1) / sqrt(x), (x, 1, 3), 4 * sqrt(3))
def test_465(s):
    assert s(integrate, (4 / (3 * x + 2)), (x, 0, 1), 4 / 3 * log(5 / 2, 10))
def test_466(s):
    assert s(integrate, (sin(2 * x + pi / 3)), (x, 0, pi / 2), 1 / 2)
def test_467(s):
    assert s(integrate, sin(x) * cos(x), (x, 0, pi / 2), 1 / 2)
def test_468(s):
    assert s(integrate, (sin(x) ** 4 + cos(x) ** 4), (x, 0, pi), 3 * pi / 4)
def test_469(s):
    assert s(integrate, (x ** 2) * sqrt(x + 1), (x, 0, 3), 3888)
def test_470(s):
    assert s(integrate, b - 4 * x, (x, 1, b), b - 2)
def test_471(s):
    assert s(integrate, (x + 1) ** 2, (x, -1, 0), 0)
def test_472(s):
    assert s(integrate, x - 1, (x, 0, 1), 5 / 6)
def test_473(s):
    assert s(integrate, 1 / (x ** 3), (x, -1, 1), 3 / 8)
def test_474(s):
    assert s(integrate, cos(x), (x, -pi / 2, pi / 2), 2)
def test_475(s):
    assert s(integrate, (x + 2) ** 2, (x, -2, 1 / 2), 0)
def test_476(s):
    assert s(integrate, (x - 3) ** 2, (x, 1 / 2, 3), 10 + 5 / 12)
def test_477(s):
    assert s(integrate, 2 * sqrt(2 * x), (x, 0, 2), 0)
def test_478(s):
    assert s(integrate, x ** 2, (x, 0, 2), 8 / 3)
def test_479(s):
    assert s(integrate, x ** 2 - 2 * x + 2, (x, 0, 1), 0)
def test_480(s):
    assert s(integrate, -2 * x + 2, (x, 0, 1), 1 / 3)
def test_481(s):
    assert s(integrate, x ** 4 - 2 * (x ** 2) + 5, (x, 0, 1), 0)
def test_482(s):
    assert s(integrate, 1, (x, 0, 1), 3 + 8 / 15)
def test_483(s):
    assert s(integrate, (1 / 2) * cos(x + pi / 4), (x, 0, pi / 4), (2 - sqrt(2)) / 4)
def test_484(s):
    assert s(integrate, (1 / 3) * sin(x - pi / 3), (x, 0, pi / 3), -1 / 6)
def test_485(s):
    assert s(integrate, 3 * sin(3 * x - 6), (x, 1, 3), 0)
def test_486(s):
    assert s(integrate, 8 * cos(4 * x - 12), (x, 0, 3), 2 * sin(12))
def test_487(s):
    assert s(integrate, sqrt(x) * (3 - 7 / x), (x, 1, 4), 0)
def test_488(s):
    assert s(integrate, sqrt(2 * x - 3), (x, 2, 6), 8 + 2 / 3)
