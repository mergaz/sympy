"""Tools for solving inequalities and systems of inequalities. """

from __future__ import print_function, division

from sympy.core import Symbol, Interval
from sympy.core.relational import Relational, Eq, Ge, Lt, GreaterThan
from sympy.core.singleton import S

from sympy.assumptions import ask, AppliedPredicate, Q
from sympy.functions import re, im, Abs
from sympy.logic import And
from sympy.polys import Poly, PolynomialError, parallel_poly_from_expr
from sympy.polys.polyroots import roots
from sympy.printing.latex import latex
from sympy.utilities.solution import add_comment, add_eq, add_exp


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
            add_comment("The have the following solution set")
            add_exp(r)
            result = result.intersect(r)
        if len(_eqs) > 1:
            add_comment("Finally we have the following solution set")
            add_exp(result)
        rslt = rslt.union(result)
    if len(eqs) > 1:
        add_comment("Thus we have the following solution set")
        add_exp(result)
    return result


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

            if not (domain.is_ZZ or domain.is_QQ):
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
