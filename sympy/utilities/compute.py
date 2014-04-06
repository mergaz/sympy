
import re
from sympy.core.function import nfloat
from sympy.core.relational import Equality
from sympy.core.symbol import Dummy
from sympy.integrals.integrals import integrate, Integral
from sympy.mpmath.calculus import approximation
from sympy.parsing.sympy_parser import parse_expr, standard_transformations, implicit_multiplication, implicit_application, function_exponentiation, implicit_multiplication_application
from sympy.simplify.simplify import simplify, nsimplify
from sympy.solvers.solvers import solve
from sympy.utilities.solution import add_exp, add_comment

integrate_pattern_ = re.compile("integrate")


def has_eq(expr):
    if expr.func is Equality:
        return True
    for arg in expr.args:
        if has_eq(arg):
            return True
    return False


def compute(user_input):
    print(user_input)
    expr = parse_expr(user_input, mymath_hack=True, evaluate=False)
    # if there is no free variables or input contains integrate, then just call simplify
    if len(expr.free_symbols) == 0:
        add_exp(expr)
        add_comment("Simplify")
        add_exp(simplify(expr))
        add_comment("Approximate")
        add_exp(nfloat(expr))
        return expr
    elif isinstance(expr, Integral):
        return integrate(simplify(expr.function), expr.limits)
    else:
        return solve(expr)
