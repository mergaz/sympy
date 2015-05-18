from macropy.core.macros import *
from macropy.core.quotes import macros, q, ast, u
from sympy import S

# macros = Macros()


@macros.expr
def asdf(tree, **kw):
    # addition = 10
    # new_tree = q[ast[tree] + u[addition]]
    # print real_repr(new_tree)
    # print unparse(new_tree)
    # return new_tree
    @Walker
    def number_search(tree, **kw):
        if type(tree) is BinOp and type(tree.left) is Num:
            print unparse(tree)
            tree.left = q[S(ast[tree.left])]
            print unparse(tree)

    new_tree = number_search.recurse(tree)
    print real_repr(new_tree)
    print unparse(new_tree)
    return new_tree
