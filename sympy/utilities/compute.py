from sympy.core.function import nfloat, Derivative
from sympy.core.sympify import sympify
from sympy.derivative.manualderivative import derivative
from sympy.integrals.integrals import integrate, Integral
from sympy.parsing.sympy_parser import parse_expr
from sympy.series.limits import Limit, _manuallimit
from sympy.simplify.simplify import simplify
from sympy.solvers.solvers import solve
from sympy.utilities.solution import add_exp, add_comment


def compute(user_input):
    expr = parse_expr(user_input, mymath_hack=True, evaluate=False)
    if isinstance(expr, Integral):
        return integrate(sympify(expr.function), expr.limits)
    elif isinstance(expr, Derivative):
        return derivative(sympify(expr.expr), list(expr.free_symbols)[0])
    elif isinstance(expr, Limit):
        return _manuallimit(expr.args[0], expr.args[1], expr.args[2])
    elif len(expr.free_symbols) == 0:
        add_exp(expr)
        add_comment("Simplify")
        add_exp(simplify(expr))
        add_comment("Approximate")
        add_exp(nfloat(expr))
        return expr
    else:
        return solve(expr)
