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

#def test_logsolve():
def test_70():
    assert simplify(log(125, 3) - 3) == 125
def test_71():
    assert simplify(log(27, (sqrt(1 / 3))) + 6) == 27
def test_72():
    assert simplify(log(0.008, 0.2) - 3) == 0.008
def test_73():
    assert simplify(1.7 ** log(2, 1.7)) == 2
def test_74():
    assert solve(sympify('log(x, 1 / 6) + 3')) == [216]
def test_75():
    assert solve(sympify('log(1 / 4, x) + 2')) == [2]
def test_76():
    assert solve(sympify('log(1 / 9, x) + 1')) == [9]
def test_77():
    assert solve(sympify('log(1 / 9, x) + 1 / 3')) == [729]
def test_78():
    assert solve(sympify('log(x, 0.3) - 2 * log(6, 0.3) + log(12, 0.3)')) == [3] #infinite reqursion?
def test_79():
    assert solve(sympify('log((2 * x - 4), 1 / 3) + 2')) == [6.5]
def test_80():
    assert solve(sympify('log(x, 3) > 2')) == And(9 < x, x < oo)
def test_81():
    assert solve(sympify('log((12 - 2 * x - x ** 2), 3) > 2')) == And(-3 < x, x < 1)
def test_82():
    assert solve(sympify('log(x + 1, pi) + log(x, pi) < log(2, pi)')) == And(0 < x, x < 1)
def test_83():
    assert solve(sympify('log(x, 10) ** 2 + 2 * log(x, 10) < 3')) == Or(And(0 < x, x < 1), And(10 < x, x < oo))
def test_84():
    assert solve(sympify('4 ** x - 2 ** x <= 2')) == And(-oo < x, x <= 1)
def test_85():
    assert solve(sympify('log(x, a) - log(3, a) - log(5, a), x')) == [15]
def test_86():
    assert solve(sympify('log(x, a) - log(2, sqrt(a)) + log(3, 1 / a), x')) == [4 / 3]
def test_87():
    assert solve(sympify('log(x, 10) ** 2 - 1')) == [10, 0.1]
def test_88():
    assert solve(sympify('log(x + 1, 2) ** 2 - log(x + 1, 1 / 4) - 5')) == [25, 0.2]
def test_89():
    assert solve(sympify('x ** log(x, 10) - 10000')) == [0.01, 100]
def test_90():
    assert solve(sympify('x ** log(x, 5) - 125 * (x ** 2)')) == [0]
def test_91():
    assert solve(sympify('x ** log(x - 2, 2) - 8')) == [8, 1 / 2]
def test_92():
    assert solve(sympify('1 / (log(x, 10) - 6) + 5 / (log(x, 10) + 2) - 1')) == [100, 10 ** 8]
def test_93():
    assert solve(sympify('log(x, 2) + 4 / log(2, x) - 5')) == [2]
def test_94():
    assert solve(sympify('2 * log(x, sqrt(3)) + log(1 / 3, x) - 3')) == [0]
def test_95():
    assert solve(sympify('log(1 / 8, x) + 3')) == [2]
def test_96():
    assert solve(sympify('log(9, x) - 1 / 2')) == [81]
def test_97():
    assert solve(sympify('log(x, 7) + 1')) == [1 / 7]
def test_98():
    assert solve(sympify('log(x, 0.3) - 2')) == [0.09] #infinite reqursion?
def test_99():
    assert solve(sympify('log(x, 6) >= 2')) == And(36 <= x, x < oo)
def test_100():
    assert solve(sympify('log(x, 9) <= 1 / 2')) == And(-oo < x, x <= 3)
def test_101():
    assert solve(sympify('log(x, 1 / 3) < -4')) == And(81 < x, x < oo)
def test_102():
    assert solve(sympify('log(x, 0.2) > -3')) == And(-oo < x, x < 125) #infinite reqursion?
def test_103():
    assert solve(sympify('log(x, 1 / 3) - log(7, 1 / 3) - log(4, 1 / 3)')) == [28]
def test_104():
    assert solve(sympify('log(x, 1 / 4) - log(9, 1 / 4) - log(5, 1 / 4)')) == [45]
def test_105():
    assert solve(sympify('log(3, 1 / 2) + log(x, 1 / 2) - log(12, 1 / 2)')) == [45]
def test_106():
    assert solve(sympify('log(8, 1 / 3) + log(x, 1 / 3) - log(4, 1 / 3)')) == [1 / 2]
def test_107():
    assert solve(sympify('log(x / 2, sqrt(3)) - log(6, sqrt(3)) - log(2, sqrt(3))')) == [24]
def test_108():
    assert solve(sympify('log(x / 3, sqrt(2)) - log(15, sqrt(2)) + log(6, sqrt(3))')) == [15 / 2]
def test_109():
    assert solve(sympify('3 * log(1 / 2, 2) - log(1 / 32, 2) - log(x, 2)')) == [45]
def test_110():
    assert solve(sympify('log(x ** 2 - 5 * x + 8, 3.4) - log(x, 3.4)')) == [4, 2] #infinite reqursion?
def test_111():
    assert solve(sympify('log(x / 3, 1 / 2) >= -2')) == And(0 > x, x < 5 / 4)
def test_112():
    assert solve(sympify('log(5 * x - 9, 1 / 3) >= log(4 * x, 1 / 3)')) == And(9 / 5 < x, x <= 9)
def test_113():
    assert solve(sympify('log(-x, 1 / 3) > log(4 - 2 * x, 1 / 3)')) == And(-oo < x, x < 0)
def test_114():
    assert solve(sympify('log(x, 2) ** 2 > 4 * log(x, 2) - 3')) == Or(And(0 < x, x < 2), And(8 < x, x < oo))
def test_115():
    assert solve(sympify('2 * log(x, 0.3) ** 2 - 7 * log(x, 0.3) - 4 <= 0')) == And(-1 / 2 <= x, x <= 4) #infinite reqursion?
def test_116():
    assert solve(sympify('log(x ** 2, 1 / 3) ** 2 - 7 * log(x, 1 / 3) + 3 <= 0')) == \
           And(1 / 3 <= x, x <= 1 / root(27, 4))
def test_117():
    assert solve(sympify('3 * log(x, 1 / 3) < log(9, 1 / 3) + log(3, 1 / 3)')) == And(3 < x, x < oo)
def test_118():
    assert solve(sympify('log(x, 1 / 2) + log(10 - x, 1 / 2) >= -1 + log(9 / 2, 1 / 2)')) == \
           Or(And(0 < x, x <= 1), And(9 <= x, x < 10))
def test_119():
    assert solve(sympify('log(7 - x, 0.4) >= log(3 * x + 6, 0.4)')) == Or(x >= 1 / 4, Eq(x, 6)) #infinite reqursion?
