from macropy.core.macros import *
from macropy.core.quotes import macros, q, ast

macros = Macros()

@macros.expr
def expect(tree, gen_sym, **kw):
    name = gen_sym()
    return q[lambda: ast[tree]]
