"""Tools for solving inequalities and systems of inequalities. """

from __future__ import print_function, division
from sympy import sqrt
from sympy.core import Symbol, Interval
from sympy.core.mul import Mul
from sympy.core.numbers import pi
from sympy.core.power import Pow
from sympy.core.relational import Relational, Eq, Ge, Lt, GreaterThan, StrictGreaterThan, StrictLessThan, LessThan
from sympy.core.singleton import S
from sympy.assumptions import ask, AppliedPredicate, Q
from sympy.core.symbol import Wild, Dummy
from sympy.functions import re, im, Abs
from sympy.functions.elementary.exponential import log
from sympy.functions.elementary.trigonometric import sin, cos, tan, cot, atan, acot, acos, asin
from sympy.logic import And
from sympy.mpmath import inf
from sympy.polys import Poly, PolynomialError, parallel_poly_from_expr
from sympy.polys.polyroots import roots
from sympy.printing.latex import latex
from sympy.simplify.simplify import simplify
from sympy.utilities.solution import add_comment, add_eq, add_exp


def signToRel(sign):
    if sign is '>':
        return StrictGreaterThan
    if sign is '>=':
        return GreaterThan
    if sign is '<':
        return StrictLessThan
    if sign is '<=':
        return LessThan


def corel(rel):
    if rel is StrictLessThan:
        return StrictGreaterThan
    if rel is LessThan:
        return GreaterThan
    if rel is StrictGreaterThan:
        return StrictLessThan
    if rel is GreaterThan:
        return LessThan


def solve_poly_inequality(numer, denom, rel):
    """Solve a polynomial inequality with rational coefficients.

    Examples
    ========

    >>> from sympy import Poly
    >>> from sympy.abc import x
    >>> from sympy.solvers.inequalities import solve_poly_inequality

    >>> solve_poly_inequality(Poly(x, x, domain='ZZ'), '==')
    [{0}]

    >>> solve_poly_inequality(Poly(x**2 - 1, x, domain='ZZ'), '!=')
    [(-oo, -1), (-1, 1), (1, oo)]

    >>> solve_poly_inequality(Poly(x**2 - 1, x, domain='ZZ'), '==')
    [{-1}, {1}]

    See Also
    ========
    solve_poly_inequalities
    """
    if rel == '==':
        add_comment("Find the roots of the the equation")
        from solvers import solve
        reals = solve(numer/denom, real=True)
        intervals = []
        for r in reals:
            intervals.append(Interval(r, r, False, False))
        return intervals

    if rel != '!=' and numer.degree() == 1 and denom.degree() == 0:
        add_comment("The solution of this ineqality is")
        a = numer.nth(1)
        b = numer.nth(0)
        c = -b / a
        rel = signToRel(rel)
        if a < 0:
            rel = corel(rel)
        if rel == StrictGreaterThan: # x > c
            i = Interval(c, S.Infinity, False, False)
        elif rel == GreaterThan: # x >= c
            i = Interval(c, S.Infinity, True, False)
        elif rel == StrictLessThan: # x < c
            i = Interval(S.NegativeInfinity, c, False, False)
        elif rel == LessThan: # x < c
            i = Interval(S.NegativeInfinity, c, False, True)
        add_exp(i)
        return [i]

    add_comment("Use the critical points method")
    add_comment("Find the roots of the the equation")
    add_eq(numer.as_expr(), 0)
    reals = roots(numer, filter='R')
    points = {}
    for r in reals:
        if rel == '>=' or rel == '<=':
            points[r] = False
        else:
            points[r] = True

    if denom != 1:
        add_comment("Find the roots of the denominator")
        add_eq(denom.as_expr(), 0)
        reals = roots(denom, filter='R')
        for r in reals:
            points[r] = True

    points[S.Infinity] = True
    points[S.NegativeInfinity] = True

    intervals = []
    points_ = points.keys()
    points_.sort()
    for i in range(0, len(points_) - 1):
        left = points_[i]
        right = points_[i + 1]
        interval = Interval(left, right, points[left], points[right])
        intervals.append(interval)
    del points_

    if rel == '!=':
        return intervals
    else:
        add_comment("Therefore we have the following intervals to test")
        for interval in intervals:
            add_exp(interval)

    result = []
    for interval in intervals:
        add_comment("Test the point")
        if interval.left == S.NegativeInfinity and interval.right == S.Infinity:
            p = 0
        elif interval.left == S.NegativeInfinity:
            p = interval.right - 1
        elif interval.right == S.Infinity:
            p = interval.left + 1
        else:
            p = (interval.right + interval.left) / 2
        add_eq(numer.gen, p)
        add_comment("We have")
        v = numer(p) / denom(p)
        if v > 0:
            add_exp(latex(v) + " > 0")
        elif v < 0:
            add_exp(latex(v) + " < 0")
        if (v > 0 and (rel == '>' or rel == '>=')) or (v < 0 and (rel == '<' or rel == '<=')):
            add_comment("Thus the interval")
            add_exp(interval)
            add_comment("is a part of the solution set")
            result.append(interval)
        else:
            add_comment("Thus the interval")
            add_exp(interval)
            add_comment("is not a part of the solution set")
    return result


