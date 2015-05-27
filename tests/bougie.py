from sympy import *
from sympy.solvers.solvers import _solve

x = Symbol('x', real=True)
y, z, a, b, c = symbols("y, z, a, b, c")
t = Dummy('t')
iv = _solve(2 ** x - t, x, tsolve=True, check=False)
print iv
# print solve(2**x - 8)
