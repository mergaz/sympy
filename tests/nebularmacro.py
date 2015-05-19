from fractions import Fraction

from macropy.core.macros import *
from macropy.core.quotes import macros, q, u

macros = Macros()
S = None


@macros.expr
def symbolize(tree, **kw):
    new_tree = number_search.recurse(tree)
    return new_tree


@macros.decorator
def distribute_asserts(tree, gen_sym, exact_src, **kw):
    input_expr_src = []
    expected_results_src = []
    for statement in tree.body:
        if isinstance(statement, Assert):  # assert solve(a) == b
            input_expr_src.append(exact_src(statement.test.left))  # solve(a)
            expected_results_src.append(exact_src(statement.test.comparators[0]))  # b

    new_body = []
    func_names = []
    new_tree = number_search.recurse(tree)
    exp_res_vars = []
    for statement in new_tree.body:
        if isinstance(statement, Assert):  # assert solve(a) == b
            assign_stmt = Assign(targets=[Name(id=gen_sym())],
                                 value=statement.test.comparators[0])  # b
            exp_res_vars.append(assign_stmt.targets[0])
            new_body.append(assign_stmt)

            func_stmt = FunctionDef(
                name=gen_sym(),
                args=arguments([], None, None, []),
                body=[Return(value=statement.test.left)],
                decorator_list=[]
            )
            func_names.append(func_stmt.name)
            new_body.append(func_stmt)
        else:
            new_body.append(statement)
    print input_expr_src
    print expected_results_src
    print unparse(List(elts=exp_res_vars))

    wrappers = Return(List(elts=list(Name(id=n) for n in func_names)))
    new_tree.body = new_body + [wrappers]
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
