from __future__ import print_function, division

from sympy.core import S, Symbol, Add, sympify, Expr, PoleError, C
from sympy.core.compatibility import string_types
from sympy.functions import factorial, gamma
from .gruntz import gruntz
from sympy.utilities.solution import start_subroutine, commit_subroutine, cancel_subroutine
from sympy.core.function import expand
from sympy.core.mul import Mul, prod
from sympy.core.singleton import S
from sympy.core.symbol import Dummy
from sympy.functions.elementary.exponential import exp, log
from sympy.polys.polytools import Poly
from sympy.utilities.solution import add_comment, add_exp, add_eq
from sympy.core import oo


def lim(f, x, x0, dir="+"):
    start_subroutine("Evaluate the limit")
    add_comment("Evaluate the limit")
    l = _manuallimit(f, x, x0)
    test = limit(f, x, x0, dir)
    if l == test:
        commit_subroutine()
        return l
    else:
        cancel_subroutine()
        return test


def limit(e, z, z0, dir="+"):
    """
    Compute the limit of e(z) at the point z0.

    z0 can be any expression, including oo and -oo.

    For dir="+" (default) it calculates the limit from the right
    (z->z0+) and for dir="-" the limit from the left (z->z0-). For infinite z0
    (oo or -oo), the dir argument doesn't matter.

    Examples
    ========

    >>> from sympy import limit, sin, Symbol, oo
    >>> from sympy.abc import x
    >>> limit(sin(x)/x, x, 0)
    1
    >>> limit(1/x, x, 0, dir="+")
    oo
    >>> limit(1/x, x, 0, dir="-")
    -oo
    >>> limit(1/x, x, oo)
    0

    Notes
    =====

    First we try some heuristics for easy and frequent cases like "x", "1/x",
    "x**2" and similar, so that it's fast. For all other cases, we use the
    Gruntz algorithm (see the gruntz() function).
    """
    e = sympify(e)
    z = sympify(z)
    z0 = sympify(z0)

    if e == z:
        return z0

    if not e.has(z):
        return e

    # gruntz fails on factorials but works with the gamma function
    # If no factorial term is present, e should remain unchanged.
    # factorial is defined to be zero for negative inputs (which
    # differs from gamma) so only rewrite for positive z0.
    if z0.is_positive:
        e = e.rewrite(factorial, gamma)

    if e.is_Mul:
        if abs(z0) is S.Infinity:
            # XXX todo: this should probably be stated in the
            # negative -- i.e. to exclude expressions that should
            # not be handled this way but I'm not sure what that
            # condition is; when ok is True it means that the leading
            # term approach is going to succeed (hopefully)
            ok = lambda w: (z in w.free_symbols and
                 any(a.is_polynomial(z) or
                 any(z in m.free_symbols and m.is_polynomial(z)
                 for m in Mul.make_args(a))
                 for a in Add.make_args(w)))
            if all(ok(w) for w in e.as_numer_denom()):
                u = C.Dummy(positive=(z0 is S.Infinity))
                inve = e.subs(z, 1/u)
                return limit(inve.as_leading_term(u), u,
                    S.Zero, "+" if z0 is S.Infinity else "-")

    if e.is_Add:
        if e.is_rational_function(z):
            rval = Add(*[limit(term, z, z0, dir) for term in e.args])
            if rval != S.NaN:
                return rval

    if e.is_Order:
        return C.Order(limit(e.expr, z, z0), *e.args[1:])

    try:
        r = gruntz(e, z, z0, dir)
        if r is S.NaN:
            raise PoleError()
    except (PoleError, ValueError):
        r = heuristics(e, z, z0, dir)
    return r


def heuristics(e, z, z0, dir):
    if abs(z0) is S.Infinity:
        return limit(e.subs(z, 1/z), z, S.Zero, "+" if z0 is S.Infinity else "-")

    rv = None
    bad = (S.NaN, None)

    if e.is_Mul or e.is_Add or e.is_Pow or e.is_Function:
        r = []
        for a in e.args:
            try:
                r.append(limit(a, z, z0, dir))
            except PoleError:
                break
            if r[-1] in bad:
                break
        else:
            if r:
                rv = e.func(*r)

    if rv in bad:
        msg = "Don't know how to calculate the limit(%s, %s, %s, dir=%s), sorry."
        raise PoleError(msg % (e, z, z0, dir))

    return rv


