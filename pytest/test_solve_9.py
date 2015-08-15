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

def test_0():
    assert solve(sympify('x ** 3 - 5 * x ** 2 + 8 * x - 6')) == [3]
def test_1():
    assert solve(sympify('5 * x ** 5 == -160')) == [-2]
def test_2():
    assert solve(sympify('2 ** (2 * x + 1) == 32')) == [2]
def test_3():
    assert solve(sympify('(1 / 9) ** (2 * x - 5) == 3 ** (5 * x - 8)')) == [2]
def test_4():
    assert solve(sympify('root(2, 3) ** x - 1 == 2 / (root(2, 3) ** (2 * x))')) == [-1 / 3]  # error in equation?
def test_5():
    assert solve(sympify('(1 / 7) ** (3 * x + 3) == 7 ** (2 * x)')) == [-3 / 5]
def test_6():
    assert solve(sympify('[2 * x - 3 * y - 1, 2 * x ** 2 - x * y - 3 * y ** 2 - 3]')) == [{x: 2, y: 1}]
def test_7():
    assert solve(sympify('[x * y - 10, 1 / x - 1 / y + 0.3]')) == [{x: -2, y: -5}, {x: 5, y: 2}]
def test_8():
    assert solve(sympify('[x ** 2 - y ** 2 - 12, x ** 2 + y ** 2 - 20]')) == \
           [{x: -4, y: -2}, {x: -4, y: 2}, {x: 4, y: -2}, {x: 4, y: 2}]
def test_9():
    assert solve(sympify('[x * y ** 2 + x * y ** 3 - 10, x + x * y - 10]')) == [{x: 5, y: 1}]
def test_10():
    assert solve(sympify('[x ** 3 + 27 * y ** 3 - 54, x ** 2 - 6 * x * y + 9 * y ** 2]')) == [{x: 3, y: 1}]
def test_11():
    assert solve(sympify('[x - y - 5, sqrt(x) + sqrt(y) - 3]')) == [{x: 1, y: 4}, {x: 4, y: 1}]
def test_12():
    assert solve(sympify('[x * z + y * z - 16, x * y + y * z - 15, x * z + x * y - 7]')) == \
           [{x: 1, y: 3, z: 4}, {x: -1, y: -3, z: -4}]
def test_13():
    assert solve(sympify('x ** 5 - 2 * x ** 4 - 3 * x ** 3 + 6 * x ** 2 - 4 * x + 8')) == [-2, 2]
def test_14():
    assert solve(sympify('x ** 2 - 5 * x + 6 >= 0')) == Or(x <= 2, x >= 3)
def test_15():
    assert solve(sympify('sin(a) - cos(a) == 0.6')) == [0.32]
def test_16():
    assert solve(sympify('x / (x ** 2 - 16) + (x - 1) / (x + 4) - 1')) == [5]
def test_17():
    assert solve(sympify('(2 * x + 3) / 5 + (7 * x - ((3 - x) / 2)) - (((7 * x + 11) / 3) + 1)')) == [1]
def test_18():
    assert solve(sympify('[2 * x + 6 * y - 18, 3 * x - 5 * y + 29]')) == {x: -3, y: 4}
def test_19():
    assert solve(sympify('(3 * x - 2) / (2 * x + 5) - (x + 4) / (x - 10)')) == [0, 45]
def test_20():
    assert solve(sympify('x ** (-1 / 4) == 2')) == [1 / 16]
def test_21():
    assert solve(sympify('root(x - 2, 2) == root(3 * x, 6)')) == [2]
def test_22():
    assert solve(sympify('sqrt(x - 7) - sqrt(x + 17) == -4')) == [8]
def test_23():
    assert solve(sympify('sqrt(2 - 2 * x) == x + 3')) == [-1]
def test_24():
    assert solve(sympify('sqrt(5 * x + 11) > x + 3')) == And(-2 < x, x < 1)
def test_25():
    assert solve(sympify('6 - sqrt(x + 3)')) == [33]
def test_26():
    assert solve(sympify('sqrt((x - 1) ** 2) - 1')) == [0, 2]
def test_27():
    assert solve(sympify('sqrt(x + 3) + 5 - 7 * x')) == [1]