def solve_rational_inequalities(eqs):
    """Solve a system of rational inequalities with rational coefficients.

    Examples
    ========

    >>> from sympy.abc import x
    >>> from sympy import Poly
    >>> from sympy.solvers.inequalities import solve_rational_inequalities

    >>> solve_rational_inequalities([[
    ... ((Poly(-x + 1), Poly(1, x)), '>='),
    ... ((Poly(-x + 1), Poly(1, x)), '<=')]])
    {1}

    >>> solve_rational_inequalities([[
    ... ((Poly(x), Poly(1, x)), '!='),
    ... ((Poly(-x + 1), Poly(1, x)), '>=')]])
    (-oo, 0) U (0, 1]

    See Also
    ========
    solve_poly_inequality
    """
    rslt = S.EmptySet
    for _eqs in eqs:
        result = Interval(S.NegativeInfinity, S.Infinity)
        for (numer, denom), rel in _eqs:
            add_comment("Solve the inequality")
            add_exp(Relational(numer.as_expr() / denom.as_expr(), 0, rel))
            intervals = solve_poly_inequality(numer, denom, rel)
            r = S.EmptySet
            for interval in intervals:
                r = r.union(interval)
            if len(intervals) > 1:
                add_comment("The have the following solution set")
                add_exp(r)
            result = result.intersect(r)
        if len(_eqs) > 1:
            add_comment("Finally we have the following solution set")
            add_exp(result)
        rslt = rslt.union(result)
    if len(eqs) > 1:
        add_comment("Thus we have the following solution set")
        add_exp(rslt)
    return rslt


def reduce_rational_inequalities(exprs, gen, assume=True, relational=True):
    """Reduce a system of rational inequalities with rational coefficients.

    Examples
    ========

    >>> from sympy import Poly, Symbol
    >>> from sympy.solvers.inequalities import reduce_rational_inequalities

    >>> x = Symbol('x', real=True)

    >>> reduce_rational_inequalities([[x**2 <= 0]], x)
    x == 0

    >>> reduce_rational_inequalities([[x + 2 > 0]], x)
    x > -2
    """
    exact = True
    eqs = []

    for _exprs in exprs:
        _eqs = []

        for expr in _exprs:
            if isinstance(expr, tuple):
                expr, rel = expr
            else:
                if expr.is_Relational:
                    expr, rel = expr.lhs - expr.rhs, expr.rel_op
                else:
                    expr, rel = expr, '=='

            try:
                (numer, denom), opt = parallel_poly_from_expr(expr.together().as_numer_denom(), gen)
            except PolynomialError:
                raise PolynomialError("only polynomials and rational functions are supported in this context")

            if not opt.domain.is_Exact:
                numer, denom, exact = numer.to_exact(), denom.to_exact(), False

            domain = opt.domain.get_exact()

            if not (domain.is_ZZ or domain.is_QQ or domain.is_EX):
                raise NotImplementedError("inequality solving is not supported over %s" % opt.domain)

            _eqs.append(((numer, denom), rel))

        eqs.append(_eqs)

    solution = solve_rational_inequalities(eqs)

    if not exact:
        solution = solution.evalf()

    if not relational:
        return solution

    real = ask(Q.real(gen), assumptions=assume)

    if not real:
        result = And(solution.as_relational(re(gen)), Eq(im(gen), 0))
    else:
        result = solution.as_relational(gen)

    return result


