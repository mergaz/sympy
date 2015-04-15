from sympy import solve, simplify
from sympy import Symbol, sin, cot, pi, E, Abs, tan, S, Rational, log, Eq, sqrt, cos, ln, asin, acos, acot, atan, root, \
    And, oo, Or, Derivative, exp, dsolve, Dummy, limit, diff, Integral, integrate
# from nebularengine import add_expectation

x = Symbol("x", real=True)
y = Symbol("y")
z = Symbol("z")
a = Symbol("a")
b = Symbol("b")
k = Dummy('k')
n = Dummy('n')


def solve_10():
    assert solve([(x ** 2) - 1 >= 0, x > 2]) == x > 2
    assert solve((S(1) / 2) ** x > S(1) / 4) == x < 2
    assert solve(Eq(sqrt(x + 3), sqrt(5 - x))) == [S(1)]
    assert solve(cos(x) - 1) == [2 * k * pi]


def test_solve_10():
    def expect0():
        actual = solve([(x ** 2) - 1 >= 0, x > 2])
        expected = x > 2
        assert actual == expected, actual

    add_expectation(expect0)

    def expect1():
        actual = solve((S(1) / 2) ** x > S(1) / 4)
        expected = x < 2
        assert actual == expected, actual

    add_expectation(expect1)

    def expect2():
        actual = solve(Eq(sqrt(x + 3), sqrt(5 - x)))
        expected = [S(1)]
        assert actual == expected, actual

    add_expectation(expect2)

    def expect3():
        actual = solve(cos(x) - 1)
        expected = [2 * k * pi]
        assert actual == expected, actual

    add_expectation(expect3)
