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

def test_0(s):
    assert s(solve,'x ** 3 - 5 * x ** 2 + 8 * x - 6', [3])
def test_1(s):
    assert s(solve,'5 * x ** 5 == -160', [-2])
def test_2(s):
    assert s(solve,'2 ** (2 * x + 1) == 32', [2])
def test_3(s):
    assert s(solve,'(1 / 9) ** (2 * x - 5) == 3 ** (5 * x - 8)', [2])
def test_4(s):
    assert s(solve,'root(2, 3) ** x - 1 == 2 / (root(2, 3) ** (2 * x))', [-1 / 3])  # error in equation?
def test_5(s):
    assert s(solve,'(1 / 7) ** (3 * x + 3) == 7 ** (2 * x)', [-3 / 5])
def test_6(s):
    assert s(solve,'[2 * x - 3 * y - 1, 2 * x ** 2 - x * y - 3 * y ** 2 - 3]', [{x: 2, y: 1}])
def test_7(s):
    assert s(solve,'[x * y - 10, 1 / x - 1 / y + 0.3]', [{x: -2, y: -5}, {x: 5, y: 2}])
def test_8(s):
    assert s(solve,'[x ** 2 - y ** 2 - 12, x ** 2 + y ** 2 - 20]', [{x: -4, y: -2}, {x: -4, y: 2}, {x: 4, y: -2}, {x: 4, y: 2}])
def test_9(s):
    assert s(solve,'[x * y ** 2 + x * y ** 3 - 10, x + x * y - 10]', [{x: 5, y: 1}])
def test_10(s):
    assert s(solve,'[x ** 3 + 27 * y ** 3 - 54, x ** 2 - 6 * x * y + 9 * y ** 2]', [{x: 3, y: 1}])
def test_11(s):
    assert s(solve,'[x - y - 5, sqrt(x) + sqrt(y) - 3]', [{x: 1, y: 4}, {x: 4, y: 1}])
def test_12(s):
    assert s(solve,'[x * z + y * z - 16, x * y + y * z - 15, x * z + x * y - 7]', [{x: 1, y: 3, z: 4}, {x: -1, y: -3, z: -4}])
def test_13(s):
    assert s(solve,'x ** 5 - 2 * x ** 4 - 3 * x ** 3 + 6 * x ** 2 - 4 * x + 8', [-2, 2])
def test_14(s):
    assert s(solve,'x ** 2 - 5 * x + 6 >= 0', Or(x <= 2, x >= 3))
def test_15(s):
    assert s(solve,'sin(a) - cos(a) == 0.6', [0.32])
def test_16(s):
    assert s(solve,'x / (x ** 2 - 16) + (x - 1) / (x + 4) - 1', [5])
def test_17(s):
    assert s(solve,'(2 * x + 3) / 5 + (7 * x - ((3 - x) / 2)) - (((7 * x + 11) / 3) + 1)', [1])
def test_18(s):
    assert s(solve,'[2 * x + 6 * y - 18, 3 * x - 5 * y + 29]', {x: -3, y: 4})
def test_19(s):
    assert s(solve,'(3 * x - 2) / (2 * x + 5) - (x + 4) / (x - 10)', [0, 45])
def test_20(s):
    assert s(solve,'x ** (-1 / 4) == 2', [1 / 16])
def test_21(s):
    assert s(solve,'root(x - 2, 2) == root(3 * x, 6)', [2])
def test_22(s):
    assert s(solve,'sqrt(x - 7) - sqrt(x + 17) == -4', [8])
def test_23(s):
    assert s(solve,'sqrt(2 - 2 * x) == x + 3', [-1])
def test_24(s):
    assert s(solve,'sqrt(5 * x + 11) > x + 3', And(-2 < x, x < 1))
def test_25(s):
    assert s(solve,'6 - sqrt(x + 3)', [33])
def test_26(s):
    assert s(solve,'sqrt((x - 1) ** 2) - 1', [0, 2])
def test_27(s):
    assert s(solve,'sqrt(x + 3) + 5 - 7 * x', [1])