def reduce_abs_inequality(expr, rel, gen, assume=True):
    """Reduce an inequality with nested absolute values.

    Examples
    ========

    >>> from sympy import Q, Abs
    >>> from sympy.abc import x
    >>> from sympy.solvers.inequalities import reduce_abs_inequality

    >>> reduce_abs_inequality(Abs(x - 5) - 3, '<', x, assume=Q.real(x))
    And(2 < x, x < 8)

    >>> reduce_abs_inequality(Abs(x + 2)*3 - 13, '<', x, assume=Q.real(x))
    And(-19/3 < x, x < 7/3)

    See Also
    ========
    reduce_abs_inequalities
    """
#    if not ask(Q.real(gen), assumptions=assume):
#        raise NotImplementedError("can't solve inequalities with absolute values of a complex variable")

    def _bottom_up_scan(expr):
        exprs = []

        if expr.is_Add or expr.is_Mul:
            op = expr.__class__

            for arg in expr.args:
                _exprs = _bottom_up_scan(arg)

                if not exprs:
                    exprs = _exprs
                else:
                    args = []

                    for expr, conds in exprs:
                        for _expr, _conds in _exprs:
                            args.append((op(expr, _expr), conds + _conds))

                    exprs = args
        elif expr.is_Pow:
            n = expr.exp

            if not n.is_Integer or n < 0:
                raise ValueError(
                    "only non-negative integer powers are allowed")

            _exprs = _bottom_up_scan(expr.base)

            for expr, conds in _exprs:
                exprs.append((expr**n, conds))
        elif isinstance(expr, Abs):
            _exprs = _bottom_up_scan(expr.args[0])

            for expr, conds in _exprs:
                exprs.append(( expr, conds + [Ge(expr, 0)]))
                exprs.append((-expr, conds + [Lt(expr, 0)]))
        else:
            exprs = [(expr, [])]

        return exprs

    exprs = _bottom_up_scan(expr)

    mapping = {'<': '>', '<=': '>='}
    inequalities = []

    for expr, conds in exprs:
        if rel not in mapping.keys():
            expr = Relational( expr, 0, rel)
        else:
            expr = Relational(-expr, 0, mapping[rel])

        inequalities.append([expr] + conds)
    add_comment("Rewrite the inequalities as")
    for inequality in inequalities:
        add_exp(inequality)
    return reduce_rational_inequalities(inequalities, gen, assume)


def reduce_abs_inequalities(exprs, gen, assume=True):
    """Reduce a system of inequalities with nested absolute values.

    Examples
    ========

    >>> from sympy import Q, Abs
    >>> from sympy.abc import x
    >>> from sympy.solvers.inequalities import reduce_abs_inequalities

    >>> reduce_abs_inequalities([(Abs(3*x - 5) - 7, '<'),
    ... (Abs(x + 25) - 13, '>')], x, assume=Q.real(x))
    And(-2/3 < x, Or(x < -38, x > -12), x < 4)

    >>> reduce_abs_inequalities([(Abs(x - 4) + Abs(3*x - 5) - 7, '<')], x,
    ... assume=Q.real(x))
    And(1/2 < x, x < 4)

    See Also
    ========
    reduce_abs_inequality
    """
    return And(*[ reduce_abs_inequality(expr, rel, gen, assume) for expr, rel in exprs ])


def _solve_inequality(ie, s):
    """ A hacky replacement for solve, since the latter only works for
        univariate inequalities. """
    if not ie.rel_op in ('>', '>=', '<', '<='):
        raise NotImplementedError
    expr = ie.lhs - ie.rhs
    try:
        p = Poly(expr, s)
    except PolynomialError:
        raise NotImplementedError
    if p.degree() != 1:
        raise NotImplementedError('%s' % ie)
    a, b = p.all_coeffs()
    if a.is_positive:
        return ie.func(s, -b/a)
    elif a.is_negative:
        return ie.func(-b/a, s)
    else:
        raise NotImplementedError


# tests that ineq is in the form a*sqrt(f(x)) REL b
def is_sqrt_ineq(ineq, symbol):
    ineq = simplify(ineq)
    if ineq.func in [StrictGreaterThan, StrictLessThan, GreaterThan, LessThan]:
        a, b, f = Wild("a"), Wild("b"), Wild("f")
        rel = ineq.func
        m = ineq.match(rel(a*sqrt(f), b))
        if not m is None and m[a] != 0 and not m[a].has(symbol) and not m[b].has(symbol) and m[f].has(symbol):
            return m[a], m[b], m[f], rel, symbol
    return None


