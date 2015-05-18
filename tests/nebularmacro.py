from macropy.core.macros import *
from macropy.core.quotes import macros, q, ast, u
from sympy import S
from fractions import Fraction


@macros.expr
def parallel(tree, **kw):
    new_tree = number_search.recurse(tree)
    # print unparse(new_tree)
    return new_tree


@Walker
def number_search(tree, **kw):
    if type(tree) is BinOp:
        if type(tree.left) is Num:
            tree.left = num2S(tree.left.n)
        if type(tree.right) is Num:
            tree.right = num2S(tree.right.n)
        # print unparse(tree)


def num2S(n):
    frac = Fraction(n).limit_denominator()
    if frac.denominator != 1:
        return q[S(u[frac.numerator]) / u[frac.denominator]]
    else:
        return q[S(u[frac.numerator])]
