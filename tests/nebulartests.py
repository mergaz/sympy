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
def stest_solve_9():
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
def stest_basecamp():
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


@parallelize_asserts
def stest_logsolve():
    assert simplify(log(125, 3) - 3) == 125
    assert simplify(log(27, (sqrt(1 / 3))) + 6) == 27
    assert simplify(log(0.008, 0.2) - 3) == 0.008
    assert simplify(1.7 ** log(2, 1.7)) == 2
    assert solve(log(x, 1 / 6) + 3) == [216]
    assert solve(log(1 / 4, x) + 2) == [2]
    assert solve(log(1 / 9, x) + 1) == [9]
    assert solve(log(1 / 9, x) + 1 / 3) == [729]
    assert solve(log(x, 3 / 10) - 2 * log(6, 3 / 10) + log(12, 3 / 10)) == [3]
    assert solve(log((2 * x - 4), 1 / 3) + 2) == [65 / 10]
    assert solve(log(x, 3) > 2) == And(9 < x, x < oo)
    assert solve(log((12 - 2 * x - x ** 2), 3) > 2) == And(-3 < x, x < 1)
    assert solve(log(x + 1, pi) + log(x, pi) < log(2, pi)) == And(0 < x, x < 1)
    assert solve(log(x, 10) ** 2 + 2 * log(x, 10) < 3) == Or(And(0 < x, x < 1), And(10 < x, x < oo))
    assert solve(4 ** x - 2 ** x <= 2) == And(-oo < x, x <= 1)
    assert solve(log(x, a) - log(3, a) - log(5, a), x) == [15]
    assert solve(log(x, a) - log(2, sqrt(a)) + log(3, 1 / a), x) == [4 / 3]
    assert solve(log(x, 10) ** 2 - 1) == [10, 1 / 100]
    assert solve(log(x + 1, 2) ** 2 - log(x + 1, 1 / 4) - 5) == [25, 1 / 5]
    assert solve(x ** log(x, 10) - 10000) == [1 / 100, 100]
    assert solve(x ** log(x, 5) - 125 * (x ** 2)) == [0]
    assert solve(x ** log(x - 2, 2) - 8) == [8, 1 / 2]
    assert solve(1 / (log(x, 10) - 6) + 5 / (log(x, 10) + 2) - 1) == [100, 10 ** 8]
    assert solve(log(x, 2) + 4 / log(2, x) - 5) == [2]
    assert solve(2 * log(x, sqrt(3)) + log(1 / 3, x) - 3) == [0]
    assert solve(log(1 / 8, x) + 3) == [2]
    assert solve(log(9, x) - 1 / 2) == [81]
    assert solve(log(x, 7) + 1) == [1 / 7]
    assert solve(log(x, 3 / 10) - 2) == [9 / 100]
    assert solve(log(x, 6) >= 2) == And(36 <= x, x < oo)
    assert solve(log(x, 9) <= 1 / 2) == And(-oo < x, x <= 3)
    assert solve(log(x, 1 / 3) < -4) == And(81 < x, x < oo)
    assert solve(log(x, 2 / 10) > -3) == And(-oo < x, x < 125)
    assert solve(log(x, 1 / 3) - log(7, 1 / 3) - log(4, 1 / 3)) == [28]
    assert solve(log(x, 1 / 4) - log(9, 1 / 4) - log(5, 1 / 4)) == [45]
    assert solve(log(3, 1 / 2) + log(x, 1 / 2) - log(12, 1 / 2)) == [45]
    assert solve(log(8, 1 / 3) + log(x, 1 / 3) - log(4, 1 / 3)) == [1 / 2]
    assert solve(log(x / 2, sqrt(3)) - log(6, sqrt(3)) - log(2, sqrt(3))) == [24]
    assert solve(log(x / 3, sqrt(2)) - log(15, sqrt(2)) + log(6, sqrt(3))) == [15 / 2]
    assert solve(3 * log(1 / 2, 2) - log(1 / 32, 2) - log(x, 2)) == [45]
    assert solve(log(x ** 2 - 5 * x + 8, 34 / 10) - log(x, 34 / 10)) == [4, 2]
    assert solve(log(x / 3, 1 / 2) >= -2) == And(0 > x, x < 5 / 4)
    assert solve(log(5 * x - 9, 1 / 3) >= log(4 * x, 1 / 3)) == And(9 / 5 < x, x <= 9)
    assert solve(log(-x, 1 / 3) > log(4 - 2 * x, 1 / 3)) == And(-oo < x, x < 0)
    assert solve(log(x, 2) ** 2 > 4 * log(x, 2) - 3) == Or(And(0 < x, x < 2), And(8 < x, x < oo))
    assert solve(2 * log(x, 3 / 10) ** 2 - 7 * log(x, 3 / 10) - 4 <= 0) == And(-1 / 2 <= x, x <= 4)
    assert solve(log(x ** 2, 1 / 3) ** 2 - 7 * log(x, 1 / 3) + 3 <= 0) == \
           And(1 / 3 <= x, x <= 1 / root(27, 4))
    assert solve(3 * log(x, 1 / 3) < log(9, 1 / 3) + log(3, 1 / 3)) == And(3 < x, x < oo)
    assert solve(log(x, 1 / 2) + log(10 - x, 1 / 2) >= -1 + log(9 / 2, 1 / 2)) == \
           Or(And(0 < x, x <= 1), And(9 <= x, x < 10))
    assert solve(log(7 - x, 4 / 10) >= log(3 * x + 6, 4 / 10)) == Or(x >= 1 / 4, Eq(x, 6))


