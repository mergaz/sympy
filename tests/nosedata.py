from functools import partial
from sympy import Symbol, sin, cot, pi, E, Abs, tan, S, Rational, log, Eq, sqrt, cos, ln, asin, acos, acot, atan, root, \
    rad, deg, And, oo, Or, I, Derivative, exp, dsolve


x = Symbol("x", real=True)
y = Symbol("y")
z = Symbol("z")
a = Symbol("a")
b = Symbol("b")

solve_generic = [
    # sys
    ([x ** 2 + x * y + y ** 2 - 4, x + x * y + y - 2], [{x: 0, y: 2}, {x: 2, y: 0}]),
    ([(x + 1) * (y + 1) - 10, (x + y) * (x * y + 1) - 25], [{x: 1, y: 4}, {x: 4, y: 1}]),
    ([x + y - 1, x ** 4 + y ** 4 - 7], [{x: (1 + sqrt(5)) / 2, y: (1 - sqrt(5)) / 2},
                                        {x: (1 - sqrt(5)) / 2, y: (1 + sqrt(5)) / 2}]),
    ([x ** 2 + y ** 2 - 5 * x * y / 2, x - y - x * y / 4], []),
    ([3 * x - 2 * y - 5, 81 * x ** 4 + 16 * y ** 4 - 6817], []),
    ([x ** 2 + y ** 2 - 1, x - y], []),
    ([x + x * y + y - 11, x ** 2 * y + x * y ** 2 - 30], []),
    ([2 * x ** 2 - 3 * x * y + y ** 2, y ** 2 - x ** 2 - 12], []),
    ([x ** 2 + y ** 4 - 20, 2 * x ** 4 + 2 * y ** 2 - 40], []),
    # lin-sys
    ([x - 3 * y + z - 4, 2 * x - 8 * y + 8 * z + 2, -6 * x + 3 * y - 15 * z - 9], []),
    ([x - 3 * y + z - 4, 2 * x - 8 * y + 8 * z + 2, ], []),
    ([x - 3 * y + z - 4, 2 * x - 8 * y + 8 * z + 2, 2 * x - 8 * y + 8 * z + 3], []),
    ([y + z - 1, x - y + z, 2 * x - 2 * y + 2 * z, 2 * x + y, 2 * x + y, y + z - 1, y + z - 1],
     [{x: -S(1) / 5, z: 3 / 5, y: 2 / 5}]),
    ([y + z - 1, y + z, 2 * x - 2 * y + 2 * z, 2 * x + y, 2 * x + y, y + z - 1, 2 * y + z - 1], []),
    ([x - y + 2 * z + 3, 4 * x + 4 * y - 2 * z - 1, -2 * x + 2 * y - 4 * z - 6], []),
    ([x - y, x + y + a], []),
    ([x - y, 2 * x - 2 * y, -x + y - 3], []),
    # abs
    (abs(x) - 5, []),
    (abs(3 * x + 4) - 7, []),
    (abs(2 - 5 * x) + 3, []),
    (abs(2 * x - 5) - abs(4 - x) + 18, []),
    (abs(abs(x) - 3) - 15, []),
    (abs(x ** 2 - 1 * x) - 2, []),
    # av
    (sin(3 * x) * cot(4 * x), []),
    (sin(6 * x) / sin(4 * x), []),
    (sin(2 * x) * sin(4 * x) * sin(6 * x) / sin(x), []),
    # exp
    (2 ** (pi * x + E) - 4, []),
    (2 ** x - 8, []),
    (5 ** (x + 2) - 125, []),
    (2 ** (2 * x) - 8 ** (x + 1), []),
    (3 ** (2 * x + 4) - 11 * 9 ** x - 210, []),
    (4 ** x - 3 * 2 ** x + 2, []),
    (2 ** (5 * x - 1) * 3 ** (3 * x - 1) * 5 ** (2 * x - 1) - 720 ** x, []),
    # ineq
    ([x ** 2 - 5 * x + 3 > 0], []),
    ([x ** 2 - 5 * x + 3 <= 0], []),
    ([x ** 2 - 5 * x + 3 < 0], []),
    ([x ** 2 - 5 * x + 3 >= 0, x > 0], []),
    ([(x ** 2 - 5 * x + 3) / (x - 3) >= 0], []),
    ([Abs(4 * x + 1) - 4 > 0], []),
    ([tan(x) < S(1) / 2], []),
    ([tan(x) <= S(1) / 2], []),
    ([tan(x) > S(1) / 2], []),
    ([tan(x) >= S(1) / 2], []),
    ([cot(x) < S(1) / 2], []),
    ([cot(x) <= S(1) / 2], []),
    ([cot(x) > S(1) / 2], []),
    ([cot(x) >= S(1) / 2], []),
    ([sin(x) < -2], []),
    ([sin(x) < 2], []),
    ([sin(x) < 1], []),
    ([sin(x) <= 1], []),
    ([sin(x) > -1], []),
    ([sin(x) >= -1], []),
    ([sin(2 * x) < 0], []),
    ([sin(2 * x + 1) < 0], []),
    # poly
    (5 * x ** 2 + 2, []),
    (4 * x ** 2 + 3 * x, [S(0), S(-3) / 4]),
    (2 * x ** 2 - 10 * x + 12, []),
    (3 * x ** 3 + 5 * x ** 2 + 2 * x - 4, []),
    (6 * x ** 3 - 11 * x ** 2 - 2 * x + 8, []),
    (x ** 4 + 5 * x ** 2 + 1, []),
    (x ** 4 + x ** 3 - 11 * x ** 2 - 5 * x + 30, []),
    (36 * x ** 4 - 13 * x ** 2 + 1, []),
    (179 * x ** 5 - 12351 * x ** 4 + 22557 * x ** 3 + 95737 * x ** 2 + 378 * x + 1608, []),
    ((x + 1) ** 4 + 5 * (x + 1) ** 2 + 1 * (x + 1), []),
    ((x ** 2 + 6 * x + 2) * (x ** 2 - 4 * x + 2), []),
    (((x + 1) ** 4) ** 2 + 5 * (x + 1) ** 4 + 1, []),
    ((3 * x + 2) ** 4 - 13 * (3 * x + 2) ** 2 + 36, []),
    ((x + 1) * (x + 2) * (x + 3) * (x + 4) - 24, []),
    ((8 * x + 7) ** 2 * (4 * x + 3) * (x + 1) - Rational(9, 2), []),
    # log
    (log(x, 2) - 10, []),
    (log(50 * x - 1, 7) - 5, []),
    (log(x, Rational(1, 3)) - 2, []),
    (log(2 * x - 1, Rational(1, 3)) - 2, []),
    (log(8, x - 1) - 1, []),
    (ln(E ** 2 + 2 * x - 3) - 2, []),
    (log(x, 3) - log(9, 3), []),
    (log(x ** 2 - 3, 3) - log(2 * x, 3), []),
    (2 * log((x - 1) ** 2, 7) + log((2 * x + 9) / (7 * x + 9), sqrt(7)), []),
    (log(x + 1) ** 2 + 10 - 11 * log(x + 1), []),
    (log(x ** 2 + 9 * x, 10) + log((x + 9) / x, 10), [-10]),
    (log(6 * sin(x) + 4, 3) * log(6 * sin(x) + 4, 5) - log(6 * sin(x) + 4, 3) - log(6 * sin(x) + 4, 5), []),
    (log(x ** 2 + 5 * x - 6, 2) - log(4 * x, 2), []),
    (log((x ** 3 - 5 * x ** 2) / (x - 5), 5) - 2, []),
    (log(2 * x) ** 2 + 3 * log(2 * x) + 2, []),
    # trig
    (Eq(cos(5 * x - pi / 6), sqrt(2) / 2), []),
    (Eq(tan(x ** 2 + 4 * x + pi / 4), 1), []),
    (Eq(sin(6 * x - pi / 3), sin(2 * x + pi / 4)), []),
    (Eq(cos(x ** 2), cos(4 * x - 3)), []),
    (Eq(6 * sin(x) ** 2 - 5 * sin(x) + 1, 0), []),
    (Eq(cos(6 * x + pi / 6) ** 2, Rational(1, 2)), []),
    (Eq(cos(3 * x ** 2) ** 2, Rational(3, 4)), []),
    (Eq(5 * sin(x) ** 2 + 3 * sin(x) + 4 * cos(x) ** 2, 5 + Rational(3, 4)), []),
    (Eq(sin(x) ** 4 + 3 * cos(x) - cos(x) ** 4 - 2, 0), []),
    (sin(x), []),
    (sin(x) - 1, []),
    (sin(x) + 1, []),
    (3 * sin(x) - 1, []),
    (sin(x) + 5 * sin(x), []),
    (sin(x) - Rational(1, 2), []),
    (sin(x) - sqrt(2) / 2, []),
    (sin(x) - Rational(1, 3), []),
    (cos(x), []),
    (cos(x) + 1, []),
    (cos(x) - 1, []),
    (tan(x) + -sqrt(3), []),
    (cot(x) - 1, []),
    (sin(2 * x) - Rational(1, 2), []),
    (sin(2 * x / 3), []),
    (sin(2 * x / 5 - 1), []),
    (sin(3 * x + pi / 4) + 1, []),
    (cos(x / 3) + sqrt(2) / 2, []),
    (tan(pi / 4 - x / 2) + 1, []),
    (cot(pi / 6 - x) - sqrt(3) / 3, []),
    (asin(x) - 1, []),
    (asin(2 * x + 1) - 0, []),
    (asin(x) + 4, []),
    (acos(x - 3) - pi / 2, []),
    (acos(x) + 1, []),
    (atan(x) - pi, []),
    (acot(2 * x - 4) - pi / 3, []),
    (5 * cos(x) ** 2 - 5 * cos(x) + 1, []),
    (8 * cos(x) ** 2 + 6 * sin(x) - 3, []),
    (3 * tan(x) ** 3 + tan(x), []),
    (sin(3 * x) * cos(4 * x), []),
    (sin(x) + sin(2 * x) + sin(3 * x), []),
    (2 * sin(x) + 3 * sin(2 * x) + 2 * sin(3 * x), []),
    # vilenkin
    (x ** sqrt(x) - x ** (x / 2), [0, 1, 4]),
    (4 - log(x, 10) - 3 * sqrt(log(x, 10)), [10]),
    (log(x, S(1) / 2) + log(x, 3) - 1, [3 ** log(2 ** (S(1) / (-log(3) + log(2))))]),
    (x ** log(x, 10) - x ** 100, [1, 10 ** 100]),
    (sin(3 * x) * cos(2 * x) * tan(7 * x), []),
    (cos(x ** 2) + cos(5 * x ** 2), []),
    (sqrt(3) * sin(x) + cos(x) - sqrt(2), []),
]

