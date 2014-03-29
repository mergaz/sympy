
import re
from sympy.core.relational import Equality
from sympy.integrals.integrals import integrate, Integral
from sympy.parsing.sympy_parser import parse_expr, standard_transformations, implicit_multiplication, implicit_application, function_exponentiation, implicit_multiplication_application
from sympy.simplify.simplify import simplify
from sympy.solvers.solvers import solve
from sympy.utilities.solution import add_exp

integrate_pattern_ = re.compile("integrate")


def has_eq(expr):
    if expr.func is Equality:
        return True
    for arg in expr.args:
        if has_eq(arg):
            return True
    return False


def compute(user_input):

    expr = parse_expr(user_input, mymath_hack=True, evaluate=False)
    # if there is no free variables or input contains integrate, then just call simplify
    print expr
    if len(expr.free_symbols) == 0:
        return add_exp(expr)
    elif isinstance(expr, Integral):
        return integrate(expr.function, expr.limits)
    else:
        return solve(expr)