@parallelize_asserts
def stest_absolve():
    assert solve(abs(2 * x - 5) - abs(7 - 2 * x)) == [3]
    assert solve(abs(x - 2) - 2 * abs(3 - x)) == [2 + 2 / 3, 4]
    assert solve(x ** 2 + abs(x) - 2) == '???'
    assert solve(x ** 2 - 3 * abs(x) + 2) == [-1, 1, -2, 2]
    assert solve(abs(3 * x - 25 / 10) >= 2) == Or(And(-oo < x, x <= 1 / 6), And(3 / 2 <= x, x < oo))
    assert solve(abs(5 - 2 * x) < 1) == And(2 < x, x < 3)
    assert solve(x ** 2 - 4 * abs(x) + 3 > 0) == Or(And(-oo < x, x < -3), And(-1 < x, x < 1))
    assert solve(2 * (x ** 2) - 5 * abs(x) + 3 >= 0) == \
           Or(And(-oo < x, x <= -3 / 2), And(-1 <= x, x <= 1), And(3 / 2 <= x, x < oo))
    assert solve(abs(x) - 5) == '???'
    assert solve(abs(x) < 5) == And(-5 < x, x < 5)
    assert solve(abs(x) >= 5) == '???'
    assert solve(abs(x - 10) - 4) == [6]
    assert solve(abs(x - 10) <= 4) == '???'
    assert solve(abs(x - 10) > 4) == Or(And(-oo < x, x < 6), And(14 < x, x < oo))  # -oo < x < 6 or 14 < x < oo
    assert solve(abs(x - 3) < 1) == '???'
    assert solve([abs(x) < 1, abs(y) < 1]) == '???'
    assert solve([abs(x) > 1, abs(y) > 1]) == '???'
    assert solve([abs(x - 2) <= 1, abs(y + 3) <= 1]) == '???'
    assert solve(abs(x + y) + abs(x - y) - 4) == '???'
    assert solve(sqrt(x + y) >= abs(x)) == '???'
    assert solve(abs(sin(x)) + abs(cos(x)) >= 1) == And(-oo < x, x < oo)
    assert solve(abs(x - sqrt(3))) == '???'
    assert solve(abs(x) - 2 / 10) == '???'
    assert solve(abs(x + 7)) == '???'
    assert solve(abs(x) - 1) == '???'
    assert solve(abs(x - 1) - 2) == '???'
    assert solve(abs(x - 1 + 5 / 6) - 2) == '???'
    assert solve(abs(x - 11) - 9) == '???'
    assert solve(abs(x + 3 / 4) - 3 - 3 / 4) == '???'
    assert solve(abs(2 * x - 1) - 3) == '???'
    assert solve(abs(1 + 3 * x) - 2) == '???'
    assert solve(abs(2 + 2 * x) - 6) == '???'
    assert solve(abs(4 * x + 1) - 5) == '???'
    assert solve(abs(1 / 5 * x - 2) - 36 / 10) == [-8, 28]
    assert solve(abs(3 - 3 / 2 * x) - 25 / 10) == [1 / 3, 3 + 2 / 3]
    assert solve(abs(2 - 7 / 2 * x) - 62 / 10) == [-12 / 10, 2 + 12 / 35]
    assert solve(abs(2 / 5 * x + 1) - 23 / 10) == [8 + 1 / 4, 3 + 1 / 4]
    assert solve([y - abs(x), y - 1 / 2 * x - 3]) == '???'
    assert solve([y + abs(x), y - 1 / 3 * x + 4]) == '???'
    assert solve([y - 3 * abs(x), y - x ** 2]) == '???'
    assert solve(abs(x) >= 3) == And(-3 <= x, x <= 3)
    assert solve(x ** 2 > abs(x)) == And(1 > x, x > -1)
    assert solve(-abs(x) < 4) == And(-oo < x, x < oo)
    assert solve(sqrt(x) >= abs(x)) == And(0 <= x, x <= 1)
    assert solve(abs(x) <= -x + 4) == And(-oo < x, x <= 2)
    assert solve(abs(x) > x - 2) == And(-oo < x, x < oo)
    assert solve(abs(x) > -x + 4) == And(x > 2, x < oo)
    assert solve(-abs(x) > 3 - x) == [0]
    assert solve(1 / (sqrt(abs(x) ** 3))) == And(-oo < x, x < 0)


