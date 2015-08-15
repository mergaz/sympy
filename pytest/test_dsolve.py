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

C1 = Symbol('C1')
C2 = Symbol('C2')
C3 = Symbol('C3')
C4 = Symbol('C4')

def dsolve_(expr):
    """this is a workaround to make dsolve output pickleable"""
    return dsolve(expr, y(x)).subs(y(x), y)

#def test_dsolve():
def test_367():
    dsolve_(Derivative(y(x), x) - 3 * y(x) * x) == (y == C1 * exp(3 * x ** 2 / 2))  # separable
def test_368():
    dsolve_(y(x).diff(x, 4) + 2 * y(x).diff(x, 3) - 2 * y(x).diff(x, 2) - 6 * y(x).diff(x) + 5 * y(x)) == \
           (y == (C1 + C2 * x) * exp(x) + (C3 * sin(x) + C4 * cos(x)) * exp(-2 * x))
def test_369():
    dsolve_(y(x).diff(x) - y(x) - y(x) ** 2 * exp(x)) == (y == exp(x) / (C1 - exp(2 * x) / 2))  # Bernoulli eq
def test_370():
    dsolve_(y(x).diff(x, 2) * x ** 2 - 4 * y(x).diff(x) * x + 6 * y(x)) == (y == x ** 2 * (C1 + C2 * x))
def test_371():
    dsolve_(cos(y(x)) - (x * sin(y(x)) - y(x) ** 2) * y(x).diff(x)) == \
           (x * cos(y) + y ** 3 / 3 == C1)  # exact
def test_372():
    dsolve_(y(x).diff(x, 2) + 2 * y(x).diff(x) + y(x) - 4 * exp(-x) * x ** 2 + cos(2 * x)) == \
           (y == (C1 + C2 * x + x ** 4 / 3) * exp(-x) - 4 * sin(2 * x) / 25 + 3 * cos(2 * x) / 25)
def test_373():
    dsolve_(y(x).diff(x, 3) - 3 * y(x).diff(x, 2) + 3 * y(x).diff(x) - y(x) - exp(x) * log(x)) == \
           (y == (C1 + C2 * x + C3 * x ** 2 + x ** 3 * (6 * log(x) - 11) / 36) * exp(x))

