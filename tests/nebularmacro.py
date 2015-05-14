from macropy.core.macros import *
from macropy.core.quotes import q, ast

macros = Macros()

@macros.expr
def expect(tree, gen_sym, **kw):
    with q as code:
        u = lambda: ast[tree]
    name = gen_sym()
    return code
