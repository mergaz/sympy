from __future__ import print_function, division
import sympy

from sympy.core import S, Symbol, Add, sympify, Expr, PoleError, Mul
from sympy.core.compatibility import string_types
from sympy.core.symbol import Dummy
from sympy.functions.combinatorial.factorials import factorial
from sympy.functions.special.gamma_functions import gamma
from sympy.series.order import Order
from sympy.core.numbers import NaN
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


def lim(f, x, x0):
    return limit(f, x, x0)


def limit(e, z, z0, dir="+"):
    """
    Compute the limit of e(z) at the point z0.

    z0 can be any expression, including oo and -oo.

    For dir="+" (default) it calculates the limit from the right
    (z->z0+) and for dir="-" the limit from the left (z->z0-).  For infinite
    z0 (oo or -oo), the dir argument is determined from the direction
    of the infinity (i.e., dir="-" for oo).

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

    return Limit(e, z, z0, dir).doit(deep=False)


def heuristics(e, z, z0, dir):
    rv = None

    if abs(z0) is S.Infinity:
        rv = limit(e.subs(z, 1/z), z, S.Zero, "+" if z0 is S.Infinity else "-")
        if isinstance(rv, Limit):
            return
    elif e.is_Mul or e.is_Add or e.is_Pow or e.is_Function:
        r = []
        for a in e.args:
            l = limit(a, z, z0, dir)
            if l.has(S.Infinity) and l.is_finite is None:
                return
            elif isinstance(l, Limit):
                return
            elif l is S.NaN:
                return
            else:
                r.append(l)
        if r:
            rv = e.func(*r)
            if rv is S.NaN:
                return

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

        if z0 is S.Infinity:
            dir = "-"
        elif z0 is S.NegativeInfinity:
            dir = "+"

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
                    u = Dummy(positive=(z0 is S.Infinity))
                    inve = e.subs(z, 1/u)
                    r = limit(inve.as_leading_term(u), u,
                              S.Zero, "+" if z0 is S.Infinity else "-")
                    if isinstance(r, Limit):
                        return self
                    else:
                        return r

        if e.is_Order:
            return Order(limit(e.expr, z, z0), *e.args[1:])

        try:
            r = gruntz(e, z, z0, dir)
            if r is S.NaN:
                raise PoleError()
        except (PoleError, ValueError):
            r = heuristics(e, z, z0, dir)
            if r is None:
                return self

        return r



def _min_degree(f, x):
    md = oo
    for t in f.as_terms()[0]:
        if t[0].is_polynomial(x):
            p = Poly(t[0], x)
            d = p.degree(x)
            if d < md:
                md = d
    return md


def _to_series(f, x, x0):
    term = f.series(n=None)
    r = next(term)
    return r

def split_xs_(num, x):
    numxs = 0
    numr = []
    cs = 1
    if num == x:
        numxs = 1
    elif num.is_Pow and num.args[0] == x and num.args[1].is_Number:
        numxs = num.args[1]
    elif num.is_Pow and num.args[1].is_Number:
        p = num.args[1]
        axs, ar, acs = split_xs_(num.args[0], x)
        numxs += axs*p
        numr += [(t[0], t[1]*p) for t in ar]
        cs *= acs**p
    elif num.subs(x, 0) != 0:
        cs *= num
    elif num.is_Mul:
        for nf in num.args:
            axs, ar, acs = split_xs_(nf, x)
            numxs += axs
            numr += ar
            cs *= acs
    else:
        numr = [(num, 1)]
    return numxs, numr, cs


def _manuallimit(f, x, x0):
    add_comment("Evaluate the limit")
    add_exp(Limit(f, x, x0))
    if f.func is Mul:
        consts = []
        factors = []
        rest = []
        for factor in f.args:
            if not factor.has(x):
                consts.append(factor)
            else:
                try:
                    lf = limit(factor, x, x0)
                except:
                    lf = NaN
                if lf.is_finite and lf != 0:
                    factors.append(factor)
                else:
                    rest.append(factor)
        if len(consts) > 0 or len(factors) > 1:
            add_comment("Using multiplication rule, we obtain")
            if len(consts):
                const = Mul(*consts)
            else:
                const = 1
            limits = []
            for factor in factors:
                limits.append(Limit(factor, x, x0))
            if len(rest) > 0:
                limits.append(Limit(Mul(*rest), x, x0))
            add_eq(Limit(f, x, x0), const * Mul(*limits))
            if len(limits) > 1:
                add_comment("Evaluate these limits")
            results = []
            if const != 1:
                results.append(const)
            for l in limits:
                lr = _manuallimit(l.args[0], x, x0)
                results.append(lr)
            add_comment("Finally, we get")
            result = Mul(*results)
            add_eq(Limit(f, x, x0), Mul(*results))
            return result

        num, den = f.as_numer_denom()
        if num.is_polynomial(x) and den.is_polynomial(x) and den != 1:
            if x0 == oo or x0 == -oo:
                add_comment("The function is a quotient of two polynomials")
                num = Poly(num, x)
                den = Poly(den, x)
                d = min(den.degree(x), num.degree())
                num = expand(num / x**d)
                den = expand(den / x**d)
                add_comment("Dividing the numerator and denominator by ")
                add_exp(x**d)
                add_comment("The limit is")
                f = num / den
                add_exp(Limit(f, x, x0))
                add_comment("Evaluate the limits of the numerator and the denominator")
                lnum = _manuallimit(num, x, x0)
                lden = _manuallimit(den, x, x0)
                if lnum == oo or lnum == -oo:
                    lf = limit(f, x, x0)
                elif lden == 0:
                    lf = limit(f, x, x0)
                else:
                    lf = lnum / lden
                add_comment("Finally, we obtain")
                add_eq(Limit(f, x, x0), lf)
                return lf

    if f.func is Add:
        consts = []
        summands = []
        rest = []
        for summand in f.args:
            if not summand.has(x):
                consts.append(summand)
            else:
                try:
                    lf = limit(summand, x, x0)
                except:
                    lf = NaN
                if lf.is_finite:
                    summands.append(summand)
                else:
                    rest.append(summand)
        if len(consts) > 0 or len(summands) > 1:
            add_comment("Using addition rule, we obtain")
            if len(consts):
                const = Add(*consts)
            else:
                const = 0
            limits = []
            for summand in summands:
                limits.append(Limit(summand, x, x0))
            if len(rest) > 0:
                limits.append(Limit(Add(*rest), x, x0))
            add_eq(Limit(f, x, x0), const + Add(*limits))
            if len(limits) > 1:
                add_comment("Evaluate these limits")
            results = []
            if const != 0:
                results.append(const)
            for l in limits:
                lr = _manuallimit(l.args[0], x, x0)
                results.append(lr)
            add_comment("Finally, we get")
            result = Add(*results)
            add_eq(Limit(f, x, x0), result)
            return result

    if x0 != oo and x0 != -oo and x0 != 0:
        add_comment("Rewrite this limit as")
        y = Dummy("y")
        add_eq(Limit(f, x, x0), Limit(f.subs(x, y + x0), y, 0))
        return _manuallimit(f.subs(x, y + x0), y, 0)
    if f.is_Pow:
        if f.args[0].has(x) and f.args[1].has(x):
            add_comment("Rewrite this limit as")
            add_exp(exp(Limit(f.args[1] * log(f.args[0]), x, x0)))
            _manuallimit(f.args[1] * log(f.args[0]), x, x0)
            add_comment("Finally, ")
            r = limit(f, x, x0)
            add_eq(Limit(f, x, x0), r)
            return r
    if x0 == 0:
        if f.func is Mul:
            num_, den_ = f.as_numer_denom()
            num = expand(num_)
            den = expand(den_)
            f_ = (num / den).cancel()
            if num != num_ or den != den_ or f_ != (num / den).cancel():
                add_comment("Rewrite this limit as")
                add_eq(Limit(f, x, x0), Limit(f_, x, x0))
                return _manuallimit(f_, x, x0)
            else:
                numxs, numr, nc = split_xs_(num, x)
                denxs, denr, dc = split_xs_(den, x)
                ncc = 1
                dcc = 1
                nr = []
                dr = []
                for n in numr:
                    s = _to_series(n[0], x, x0)
                    l = limit(n[0] / s, x, x0)
                    if l.is_finite and l != 0:
                        add_comment("We know that")
                        r = Limit(n[0] / s, x, x0)
                        nr.append(r**n[1])
                        add_eq(r, l)
                        p = Poly(s, x)
                        denxs -= p.degree()
                        ncc *= p.nth(p.degree())
                    else:
                        nc *= n[0]**n[1]
                for d in denr:
                    s = _to_series(d[0], x, x0)
                    l = limit(d[0] / s, x, x0)
                    if l.is_finite and l != 0:
                        add_comment("We know that")
                        r = Limit(d[0] / s, x, x0)
                        dr.append(r**d[1])
                        add_eq(r, l)
                        p = Poly(s, x)
                        numxs -= p.degree()
                        dcc *= p.nth(p.degree())
                    else:
                        dc *= d[0]**d[1]
                result = limit(f, x, x0)
                rest = (x**numxs / x**denxs * nc / dc).cancel()
                if rest != 1:
                    rest = Limit(rest, x, x0)
                rr = ncc / dcc * Mul(*nr) / Mul(*dr) * rest
                if rr != Limit(f, x, x0):
                    add_comment("Therefore, we obtain")
                    add_eq(Limit(f, x, x0), rr)
                    add_comment("Finally, we have")
                    add_eq(Limit(f, x, x0), result)
                return result
    add_comment("This limit is equal to")
    v = limit(f, x, x0)
    add_exp(v)
    return v