@parallelize_asserts
def test_varsolve():
    assert solve(2 + x - x ** 2 > 0) == And(-1 < x, x < 2)
    assert solve(3 / 10 * (x ** 2) + x + 3 / 10 <= 0) == And(-3 <= x, x <= -1 / 3)
    assert solve(3 * (x ** 2) - 2 * x - 1 <= 0) == And(-1 / 3 <= x, x <= 1)
    assert solve(6 * (x ** 2) + x - 2 <= 0) == [0]
    assert solve(x ** 2 - 2 * x + 1 <= 0) == [1]
    assert solve(-1 / 4 * (x ** 2) - 2 * x + 5 > 0) == [0]
    assert solve(4 * (x ** 2) + 4 * x + 1 > 0) == Or(And(-oo < x, x < -1 / 2), And(-1 / 2 < x, x < oo))
    assert solve(3 * (x ** 2) + 7 * x - 7 > 0) == [0]
    assert solve(9 * (x ** 4) - 10 * (x ** 2) + 1 <= 0) == Or(And(-1 <= x, x <= -1 / 3), And(1 / 3 < x, x < 1))
    assert solve(4 * (x ** 4) + 10 * (x ** 2) - 66 >= 0) == [0]
    assert solve(x ** 3 < 5) == And(-oo < x, x < root(5, 3))
    assert solve(x ** 7 >= 11) == And(root(11, 7) <= x, x < oo)
    assert solve(3 ** (6 - x) - 3 ** (3 * x - 2)) == [2]
    assert solve(3 ** (x ** 2 - x - 2) - 81) == [-2, 3]
    assert solve(7 ** (x + 2) + 4 * (7 ** (x - 1)) - 347) == [1]
    assert solve((1 / 5) ** (1 - x) - (1 / 5) ** x - 496 / 100) == [2]
    assert solve(x / (x - 2) - 8 / (x + 5) - 14 / (x ** 2 + 3 * x - 10)) == [1]
    assert solve(y / (2 * y - 3) + 1 / (y + 7) + 17 / (2 * (y ** 2) + 11 * y - 21)) == [-2]
    assert solve(x ** 3 + 5 * x - 6) == [1]
    assert solve(13 * (5 * x - 1) - 15 * (4 * x + 2) < 0) == And(-oo < x, x < 86 / 10)
    assert solve(6 * (7 - 1 / 5 * x) - 5 * (8 - 2 / 5 * x) > 0) == And(oo > x, x > -5 / 2)
    assert solve(x ** 2 + 2 * x - 48 < 0) == And(-8 < x, x < 6)
    assert solve(-x ** 2 + 2 * x + 15 < 0) == Or(And(-oo < x, x < 3 / 2), And(2 < x, x < oo))
    assert solve(4 * (x ** 2) - 12 * x + 9 > 0) == Or(And(-oo < x, x < 3 / 2), And(3 / 2 < x, x < oo))
    assert solve(2 * (x ** 2) + 13 * x - 7 > 0) == Or(And(-oo < x, x < -7), And(1 / 2 < x, x < oo))
    assert solve(6 * (x ** 2) - 13 * x + 5 <= 0) == And(1 / 2 <= x, x <= 1 + 2 / 3)
    assert solve(3 * (x ** 2) - 2 * x > 0) == Or(And(-oo < x, x < 0), And(2 / 3 < x, x < oo))
    assert solve(1 / 5 * (x ** 2) > 18 / 10) == Or(And(-oo < x, x < -3), And(3 < x, x < oo))
    assert solve(7 * x < x ** 2) == Or(And(-oo < x, x < 0), And(7 < x, x < oo))
    assert solve(1 / 100 * (x ** 2) <= 1) == And(-10 <= x, x <= 10)
    assert solve(4 * x <= -x ** 2) == And(-4 <= x, x <= 0)
    assert solve(-3 / 10 * x < 3 / 5 * (x ** 2)) == Or(And(-oo < x, x < -1 / 2), And(0 < x, x < oo))
    assert solve(3 * (x ** 2) + 40 * x + 10 < -x ** 2 + 11 * x + 3) == And(-7 <= x, x <= -1 / 4)
    assert solve(2 * (x ** 2) + 8 * x - 111 < (3 * x - 5) * (2 * x + 6)) == [0]
    assert solve(2 * x * (3 * x - 1) > 4 * (x ** 2) + 5 * x + 9) == Or(And(-oo < x, x < -1), And(9 / 2 < x, x < oo))
    assert solve((5 * x + 7) * (x - 2) < 21 * (x ** 2) - 11 * x - 13) == [0]
    assert solve((x - 14) * (x + 10) < 0) == And(-10 < x, x < 14)
    assert solve((x + 1 / 10) * (x + 63 / 10) >= 0) == \
           Or(And(-oo < x, x <= -63 / 10), And(-1 / 10 <= x, x < oo))
    assert solve((x - 2) * (x - 5) * (x - 12) > 0) == Or(And(2 < x, x < 5), And(12 < x, x < oo))
    assert solve(-4 * (x + 9 / 10) * (x - 32 / 10) < 0) == \
           Or(And(-oo < x, x < -9 / 10), And(32 / 10 < x, x < oo))
    assert solve((14 / 10 - x) / (x + 38 / 10) < 0) ==\
           Or(And(-oo < x, x < -38 / 10), And(14 / 10 < x, x < oo))
    assert solve((5 * x - 3 / 2) / (x - 4) > 0) == Or(And(-oo < x, x < 3 / 10), And(4 < x, x < oo))
    assert solve((x - 21) / (x + 7) < 0) == And(-7 < x, x < 21)
    assert solve((x + 47 / 10) / (x - 72 / 10) > 0) ==\
           Or(And(-oo < x, x < -47 / 10), And(72 / 10 < x, x < oo))
    assert solve(tan(-x / 2) < 1) == And(-pi / 2 + 2 * pi * k < x, x < pi + 2 * pi * k)
    assert solve(sin((3 * pi) / 2 - x) < sqrt(3) / 2) ==\
           And(-(5 * pi) / 6 + 2 * pi * k < x, x < (5 * pi) / 6 + 2 * pi * k)
    assert solve(sin(x) * cos(pi / 3) + sin(pi / 3) * cos(x) <= 1 / 2) == \
           And(-(3 * pi) / 2 + 2 * pi * k <= x, x <= (-pi) / 6 + 2 * pi * k)
    assert solve(sin(pi / 6) * cos(x) + cos(pi / 6) * sin(x) <= 1) == And(-oo < x, x < oo)
    assert solve(1 - cos(x) - 2 * sin(x / 2)) == [2 * pi * k, pi + 4 * pi * k]
    assert solve(2 / (3 * sqrt(2) * sin(x) - 1) - 1) == [((-1) ** k) * (pi / 4) + pi * k]
    assert solve(4 / (sqrt(3) * tan(x) + 5) - 1 / 2) == [pi / 3 + pi * k]
    assert solve(sqrt(13 - x ** 2) - 3) == [-2, 2]
    assert solve(x - sqrt(x + 1) - 5) == [8]
    assert solve(sqrt(x) + x ** 2 - 18) == [4]