solve_9 = [
    (x ** 3 - 5 * x ** 2 + 8 * x - 6, [S(3)]),
    (Eq(5 * x ** 5, -160), [S(-2)]),
    (Eq(2 ** (2 * x + 1), 32), [S(2)]),
    (Eq(S(1) / 9 ** (2 * x - 5), 3 ** (5 * x - 8)), [S(2)]),
    (Eq(root(2, 3) ** x - 1, 2 / (root(2, 3) ** (2 * x))), [S(-1) / 3]),  # error in equation?
    (Eq((S(1) / 7) ** (3 * x + 3), 7 ** (2 * x)), [S(-3) / 5]),
    ([2 * x - 3 * y - 1, 2 * x ** 2 - x * y - 3 * y ** 2 - 3], [{x: S(2), y: S(1)}]),
    ([x * y - 10, S(1) / x - S(1) / y + 0.3], [{x: -2.0, y: -5.0}, {x: 5.0, y: 2.0}]),
    ([x ** 2 - y ** 2 - 12, x ** 2 + y ** 2 - 20], [{x: S(-4), y: S(-2)}, {x: S(4), y: S(2)}]),
    ([x * y ** 2 + x * y ** 3 - 10, x + x * y - 10], [{x: 5, y: 1}]),
    ([x ** 3 + 27 * y ** 3 - 54, x ** 2 - 6 * x * y + 9 * y ** 2], [{x: 3, y: 1}]),
    ([x - y - 5, sqrt(x) + sqrt(y) - 3], [{x: 1, y: 4}, {x: 4, y: 1}]),
    ([x * z + y * z - 16, x * y + y * z - 15, x * z + x * y - 7], [{x: 1, y: 3, z: 4}, {x: -1, y: -3, z: -4}]),
    (x ** 5 - 2 * x ** 4 - 3 * x ** 3 + 6 * x ** 2 - 4 * x + 8, [S(-2), S(2)]),
    (x ** 2 - 5 * x + 6 >= 0, Or(And(-oo < x, x < 3), And(3 < x, x < oo))),
    (Eq(sin(a) - cos(a), 0.6), [S(0.32)]),
    (x / (x ** 2 - 16) + (x - 1) / (x + 4) - 1, [S(5)]),
    ((2 * x + 3) / 5 + (7 * x - ((3 - x) / 2)) - (((7 * x + 11) / 3) + 1), [S(1)]),
    ([2 * x + 6 * y - 18, 3 * x - 5 * y + 29], [{x: -3, y: 4}]),
    ((3 * x - 2) / (2 * x + 5) - (x + 4) / (x - 10), [S(0.45)]),
    # hangs up the test execution
    (Eq(x ** (-S(1) / 4), 2), [S(1) / 16]),
    (Eq(root(x - 2, 2), root(3 * x, 6)), [S(2)]),
    (Eq(sqrt(x - 7) - sqrt(x + 17), -4), [S(8)]),
    (Eq(sqrt(2 - 2 * x), x + 3), [S(-1)]),
    (sqrt(5 * x + 11) > x + 3, Or(And(-2.2 < x, x < -2))),
    (6 - sqrt(x + 3), [S(33)]),
    (sqrt((x - 1) ** 2) - 1, [S(2), S(0)]),
    (sqrt(x + 3) + 5 - 7 * x, [S(1)]),
]