class Limit(Expr):
    """Represents an unevaluated limit.

    Examples
    ========

    >>> from sympy import Limit, sin, Symbol
    >>> from sympy.abc import x
    >>> Limit(sin(x)/x, x, 0)
    Limit(sin(x)/x, x, 0)
    >>> Limit(1/x, x, 0, dir="-")
    Limit(1/x, x, 0, dir='-')

    """

    def __new__(cls, e, z, z0, dir="+"):
        e = sympify(e)
        z = sympify(z)
        z0 = sympify(z0)
        if isinstance(dir, string_types):
            dir = Symbol(dir)
        elif not isinstance(dir, Symbol):
            raise TypeError("direction must be of type basestring or Symbol, not %s" % type(dir))
        if str(dir) not in ('+', '-'):
            raise ValueError(
                "direction must be either '+' or '-', not %s" % dir)
        obj = Expr.__new__(cls)
        obj._args = (e, z, z0, dir)
        return obj

    def doit(self, **hints):
        """Evaluates limit"""
        e, z, z0, dir = self.args
        if hints.get('deep', True):
            e = e.doit(**hints)
            z = z.doit(**hints)
            z0 = z0.doit(**hints)
        return limit(e, z, z0, str(dir))



def _min_degree(f, x):
    md = oo
    for t in f.as_terms()[0]:
        if t[0].is_polynomial(x):
            p = Poly(t[0], x)
            d = p.degree(x)
            if d < md:
                md = d
    return md


def _is_series(f, x):
    for t in f.as_terms()[0]:
        if not t[0].is_polynomial(x) and not t[0].is_Order:
            return False
    return True

def _to_series(f, x, x0):
    term = f.series(n=None)
    r = next(term)
    d = Poly(r, x).degree()
    return f.series(n=d + 1)


def _rewrite_factors_using_series(factors, x, x0):
    u = Dummy("u")
    rewriten_factors = []
    for factor in factors:
        base, power = factor.as_base_exp()
        if base != x and base.subs(x, x0) == 0:
            add_comment("We know that")
            s = _to_series(base, x, x0)
            add_eq(base, s)
            rewriten_factors.append(_to_series(base, x, x0) ** power)
            continue
        rewriten_factors.append(factor)
    return rewriten_factors


def _manuallimit(f, x, x0):
    add_exp(Limit(f, x, x0))
    v = f.subs(x, x0)
    if not v is S.NaN:
        add_comment("This limit is equal to")
        add_exp(v)
        return v
    if x0 != oo and x0 != -oo and x0 != 0:
        add_comment("Rewrite this limit as")
        y = Dummy("y")
        return _manuallimit(f.subs(x, y + x0), y, 0)
    if f.is_Pow:
        add_comment("Rewrite this limit as")
        add_exp(exp(Limit(f.args[1] * log(f.args[0]), x, x0)))
        add_comment("Evaluate the limit")
        return exp(_manuallimit(f.args[1] * log(f.args[0]), x, x0))

    if x0 == oo or x0 == -oo:
        if f.func is Mul:
            num, den = f.as_numer_denom()
            if num.is_polynomial(x) and den.is_polynomial(x):
                num = Poly(num, x)
                den = Poly(den, x)
                d = min(num.degree(x), den.degree(x))
                num = expand(num / x**d)
                den = expand(den / x**d)
                f = num / den
                add_comment("Rewrite this limit as")
                return _manuallimit(f, x, x0)
    if x0 == 0:
        if f.func is Mul:
            num, den = f.as_numer_denom()
            num = expand(num)
            den = expand(den)
            if _is_series(num, x) and _is_series(den, x):
                d1 = _min_degree(num, x)
                d2 = _min_degree(den, x)
                d = max(d1, d2)
                num = expand(num / x**d)
                den = expand(den / x**d)
                f = num / den
                add_comment("Rewrite this limit as")
                return _manuallimit(f, x, x0)

            rf = prod(_rewrite_factors_using_series(f.args, x, x0))
            if rf != f:
                add_comment("Rewrite this limit as")
                return _manuallimit(rf, x, x0)
