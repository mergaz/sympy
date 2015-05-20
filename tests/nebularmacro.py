from fractions import Fraction
from operator import add
from functools import reduce

from macropy.core.macros import *
from macropy.core.quotes import macros, q, u, name, ast, ast_list

macros = Macros()
S = None


@macros.expr
def symbolize(tree, **kw):
    new_tree = number_search.recurse(tree)
    return new_tree


@macros.decorator
def parallelize_asserts(tree, gen_sym, exact_src, **kw):
    """
    Transforms all asserts in a function of the form
        def test_me():
            assert solve(a1) == b1
            print "hi"
            assert solve(a2) == b2
    into
        def test_me():
            expected_1 = lambda: b1
            actual_1 = lambda: solve(a1)
            print "hi"
            expected_2 = lambda: b2
            actual_2 = lambda: solve(a2)
            return [('solve(a1)', 'b1', expected_1, actual_1), ('solve(a2)', 'b2', expected_2, actual_2)]
    """
    transformer = lambda stmt: (transform_assert(stmt, gen_sym, exact_src) if isinstance(stmt, Assert)
                                else ([stmt], None, None, None, None))
    transformed_statements = map(transformer, tree.body)
    new_body = reduce(add, [ts[0] for ts in transformed_statements])

    ret = list(q[u[in_str], u[ex_str], name[ex_sym], name[ac_sym]]
               for code, in_str, ex_str, ex_sym, ac_sym in transformed_statements
               if in_str is not None)
    tree.body = new_body + [Return(value=q[ast_list[ret]])]
    new_tree = number_search.recurse(tree)
    # print unparse(new_tree)
    return new_tree


def transform_assert(stmt, gen_sym, exact_src):
    """
    Transforms and assert statement of the form
        assert solve(a) == b
    into
        expected_1 = lambda: b
        actual_1 = lambda: solve(a)
    :return: ('solve(a)', 'b', expected_1, actual_1)
    """
    input_str = exact_src(stmt.test.left)  # solve(a)
    expected_str = exact_src(stmt.test.comparators[0])  # b
    expected_sym = gen_sym("expected_")
    actual_sym = gen_sym("actual_")
    with q as code:
        name[expected_sym] = lambda: ast[stmt.test.comparators[0]]
        name[actual_sym] = lambda: ast[stmt.test.left]
    copy_location(code[0], stmt.test.comparators[0])
    copy_location(code[1], stmt.test.left)

    return code, input_str, expected_str, expected_sym, actual_sym


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
