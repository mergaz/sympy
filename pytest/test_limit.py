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

h = Symbol('h')
n = Symbol('n')

#def test_limit():
def test_374(s):
    assert s(limit, 1 + (1 / (7 ** n)), n, oo, 1)
def test_375(s):
    assert s(limit, (3 - (2 ** n)) / (2 ** n), n, oo, -1)
def test_376(s):
    assert s(limit, 3 / (2 ** n) - 1, n, oo, -1)
def test_377(s):
    assert s(limit, 1 / (4 ** n), n, oo, 0)
def test_378(s):
    assert s(limit, 0.2 ** n, n, oo, 0)
def test_379(s):
    assert s(limit, 0.6 ** n - 2, n, oo, -2)
def test_380(s):
    assert s(limit, 1 - (1 / (2 ** n)), n, oo, 1)
def test_381(s):
    assert s(limit, (-1.3) ** n, n, oo, 0)
def test_382(s):
    assert s(limit, (3 ** (n + 2) + 2) / (3 ** n), n, oo, 9)
def test_383(s):
    assert s(limit, ((9 * (3 ** n) + 2) / (3 ** n)), n, oo, 9)
def test_384(s):
    assert s(limit, 9 + (2 / (3 ** n)), n, oo, 9)
def test_385(s):
    assert s(limit, (((5 ** n) + 1) ** 2) / (5 ** (2 * n)), n, oo, 1)
def test_386(s):
    assert s(limit, (5 ** (2 * n) + 1 + 2 * (5 ** n)) / (5 ** (2 * n)), n, oo, 1)
def test_387(s):
    assert s(limit, 1 + (1 / (5 ** (2 * n)) + (2 / (5 ** n))), n, oo, 1)
def test_388(s):
    assert s(limit, (6 - 7 / (n ** 2) - 3 / n - 3 / (sqrt(n))), n, oo, 6)
def test_389(s):
    assert s(limit, (1 / n) + 3 / (sqrt(n)) - 4 + 7 / (n ** 2), n, oo, -4)
def test_390(s):
    assert s(limit, (5 * n + 3) / (n + 1), n, oo, 5)
def test_391(s):
    assert s(limit, ((2 * n + 1) / (3 * n - 1)), n, oo, 2 / 3)
def test_392(s):
    assert s(limit, (0.5 * 5 ** (-n)), n, oo, 0)
def test_393(s):
    assert s(limit, (2 * (n ** 2) - 1) / (n ** 2), n, oo, 2)
def test_394(s):
    assert s(limit, (3 - (n ** 2)) / (n ** 2), n, oo, -1)
def test_395(s):
    assert s(limit, (2 * n + 1) * (n - 3) / (n ** 2), n, oo, 2)
def test_396(s):
    assert s(limit, ((3 * n - 2) * (2 * n + 3)) / (n ** 2), n, oo, 6)
def test_397(s):
    assert s(limit, (n ** 2 * (2 * n + 5) - 2 * n ** 3 + 5 * n ** 2 - 13) / (n * (n + 1) * (n - 7) + 1 - n), n, oo, 0)
def test_398(s):
    assert s(limit, ((1 - n) * (n ** 2) + 1 + (n ** 3)) / ((n ** 2) + 2 * n), n, oo, 1)
def test_399(s):
    assert s(limit, 1 / (x ** 2) + 3 / (x ** 3), x, oo, 0)
def test_400(s):
    assert s(limit, (2 / (x ** 9)) + 1, x, oo, 1)
def test_401(s):
    assert s(limit, 7 / (x ** 2) - 7, x, oo, -7)
def test_402(s):
    assert s(limit, (12 - 1 / (x ** 2)) * (16 / (x ** 7)), x, oo, 0)
def test_403(s):
    assert s(limit, ((5 / (x ** 3) + 1) * ((-8) / (x ** 2) - 2)), x, oo, -2)
def test_404(s):
    assert s(limit, (6 * x + 3 * h - 5), h, 0, 6 * x - 5)
def test_405(s):
    assert s(limit, -6 * x - 3 * h, h, 0, -6 * x)
def test_406(s):
    assert s(limit, 10 * t + 5 * h, h, 0, 10 * t)
def test_407(s):
    assert s(limit, 2 * t + h, h, 0, 2 * t)