# tests that ineq is in the form c*log(a, f(x)) REL b
def is_log_ineq(ineq, symbol):
    ineq = simplify(ineq)
    if ineq.func in [StrictGreaterThan, StrictLessThan, GreaterThan, LessThan]:
        rel = ineq.func
        b = ineq.args[1]
        if ineq.args[0].func is log:
            f = ineq.args[0].args[0]
            if len(ineq.args[0].args) == 2:
                a = ineq.args[0].args[1]
            else:
                a = S.Exp1
            if f.has(symbol) and not a.has(symbol) and not b.has(symbol):
                return a, b, 1, f, rel, symbol
        elif ineq.args[0].func is Mul and ineq.args[0].args[1].func is log:
            c = ineq.args[0].args[0]
            f = ineq.args[0].args[1].args[0]
            if len(ineq.args[0].args[1].args) == 2:
                a = ineq.args[0].args[1].args[1]
            else:
                a = S.Exp1
            if f.has(symbol) and not a.has(symbol) and not b.has(symbol) and not c.has(symbol):
                return a, b, c, f, rel, symbol
    return None


# tests that ineq is in the form log(a, f(x)) REL log(b, g(x))
def is_log_log_ineq(ineq, symbol):
    ineq = simplify(ineq)
    if ineq.func in [StrictGreaterThan, StrictLessThan, GreaterThan, LessThan]:
        rel = ineq.func
        if ineq.args[0].func is log and ineq.args[1].func is log:
            f = ineq.args[0].args[0]
            g = ineq.args[1].args[0]
            if len(ineq.args[0].args) == 2:
                a = ineq.args[0].args[1]
            else:
                a = S.Exp1
            if len(ineq.args[1].args) == 2:
                b = ineq.args[1].args[1]
            else:
                b = S.Exp1
            if f.has(symbol) and g.has(symbol) and not a.has(symbol) and not b.has(symbol):
                return a, b, f, g, rel, symbol
    return None


# solve ineq is in the form log(a, f(x)) REL b
def solve_log_ineq(log_ineq_params):
    a, b, c, f, rel, symbol = log_ineq_params
    ineq = rel(c*log(f, a), b)
    add_comment("Solve the inequality")
    add_exp(ineq)
    if c > 0 and c != 1:
        add_comment("Rewrite it as")
        b, c = b / c, 1
        ineq = rel(log(f, a), b)
        add_exp(ineq)
    if c < 0:
        add_comment("Rewrite it as")
        b, c, rel = b / c, 1, corel(rel)
        ineq = rel(log(f, a), b)
        add_exp(ineq)
    elif c != 1:
        raise NotImplementedError("can't reduce %s" % ineq)

    if a > 1:
        add_comment("The base of log is greater than 1 therefore we have")
        ineq = rel(f, Pow(a, b, evaluate=False))
        add_exp(ineq)
    elif 0 < a < 1:
        add_comment("The base of log is less than 1 therefore we have")
        ineq = corel(rel)(f, Pow(a, b, evaluate=False))
        add_exp(ineq)
    else:
        raise NotImplementedError("can't reduce %s" % ineq)
    add_comment("And we have a restriction")
    dom = StrictGreaterThan(f, 0)
    add_exp(dom)
    return reduce_inequalities([ineq, dom], True, [symbol])


# solve ineq is in the form log(a, f(x)) REL log(b, g(x))
def solve_log_log_ineq(log_log_ineq_params):
    a, b, f, g, rel, symbol = log_log_ineq_params
    ineq = rel(log(f, a), log(g, b))
    add_comment("Solve the inequality")
    add_exp(ineq)
    dom1 = StrictGreaterThan(f, 0)
    dom2 = StrictGreaterThan(g, 0)
    if a != b:
        add_comment("Rewrite it as")
        if simplify(log(b, a)).is_Integer:
            f = Pow(f, log(b, a), evaluate=False)
            a = b
        else:
            g = Pow(g, log(a, b), evaluate=False)
            b = a
        ineq = rel(log(f, a), log(g, b))
        add_exp(ineq)
    if a > 1:
        add_comment("The base of log is greater than 1 therefore we have")
        ineq = rel(f, g)
        add_exp(ineq)
    elif 0 < a < 1:
        add_comment("The base of log is less than 1 therefore we have")
        ineq = corel(rel)(f, g)
        add_exp(ineq)
    else:
        raise NotImplementedError("can't reduce %s" % ineq)
    add_comment("And we have restrictions")
    add_exp(dom1)
    add_exp(dom2)
    return reduce_inequalities([ineq, dom1, dom2], True, [symbol])


