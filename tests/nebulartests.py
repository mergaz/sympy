from nebularmacro import macros, symbolize, distribute_asserts

from sympy import solve, simplify
from sympy import Symbol, sin, cot, pi, E, Abs, tan, S, Rational, log, Eq, sqrt, cos, ln, asin, acos, acot, atan, root, \
    And, oo, Or, Derivative, exp, dsolve, Dummy, limit, diff, Integral, integrate

x = Symbol("x", real=True)
y = Symbol("y")
z = Symbol("z")
a = Symbol("a")
b = Symbol("b")
k = Dummy('k')
n = Dummy('n')

u = symbolize[3 * (x ** 2) - 2 * x + (x + 0.1) * (x + 6.3) - 4/7 * (x + 0.9) * (x - 3.2)]

@distribute_asserts
def omicron():
    assert 3 * (x ** 2) != 3 * x * x
    assert 3 * (x ** 2) == 3 * x * x

@distribute_asserts
def test_solve_10():
    assert solve([x ** 2 - 1 >= 0, x > 2]) == x > 2
    assert solve(0.5 ** x > 0.25) == x < 2
    assert solve(Eq(sqrt(x + 3), sqrt(5 - x))) == [1]
    assert solve(cos(x) - 1) == [2 * k * pi]

#
# def solve_10():
#     def expect0():
#         actual = solve([(x ** 2) - 1 >= 0, x > 2])
#         expected = x > 2
#         assert actual == expected, actual
#
#     yield expect0
#