C1 = Symbol('C1')
C2 = Symbol('C2')
C3 = Symbol('C3')
C4 = Symbol('C4')

dsolve_generic = [
    (Derivative(y(x), x) - 3 * y(x) * x, Eq(y(x), C1 * exp(3 * x ** 2 / 2))),  # separable

    (y(x).diff(x, 4) + 2 * y(x).diff(x, 3) - 2 * y(x).diff(x, 2) - 6 * y(x).diff(x) + 5 * y(x),
     Eq(y(x), (C1 + C2 * x) * exp(x) + (C3 * sin(x) + C4 * cos(x)) * exp(-2 * x))),  # LHDE with CC

    (y(x).diff(x) - y(x) - y(x) ** 2 * exp(x), Eq(y(x), exp(x) / (C1 - exp(2 * x) / 2))),  # Bernoulli eq

    (y(x).diff(x, 2) * x ** 2 - 4 * y(x).diff(x) * x + 6 * y(x), Eq(y(x), x ** 2 * (C1 + C2 * x))),  # Euler eq

    (cos(y(x)) - (x * sin(y(x)) - y(x) ** 2) * y(x).diff(x), Eq(x * cos(y(x)) + y(x) ** 3 / 3, C1)),  # exact

    (y(x).diff(x, 2) + 2 * y(x).diff(x) + y(x) - 4 * exp(-x) * x ** 2 + cos(2 * x),
     Eq(y(x), (C1 + C2 * x + x ** 4 / 3) * exp(-x) - 4 * sin(2 * x) / 25 + 3 * cos(2 * x) / 25)),

    (y(x).diff(x, 3) - 3 * y(x).diff(x, 2) + 3 * y(x).diff(x) - y(x) - exp(x) * log(x),
     Eq(y(x), (C1 + C2 * x + C3 * x ** 2 + x ** 3 * (6 * log(x) - 11) / 36) * exp(x))),
]

dsolve_func = partial(dsolve, func=y(x))
