from nebularmacro import macros, symbolize, parallelize_asserts
from macropy.case_classes import macros, case

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


@case
class EvaluationFailure(exception): pass
@case
class ComparisonFailure(actual, exception): pass
@case
class Success(actual): pass

@parallelize_asserts
def omicron():
    assert 3 * x ** 2 != 3 * x * x
    assert 3 * (x ** 2) == 3 * x * x


@parallelize_asserts
def test_solve_10():
    assert solve([x ** 2 - 1 >= 0, x > 2]) == (x > 2)
    assert solve(0.5 ** x > 0.25) == (x < 2)
    assert solve(Eq(sqrt(x + 3), sqrt(5 - x))) == [1]
    assert solve(cos(x) - 1) == [3 * k * pi]

#
# def solve_10():
#     def expect0():
#         actual = solve([(x ** 2) - 1 >= 0, x > 2])
#         expected = x > 2
#         assert actual == expected, actual
#
#     yield expect0
#
