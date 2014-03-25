
import re
from sympy.core.relational import Equality
from sympy.parsing.sympy_parser import parse_expr, standard_transformations, implicit_multiplication, implicit_application, function_exponentiation, implicit_multiplication_application
from sympy.simplify.simplify import simplify
from sympy.solvers.solvers import solve

integrate_pattern_ = re.compile("integrate")


def has_eq(expr):
    if expr.func is Equality:
        return True
    for arg in expr.args:
        if has_eq(arg):
            return True
    return False


def compute(user_input):
    transformations = standard_transformations + (implicit_multiplication, implicit_application, function_exponentiation, implicit_multiplication_application)
    expr = parse_expr(user_input, transformations=transformations, change_assign_to_eq=True, change_eq_to_call_eq=True, evaluate=False)
    # if there is no free variables or input contains integrate, then just call simplify
    if len(expr.free_symbols) == 0 or (integrate_pattern_.match(user_input) and not has_eq(expr)):
        return simplify(expr)
    else:
        return solve(expr)
