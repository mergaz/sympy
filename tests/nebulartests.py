from nebularmacro import macros, parallelize_asserts

from sympy import solve, simplify
from sympy import Symbol, sin, cot, pi, E, Abs, tan, S, Rational, log, Eq, sqrt, cos, ln, asin, acos, acot, atan, root, \
    And, oo, Or, Derivative, exp, dsolve, Dummy, limit, diff, Integral, integrate

x = Symbol("x", real=True)
y = Symbol("y")
z = Symbol("z")
a = Symbol("a")
b = Symbol("b")
t = Symbol("t")
k = Dummy('k')
n = Dummy('n')


@parallelize_asserts
def test_solve_9():
    assert solve(x ** 3 - 5 * x ** 2 + 8 * x - 6) == [3]
    assert solve(5 * x ** 5 == -160) == [-2]
    assert solve(2 ** (2 * x + 1) == 32) == [2]
    assert solve((1 / 9) ** (2 * x - 5) == 3 ** (5 * x - 8)) == [2]
    assert solve(root(2, 3) ** x - 1 == 2 / (root(2, 3) ** (2 * x))) == [-1 / 3]  # error in equation?
    assert solve((1 / 7) ** (3 * x + 3) == 7 ** (2 * x)) == [-3 / 5]
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
    assert solve(sin(a) - cos(a) == 6 / 10) == [32 / 100]
    assert solve(x / (x ** 2 - 16) + (x - 1) / (x + 4) - 1) == [5]
    assert solve((2 * x + 3) / 5 + (7 * x - ((3 - x) / 2)) - (((7 * x + 11) / 3) + 1)) == [1]
    assert solve([2 * x + 6 * y - 18, 3 * x - 5 * y + 29]) == {x: -3, y: 4}
    assert solve((3 * x - 2) / (2 * x + 5) - (x + 4) / (x - 10)) == [0, 45]
    assert solve(x ** (-1 / 4) == 2) == [1 / 16]
    assert solve(root(x - 2, 2) == root(3 * x, 6)) == [2]
    assert solve(sqrt(x - 7) - sqrt(x + 17) == -4) == [8]
    assert solve(sqrt(2 - 2 * x) == x + 3) == [-1]
    assert solve(sqrt(5 * x + 11) > x + 3) == And(-2 < x, x < 1)
    assert solve(6 - sqrt(x + 3)) == [33]
    assert solve(sqrt((x - 1) ** 2) - 1) == [0, 2]
    assert solve(sqrt(x + 3) + 5 - 7 * x) == [1]


@parallelize_asserts
def test_basecamp():
    assert solve((2 ** (3 * log(x, 10))) * (5 ** log(x, 10)) - 1600) == [100]
    assert solve((2 ** (log(x ** 2, 3))) * (5 ** (log(x, 3))) - 400) == [9]
    assert solve(2 / (3 ** x - 1) <= 7 / (9 ** x - 2)) == Or(And(-log(2) / log(3) <= x, x < 0),
                                                             And(log(2) / (2 * log(3)) < x, x <= 1))
    assert solve(log(log(x ** 2, 2), 1 / 3) > 0) == Or(And(-sqrt(2) < x, x < -1),
                                                       And(1 < x, x < sqrt(2)))
    assert solve(log((3 * x - 2) / (x ** 2 + 1), 5) > 0) == And(2 / 3 < x, x < oo)
    assert solve(4 * log(x, 4) - 33 * log(4, x) <= 1) == Or(And(0 < x, x <= 4 ** ((1 - sqrt(265)) / 8)),
                                                            And(1 < x, x <= 4 ** ((1 + sqrt(265)) / 8)))
    assert solve(root((81 - x), 3) < 3) == '???'
    assert solve(root((69 - 5 * x), 3) < 5) == '???'
    assert solve(root((x ** 2 - 9), 5) < 2) == '???'
    assert solve(sqrt((x + 1) ** 2) - x - 1) == '???'
    assert solve(x ** 4 - 2 * (x ** 3) - 11 * (x ** 2) - 4 * x - 4) == '???'
    assert solve((2 * x) / (4 * (x ** 2) + 3 * x + 8) + (3 * x) / (4 * (x ** 2) - 6 * x + 8) - 1 / 6) == '???'
    assert solve([x - 2 * y - 6, 5 * x + 2 - 1]) == '???'
    assert solve([7 * x - 2 * y - 5, x ** 2 - y ** 2 - (12 * (x - y))]) == '???'
    assert solve([x ** 2 - 2 * x * y - 7, x - 3 * y + 2]) == '???'
    assert solve([2 * (x ** 2) - x * y + 3 * (y ** 2) - 7 * x - 12 * y - 1, x - y - 1]) == '???'
    assert solve([x ** 2 + 2 * (y ** 2) - 208, 3 * (x ** 2) - y ** 2 - 1]) == '???'
    assert solve([(2 * x - 5) ** 2 + (3 * y - 2) ** 2 - 17, (2 * x - 5) * (3 * y - 2) - 4]) == '???'
    assert solve([x ** 4 + y ** 4 + x ** 2 + y ** 2 - 92, x * y - 3]) == '???'
    assert solve([x ** 2 + y ** 2 - 10, x ** 3 + y ** 3 - (6 * (x + y))]) == '???'
    assert solve([x ** 2 - 4 * (y ** 2) - 9, x * y + 2 * (y ** 2) - 18]) == '???'
    assert solve([(x + 2 * y) / (x - y) + (x - 2 * y) / (x + y) - 4, x ** 2 + x * y + y ** 2 - 21]) == '???'
    assert solve(root((x + 1) / x, 3) > -1) == '???'
    assert solve(sqrt(7 - 2 * x) > x - 2) == '???'
    assert solve(sin(t) + sin(3 * t) - (2 * sin(2 * t) * cos(t))) == '???'
    assert solve(cos(5 * t) * cos(2 * t) - cos(7 * t) * cos(4 * t)) == '???'
    assert solve(sin(t) > 0) == '???'
    assert solve(log(5, x) > log(6, x)) == '???'
    assert solve((1 / 4) ** x < 1 / 16) == '???'
    assert solve(log(1 / 2) * (4 * x - 14) <= -1) == '???'
    assert solve(x ** (sqrt(x)) - x ** (x / 2)) == '???'
    assert solve(root(2 * x - 1, 3) + root(x - 1, 3) - 1) == [1]
    assert simplify(sin(3 / 2 * pi)) == -1
    assert diff(root(x, 4), x) == 1 / (4 * x ** (3 / 4))
    assert diff(x ** 3, x) == 3 * x ** 2
    assert diff(1 / (cos(x) ** 2), x) == 2 * sin(x) / cos(x) ** 3
    assert diff(x ** 4 / (1 + x ** 2), x) == 0
    assert diff(1 / sqrt(25 - x ** 2), x) == 0
    assert limit((1 / (4 + log(x))), x, 0) == 0
    assert diff(exp(-3 * x), x) == -3 * exp(-3 * x)
    assert diff((-9 * y), y) == -9
    assert diff(3 * (y - 4), y) == 3
