from sympy import *
from sympy.solvers.solvers import _solve

x = Symbol('x', real=True)
y, z, a, b, c = symbols("y, z, a, b, c")
t = Dummy('t')
# iv = _solve(2 ** x - t, x, tsolve=True, check=False)
iv = solve(root((81 - x), 3) < 3) == '???'
print iv
# print solve(2**x - 8)
# problems with NoneType not iterable are coming mostly from this change:
# https://github.com/sympy/sympy/commit/9b1f3d7402538c587a00fa4df162208998727830#diff-e2a46e260ac6a40415353a416f21fd4f
# see the full history at around 16 Jan
# https://github.com/sympy/sympy/commits/master/sympy/solvers/solvers.py
