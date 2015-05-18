from nebularmacro import macros, asdf
from sympy import S

def omicron():
    return asdf[1-1.0/3]

# from sympy import solve, simplify
# from sympy import Symbol, sin, cot, pi, E, Abs, tan, S, Rational, log, Eq, sqrt, cos, ln, asin, acos, acot, atan, root, \
#     And, oo, Or, Derivative, exp, dsolve, Dummy, limit, diff, Integral, integrate
#
# x = Symbol("x", real=True)
# y = Symbol("y")
# z = Symbol("z")
# a = Symbol("a")
# b = Symbol("b")
# k = Dummy('k')
# n = Dummy('n')
#
# def test_solve_10():
#     expect[solve([(x ** 2) - 1 >= 0, x > 2]) == x > 2]
#     expect[solve((S(1) / 2) ** x > S(1) / 4) == x < 2]
#     expect[solve(Eq(sqrt(x + 3), sqrt(5 - x))) == [S(1)]]
#     expect[solve(cos(x) - 1) == [2 * k * pi]]
#
#
# def solve_10():
#     def expect0():
#         actual = solve([(x ** 2) - 1 >= 0, x > 2])
#         expected = x > 2
#         assert actual == expected, actual
#
#     yield expect0
#
#     def expect1():
#         actual = solve((S(1) / 2) ** x > S(1) / 4)
#         expected = x < 2
#         assert actual == expected, actual
#
#     yield expect1
#
#     def expect2():
#         actual = solve(Eq(sqrt(x + 3), sqrt(5 - x)))
#         expected = [S(1)]
#         assert actual == expected, actual
#
#     yield expect2
#
#     def expect3():
#         actual = solve(cos(x) - 1)
#         expected = [2 * k * pi]
#         assert actual == expected, actual
#
#     yield expect3
