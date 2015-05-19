from fractions import Fraction

from macropy.core.macros import *
from macropy.core.quotes import macros, q, u

S = None


@macros.expr
def symbolize(tree, **kw):
    new_tree = number_search.recurse(tree)
    return new_tree


@macros.decorator
def distribute_asserts(tree, gen_sym, exact_src, **kw):
    expressions = []
    expected_results = []
    for statement in tree.body:
        if isinstance(statement, Assert): # assert solve(a) == b
            expressions.append(exact_src(statement.test.left)) # solve(a)
    new_body = []
    func_names = []
    new_tree = number_search.recurse(tree)
    for statement in new_tree.body:
        if isinstance(statement, Assert): # assert solve(a) == b
            expected_results.append(statement.test.comparators[0]) # b
            new_stmt = FunctionDef(
                gen_sym(),
                arguments([], None, None, []),
                [Return(value=statement.test.left)],
                []
            )
            func_names.append(new_stmt.name)
            new_body.append(new_stmt)
        else:
            new_body.append(statement)
    wrappers = Return(List(elts=list(Name(id=n) for n in func_names)))
    new_tree.body = new_body + [wrappers]
    print expressions
    print unparse(List(elts=expected_results))
    print unparse(new_tree)
    return new_tree


@Walker
def number_search(tree, **kw):
    if isinstance(tree, BinOp):
        if isinstance(tree.left, Num):
            tree.left = num2S(tree.left.n)
        if isinstance(tree.right, Num):
            tree.right = num2S(tree.right.n)
    elif isinstance(tree, Compare):
        if isinstance(tree.left, Num):
            tree.left = num2S(tree.left.n)
        tree.comparators = list(num2S(cr.n) if isinstance(cr, Num) else cr for cr in tree.comparators)


def num2S(n):
    frac = Fraction(n).limit_denominator()
    if frac.denominator != 1:
        return q[S(u[int(frac.numerator)]) / u[int(frac.denominator)]]
    else:
        return q[S(u[int(frac.numerator)])]
