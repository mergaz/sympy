from nebularmacro import macros, sympylize, parallelize_asserts

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


@parallelize_asserts
def test_solve_9():
    assert solve(x ** 3 - 5 * x ** 2 + 8 * x - 6) == [3]
    assert solve(5 * x ** 5 == -160) == [-2]
    assert solve(2 ** (2 * x + 1) == 32) == [2]
    assert solve((1 / 9) ** (2 * x - 5) == 3 ** (5 * x - 8)) == [2]
    assert solve(root(2, 3) ** x - 1 == 2 / (root(2, 3) ** (2 * x))) == [S(-1) / 3]  # error in equation?
    assert solve((1 / 7) ** (3 * x + 3) == 7 ** (2 * x)) == [S(-3) / 5]
    assert solve([2 * x - 3 * y - 1, 2 * x ** 2 - x * y - 3 * y ** 2 - 3]) == [{x: 2, y: 1}]
    assert solve([x * y - 10, 1 / x - 1 / y + 3 / 10]) == [{x: -2, y: -5}, {x: 5, y: 2}]
    assert solve([x ** 2 - y ** 2 - 12, x ** 2 + y ** 2 - 20]) == \
           [{x: -4, y: -2}, {x: -4, y: 2}, {x: 4, y: -2}, {x: 4, y: 2}]
    assert solve([x * y ** 2 + x * y ** 3 - 10, x + x * y - 10]) == [{x: 5, y: 1}]
    assert solve([x ** 3 + 27 * y ** 3 - 54, x ** 2 - 6 * x * y + 9 * y ** 2]) == [{x: 3, y: 1}]
    assert solve([x - y - 5, sqrt(x) + sqrt(y) - 3]) == [{x: 1, y: 4}, {x: 4, y: 1}]
    assert solve([x * z + y * z - 16, x * y + y * z - 15, x * z + x * y - 7]) == \
           [{x: 1, y: 3, z: 4}, {x: -1, y: -3, z: -4}]
    assert solve(x ** 5 - 2 * x ** 4 - 3 * x ** 3 + 6 * x ** 2 - 4 * x + 8) == [-2, 2]
    assert solve(x ** 2 - 5 * x + 6 >= 0) == Or(x <= 2, x >= 3)
    assert solve(sin(a) - cos(a) == 6 / 10) == [S(32) / 100]
    assert solve(x / (x ** 2 - 16) + (x - 1) / (x + 4) - 1) == [5]
    assert solve((2 * x + 3) / 5 + (7 * x - ((3 - x) / 2)) - (((7 * x + 11) / 3) + 1)) == [1]
    assert solve([2 * x + 6 * y - 18, 3 * x - 5 * y + 29]) == {x: -3, y: 4}
    assert solve((3 * x - 2) / (2 * x + 5) - (x + 4) / (x - 10)) == [0, 45]
    assert solve(x ** (-1 / 4) == 2) == [S(1) / 16]
    assert solve(root(x - 2, 2) == root(3 * x, 6)) == [2]
    assert solve(sqrt(x - 7) - sqrt(x + 17) == -4) == [8]
    assert solve(sqrt(2 - 2 * x) == x + 3) == [-1]
    assert solve(sqrt(5 * x + 11) > x + 3) == And(-2 < x, x < 1)
    assert solve(6 - sqrt(x + 3)) == [33]
    assert solve(sqrt((x - 1) ** 2) - 1) == [0, 2]
    assert solve(sqrt(x + 3) + 5 - 7 * x) == [1]


@parallelize_asserts
def test_solve_10():
    assert solve([x ** 2 - 1 >= 0, x > 2]) == (x > 2)
    assert solve(0.5 ** x > 0.25) == (x < 2)
    assert solve(sqrt(x + 3) == sqrt(5 - x)) == [1]
    assert solve(cos(x) - 1) == [3 * k * pi]