# tests that ineq is in the form a*trig(f(x)) REL b
def is_trig_ineq(ineq, symbol):
    ineq = simplify(ineq)
    if ineq.func in [StrictGreaterThan, StrictLessThan, GreaterThan, LessThan]:
        a, b, f = Wild("a"), Wild("b"), Wild("f")
        for trig in [sin, cos, tan, cot]:
            rel = ineq.func
            m = ineq.match(rel(a*trig(f), b))
            if not m is None and m[a] != 0 and not m[a].has(symbol) and not m[b].has(symbol) and m[f].has(symbol):
                return m[a], m[b], m[f], rel, trig, symbol
    return None


def solve_trig_help(left, right, rel, f, symbol):
    from sympy.solvers.solvers import solve
    add_comment("We have")
    if rel in [StrictGreaterThan, StrictLessThan]:
        add_exp(And(StrictLessThan(left, f), StrictLessThan(f, right)))
    else:
        add_exp(And(LessThan(left, f), LessThan(f, right)))
    if symbol - f != 0:
        left = solve(Eq(f, left), symbol)
        if len(left) != 1:
            raise NotImplementedError()
        left = left[0]
        right = solve(Eq(f, right), symbol)
        if len(right) != 1:
            raise NotImplementedError()
        right = right[0]
        add_comment("Therefore")
        if rel in [StrictGreaterThan, StrictLessThan]:
            add_exp(And(StrictLessThan(left, symbol), StrictLessThan(symbol, right)))
        else:
            add_exp(And(LessThan(left, symbol), LessThan(symbol, right)))
    if rel in [StrictGreaterThan, StrictLessThan]:
        interval = Interval(left, right)
    else:
        interval = Interval(left, right, False, False)
    return interval


# solves a*sqrt(f(x)) REL b
def solve_sqrt_ineq(trig_ineq_params):
    a, b, f, rel, symbol = trig_ineq_params
    c = b / a
    add_comment("Solve the inequality")
    add_exp(rel(a * sqrt(f), b))
    if a != 1:
        if a < 0:
            rel = corel(rel)
        add_comment("Rewrite this equations as")
        add_exp(rel(sqrt(f), c))

    # sqrt(f(x)) < c <= 0 or # sqrt(f(x)) <= c < 0.
    if (rel is StrictLessThan and c <= 0) or (rel is LessThan and c < 0):
        add_comment("There is no solution because the values of sqrt are non-negative")
        return S.EmptySet

    add_comment("Square the both sides of the inequality to eliminate the radical sign")
    ineq = rel(f, pow(c, 2))
    add_exp(ineq)
    dom = GreaterThan(f, 0)
    add_comment("This step is correct if")
    add_exp(dom)
    return reduce_inequalities([ineq, dom], True, [symbol])


def solve_trig_ineq(trig_ineq_params):
    a, b, f, rel, trig, symbol = trig_ineq_params
    c = b / a
    k = Dummy("k")
    add_comment("Solve the inequality")
    add_exp(rel(a * trig(f), b))
    add_comment("This inequality is triginometric")
    if a < 0:
        rel = corel(rel)
    if trig in [sin, cos] and (
            (rel is StrictLessThan and c <= -1) or
            (rel is LessThan and c < -1) or
            (rel is StrictGreaterThan and c >= 1) or
            (rel is GreaterThan and c > 1)):
        add_comment("There is no solution")
        return S.EmptySet
    elif trig in [sin, cos] and (
            (rel is StrictLessThan and c > 1) or
            (rel is LessThan and c >= 1) or
            (rel is StrictGreaterThan and c < -1) or
            (rel is GreaterThan and c <= -1)):
        add_comment("Any number is a solution of this equation")
        return Interval(-inf, inf)
    elif trig is sin:
        if rel in [LessThan, StrictLessThan]:
            return solve_trig_help(2*pi*k - pi - asin(c), 2*pi*k + asin(c), rel, f, symbol)
        if rel in [GreaterThan, StrictGreaterThan]:
            return solve_trig_help(2*pi*k + asin(c), 2*pi*k + pi - asin(c), rel, f, symbol)
    elif trig is cos:
        if rel in [LessThan, StrictLessThan]:
            return solve_trig_help(2*pi*k + acos(c), 2*pi*k + 2*pi - acos(c), rel, f, symbol)
        if rel in [GreaterThan, StrictGreaterThan]:
            return solve_trig_help(2*pi*k - acos(c), 2*pi*k + acos(c), rel, f, symbol)
    elif trig is tan:
        if rel in [LessThan, StrictLessThan]:
            return solve_trig_help(-pi/2 + pi*k, pi*k + atan(c), rel, f, symbol)
        if rel in [GreaterThan, StrictGreaterThan]:
            return solve_trig_help(pi*k + atan(c), pi/2 + pi*k, rel, f, symbol)
    elif trig is cot:
        if rel in [LessThan, StrictLessThan]:
            return solve_trig_help(pi*k + acot(c), pi + pi*k, rel, f, symbol)
        if rel in [GreaterThan, StrictGreaterThan]:
            return solve_trig_help(pi*k, pi*k + acot(c), rel, f, symbol)


def reduce_inequalities(inequalities, assume=True, symbols=[]):
    """Reduce a system of inequalities with rational coefficients.

    Examples
    ========

    >>> from sympy import Q, sympify as S
    >>> from sympy.abc import x, y
    >>> from sympy.solvers.inequalities import reduce_inequalities

    >>> reduce_inequalities(S(0) <= x + 3, Q.real(x), [])
    x >= -3

    >>> reduce_inequalities(S(0) <= x + y*2 - 1, True, [x])
    -2*y + 1 <= x
    """
    if not hasattr(inequalities, '__iter__'):
        inequalities = [inequalities]

    if len(inequalities) == 1 and len(symbols) == 1 \
            and inequalities[0].is_Relational:
        try:
            return _solve_inequality(inequalities[0], symbols[0])
        except NotImplementedError:
            pass

    poly_part, abs_part, extra_assume = {}, {}, []

    if len(inequalities) == 1 and len(symbols) == 1:
        ineq = inequalities[0]
        symbol = symbols[0]
        trig_ineq_params = is_trig_ineq(ineq, symbol)
        if trig_ineq_params is not None:
            return solve_trig_ineq(trig_ineq_params)
        sqrt_ineq_params = is_sqrt_ineq(ineq, symbol)
        if sqrt_ineq_params is not None:
            return solve_sqrt_ineq(sqrt_ineq_params)
        log_ineq_params = is_log_ineq(ineq, symbol)
        if log_ineq_params is not None:
            return solve_log_ineq(log_ineq_params)
        log_log_ineq_params = is_log_log_ineq(ineq, symbol)
        if log_log_ineq_params is not None:
            return solve_log_log_ineq(log_log_ineq_params)

    for inequality in inequalities:
        if isinstance(inequality, bool):
            if inequality is False:
                return False
            else:
                continue

        if isinstance(inequality, AppliedPredicate):
            extra_assume.append(inequality)
            continue

        if inequality.is_Relational:
            expr, rel = inequality.lhs - inequality.rhs, inequality.rel_op
        else:
            expr, rel = inequality, '=='

        gens = expr.atoms(Symbol)

        if not gens:
            return False
        elif len(gens) == 1:
            gen = gens.pop()
        else:
            raise NotImplementedError(
                "only univariate inequalities are supported")

        components = expr.find(lambda u: u.is_Function)

        if not components:
            if gen in poly_part:
                poly_part[gen].append((expr, rel))
            else:
                poly_part[gen] = [(expr, rel)]
        else:
            if all(isinstance(comp, Abs) for comp in components):
                if gen in abs_part:
                    abs_part[gen].append((expr, rel))
                else:
                    abs_part[gen] = [(expr, rel)]
            else:
                raise NotImplementedError("can't reduce %s" % inequalities)

    extra_assume = And(*extra_assume)

    if assume is not None:
        assume = And(assume, extra_assume)
    else:
        assume = extra_assume

    poly_reduced = []
    abs_reduced = []

    for gen, exprs in poly_part.items():
        poly_reduced.append(reduce_rational_inequalities([exprs], gen, assume))

    for gen, exprs in abs_part.items():
        abs_reduced.append(reduce_abs_inequalities(exprs, gen, assume))

    return And(*(poly_reduced + abs_reduced))
