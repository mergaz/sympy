"""Solvers of systems of polynomial equations. """

from __future__ import print_function, division

from sympy.core import S
from sympy.core.mul import Mul
from sympy.core.power import Pow
from sympy.polys import Poly, groebner, roots
from sympy.polys.polyfuncs import symmetrize
from sympy.polys.polytools import parallel_poly_from_expr, factor, factor_list
from sympy.polys.polyerrors import (ComputationFailed,
    PolificationFailed, CoercionFailed)
from sympy.simplify import rcollect
from sympy.utilities import default_sort_key, postfixes

from sympy.utilities.solution import add_exp, add_eq, add_step, add_comment, start_subroutine, commit_subroutine, cancel_subroutine


class SolveFailed(Exception):
    """Raised when solver's conditions weren't met. """


def add_sol_(sol, gens):
    for i, s in enumerate(sol):
        add_eq(gens[i], s)
    add_comment("")

def soltodict(gens, sol):
    subs = dict()
    for i, sol in enumerate(sol):
        subs[gens[i]] = sol
    return subs

def solve_poly_system_(polys, optgens):
    if len(polys) == len(optgens) == 2:
        f, g = polys

        a, b = f.degree_list()
        c, d = g.degree_list()

        if a <= 2 and b <= 2 and c <= 2 and d <= 2:
            try:
                start_subroutine("Solve biquadratic")
                r = solve_biquadratic(f, g, optgens)
                commit_subroutine()
                return r
            except SolveFailed:
                cancel_subroutine()
                pass

    r = solve_generic(polys, optgens)
    return r


def solve_poly_system(seq, *gens, **args):
    """
    Solve a system of polynomial equations.

    Examples
    ========

    >>> from sympy import solve_poly_system
    >>> from sympy.abc import x, y

    >>> solve_poly_system([x*y - 2*y, 2*y**2 - x**2], x, y)
    [(0, 0), (2, -sqrt(2)), (2, sqrt(2))]
    """
    try:
        polys, opt = parallel_poly_from_expr(seq, *gens, **args)
    except PolificationFailed as exc:
        raise ComputationFailed('solve_poly_system', len(seq), exc)

    """
    ! this block leads to infinite recursion
    # Try to sum equations for simplification
    if len(polys) == 2:
        a = polys[0].coeff_monomial(1)
        b = polys[1].coeff_monomial(1)
        if a != 0 and b != 0 and len(factor_list(polys[0] - a/b * polys[1].as_expr())[1]) > 1:
            add_comment("Add the second equation multiplied by {} to the first equation", str(-a/b))
            sys = [polys[0] - a/b * polys[1].as_expr(), polys[1]]
            add_eq(sys[0].as_expr(), 0)
            add_eq(sys[1].as_expr(), 0)
            return solve_poly_system(sys, *gens, **args)
    """

    # Try to factor
    for i, p in enumerate(polys):
        fctrs = factor_list(p)
        if len(fctrs[1]) > 1:
            add_comment("Since")
            fp = fctrs[0]
            for fctr in fctrs[1]:
                fp = Mul(fp, Pow(fctr[0].as_expr(), fctr[1]), evaluate=False)
            add_eq(p.as_expr(), fp)
            add_comment("the system is equivalent to the following systems")
            syss = []
            for fctr in fctrs[1]:
                sys = []
                for j, q in enumerate(polys):
                    if i != j:
                        add_eq(q.as_expr(), 0)
                        sys.append(q)
                    else:
                        add_eq(fctr[0].as_expr(), 0)
                        sys.append(fctr[0])
                syss.append(sys)
                add_comment("")
            solution = []
            for sys in syss:
                add_comment("Solve the system")
                for t in sys:
                    add_eq(t.as_expr(), 0)
                solution += solve_poly_system(sys, *gens, **args)
            add_comment("Finally we have")
            for s in solution:
                add_sol_(s, gens)
            return solution


    try:
        # Try to symmetrize and use a simplifying substitution
        symmetrized = symmetrize_(polys, opt.gens)
        add_comment("Use the following substitution")
        for s in symmetrized[2].items():
            add_eq(s[0], s[1])
        add_comment("We have the following system")
        sys = []
        for s in symmetrized[0]:
            sys.append(Poly(s, symmetrized[1]))
            add_eq(s.as_expr(), 0)

        symmetrized_solution = solve_poly_system_(sys, symmetrized[1])
        add_comment("Use the back substitution")
        solution = []
        for s in symmetrized_solution:
            add_comment("Consider the solution")
            for i, r in enumerate(s):
                add_eq(symmetrized[1][i], r)
            add_comment("Solve the system of equation")
            sys = []
            for i, r in enumerate(s):
                q = symmetrized[2][symmetrized[1][i]]
                add_eq(q, r)
                q = q - r
                sys.append(Poly(q, opt.gens))
            solution += solve_poly_system_(sys, opt.gens)
        if len(symmetrized_solution) > 1:
            add_comment("Finally we have !!!")
            for s in solution:
                add_sol_(s, gens)
        return solution
    except:
        return solve_poly_system_(polys, opt.gens)

def solve_biquadratic(f, g, optgens):
    """Solve a system of two bivariate quadratic polynomial equations.

    Examples
    ========

    >>> from sympy.polys import Options, Poly
    >>> from sympy.abc import x, y
    >>> from sympy.solvers.polysys import solve_biquadratic
    >>> NewOption = Options((x, y), {'domain': 'ZZ'})

    >>> a = Poly(y**2 - 4 + x, y, x, domain='ZZ')
    >>> b = Poly(y*2 + 3*x - 7, y, x, domain='ZZ')
    >>> solve_biquadratic(a, b, NewOption)
    [(1/3, 3), (41/27, 11/9)]

    >>> a = Poly(y + x**2 - 3, y, x, domain='ZZ')
    >>> b = Poly(-y + x - 4, y, x, domain='ZZ')
    >>> solve_biquadratic(a, b, NewOption)
    [(-sqrt(29)/2 + 7/2, -sqrt(29)/2 - 1/2), (sqrt(29)/2 + 7/2, -1/2 + \
      sqrt(29)/2)]
    """
    G = groebner([f, g])

    if len(G) == 1 and G[0].is_ground:
        add_comment("This system has no solution")
        return []

    if len(G) != 2:
        raise SolveFailed

    p, q = G
    x, y = optgens

    add_comment("Rewrite the system as")
    add_eq(p.as_expr(), 0)
    add_eq(q.as_expr(), 0)

    p = Poly(p, x, expand=False)
    q = q.ltrim(-1)

    add_comment("Solve the first equation")
    add_eq(p.as_expr(), 0)
    p_roots = [ rcollect(expr, y) for expr in roots(p).keys() ]
    add_comment("Solve the second equation")
    add_eq(q.as_expr(), 0)
    q_roots = list(roots(q).keys())

    solutions = []
    for q_root in q_roots:
        add_comment("Consider the root")
        add_eq(y, q_root)
        for p_root in p_roots:
            add_comment("Since")
            add_eq(x, p_root)
            add_comment("We have")
            add_eq(x, p_root.subs(y, q_root, evaluate=False))
            solution = (p_root.subs(y, q_root), q_root)
            solutions.append(solution)

    if len(solutions) == 0:
        add_comment("Therefore there is no solution")
    else:
        add_comment("Therefore we have the following solutions of the system")
        for s in solutions:
            add_sol_(s, optgens)

    return sorted(solutions, key=default_sort_key)


def solve_generic(polys, optgens):
    """
    Solve a generic system of polynomial equations.

    Returns all possible solutions over C[x_1, x_2, ..., x_m] of a
    set F = { f_1, f_2, ..., f_n } of polynomial equations,  using
    Groebner basis approach. For now only zero-dimensional systems
    are supported, which means F can have at most a finite number
    of solutions.

    The algorithm works by the fact that, supposing G is the basis
    of F with respect to an elimination order  (here lexicographic
    order is used), G and F generate the same ideal, they have the
    same set of solutions. By the elimination property,  if G is a
    reduced, zero-dimensional Groebner basis, then there exists an
    univariate polynomial in G (in its last variable). This can be
    solved by computing its roots. Substituting all computed roots
    for the last (eliminated) variable in other elements of G, new
    polynomial system is generated. Applying the above procedure
    recursively, a finite number of solutions can be found.

    The ability of finding all solutions by this procedure depends
    on the root finding algorithms. If no solutions were found, it
    means only that roots() failed, but the system is solvable. To
    overcome this difficulty use numerical algorithms instead.

    References
    ==========

    .. [Buchberger01] B. Buchberger, Groebner Bases: A Short
    Introduction for Systems Theorists, In: R. Moreno-Diaz,
    B. Buchberger, J.L. Freire, Proceedings of EUROCAST'01,
    February, 2001

    .. [Cox97] D. Cox, J. Little, D. O'Shea, Ideals, Varieties
    and Algorithms, Springer, Second Edition, 1997, pp. 112

    Examples
    ========

    >>> from sympy.polys import Poly, Options
    >>> from sympy.solvers.polysys import solve_generic
    >>> from sympy.abc import x, y
    >>> NewOption = Options((x, y), {'domain': 'ZZ'})

    >>> a = Poly(x - y + 5, x, y, domain='ZZ')
    >>> b = Poly(x + y - 3, x, y, domain='ZZ')
    >>> solve_generic([a, b], NewOption)
    [(-1, 4)]

    >>> a = Poly(x - 2*y + 5, x, y, domain='ZZ')
    >>> b = Poly(2*x - y - 3, x, y, domain='ZZ')
    >>> solve_generic([a, b], NewOption)
    [(11/3, 13/3)]

    >>> a = Poly(x**2 + y, x, y, domain='ZZ')
    >>> b = Poly(x + y*4, x, y, domain='ZZ')
    >>> solve_generic([a, b], NewOption)
    [(0, 0), (1/4, -1/16)]
    """
    def _is_univariate(f):
        """Returns True if 'f' is univariate in its last variable. """
        for monom in f.monoms():
            if any(m > 0 for m in monom[:-1]):
                return False

        return True

    def _subs_root(f, gen, zero):
        """Replace generator with a root so that the result is nice. """
        p = f.as_expr({gen: zero})

        if f.degree(gen) >= 2:
            p = p.expand(deep=False)

        return p

    def _solve_reduced_system(system, gens, entry=False):
        """Recursively solves reduced polynomial systems. """
        if len(system) == len(gens) == 1:
            zeros = list(roots(system[0], gens[-1]).keys())
            add_comment("We have the following solutions")
            for zero in zeros:
                add_eq(gens[-1], zero)
            return [ (zero,) for zero in zeros ]

        basis = groebner(system, gens, polys=True)

        add_comment("Rewrite the system as")
        for f in basis:
            add_eq(f.as_expr(), 0)

        if len(basis) == 1 and basis[0].is_ground:
            add_comment("Hence the system has no solution")
            if not entry:
                return []
            else:
                return None

        univariate = list(filter(_is_univariate, basis))

        if len(univariate) == 1:
            f = univariate.pop()
        else:
            raise NotImplementedError("only zero-dimensional systems supported (finite number of solutions)")

        gens = f.gens
        gen = gens[-1]

        add_comment("Solve the equation")
        add_eq(f.as_expr(), 0)
        zeros = list(roots(f.ltrim(gen)).keys())

        if not zeros:
            add_comment("The system has no solution")
            return []

        if len(basis) == 1:
            add_comment("We have the following solutions")
            for zero in zeros:
                add_eq(gen, zero)
            return [ (zero,) for zero in zeros ]

        solutions = []

        add_comment("Substitute every root to the system")
        for zero in zeros:
            new_system = []
            new_gens = gens[:-1]

            for b in basis[:-1]:
                eq = _subs_root(b, gen, zero)

                if eq is not S.Zero:
                    new_system.append(eq)
            add_comment("Consider the root")
            add_eq(gen, zero)
            add_comment("We have")
            for eq in new_system:
                add_eq(eq, 0)
            for solution in _solve_reduced_system(new_system, new_gens):
                solutions.append(solution + (zero,))
            add_comment("We have the following solutions")
            for s in solutions:
                add_sol_(s, gens)

        return solutions

    try:
        result = _solve_reduced_system(polys, optgens, entry=True)
    except CoercionFailed:
        raise NotImplementedError

    if result is not None:
        return sorted(result, key=default_sort_key)
    else:
        return None


def is_symmetrize_(polys, gens):
    for p in polys:
        s = symmetrize(p, gens, formal=True)
        if s[1] != 0:
            return False
    return True

def subs_(polys, s):
    if type(polys) is list:
        result = []
        for p in polys:
            result.append(p.subs(s))
        return result
    if type(polys) is dict:
        result = dict()
        for p, q in polys.items():
            result[p] = q.subs(s)
        return result

def guess_subs_to_symm(polys, gens):
    """
    Returns a substitution for symmetrizing the system
    """
    if len(gens) != 2:
        return None
    for p in polys:
        a = p.coeff_monomial(gens[0])
        b = p.coeff_monomial(gens[1])
        if a != 0 and b != 0:
            ps = subs_(polys, {gens[0]: gens[0], gens[1]: a/b * gens[1]})
            if is_symmetrize_(ps, gens):
                return (ps, {gens[0]: gens[0], gens[1]: b/a * gens[1]})
    return None


def symmetrize_(polys, gens):
    """
    If system has a symmetric form, then use simplifying substitutions
    """
    gs = None
    if not is_symmetrize_(polys, gens):
        gs = guess_subs_to_symm(polys, gens)
        if gs is None:
            raise SolveFailed
        polys = gs[0]
    new_gens = set()
    subs = dict()
    new_sys = []
    for p in polys:
        s = symmetrize(p, gens, formal=True)
        new_p = Poly(s[0])
        new_sys.append(new_p)
        for sub in s[2]:
            if sub[0] in new_p.gens:
                subs[sub[0]] = sub[1]
                new_gens.add(sub[0])
    if len(gens) != len(new_gens):
        raise SolveFailed
    new_gens = list(new_gens)
    new_gens = sorted(new_gens, key=default_sort_key)
    if gs:
        subs = subs_(subs, gs[1])
    return [new_sys, new_gens, subs]

def solve_triangulated(polys, *gens, **args):
    """
    Solve a polynomial system using Gianni-Kalkbrenner algorithm.

    The algorithm proceeds by computing one Groebner basis in the ground
    domain and then by iteratively computing polynomial factorizations in
    appropriately constructed algebraic extensions of the ground domain.

    Examples
    ========

    >>> from sympy.solvers.polysys import solve_triangulated
    >>> from sympy.abc import x, y, z

    >>> F = [x**2 + y + z - 1, x + y**2 + z - 1, x + y + z**2 - 1]

    >>> solve_triangulated(F, x, y, z)
    [(0, 0, 1), (0, 1, 0), (1, 0, 0)]

    References
    ==========

    1. Patrizia Gianni, Teo Mora, Algebraic Solution of System of
    Polynomial Equations using Groebner Bases, AAECC-5 on Applied Algebra,
    Algebraic Algorithms and Error-Correcting Codes, LNCS 356 247--257, 1989

    """
    G = groebner(polys, gens, polys=True)
    G = list(reversed(G))

    domain = args.get('domain')

    if domain is not None:
        for i, g in enumerate(G):
            G[i] = g.set_domain(domain)

    f, G = G[0].ltrim(-1), G[1:]
    dom = f.get_domain()

    zeros = f.ground_roots()
    solutions = set([])

    for zero in zeros:
        solutions.add(((zero,), dom))

    var_seq = reversed(gens[:-1])
    vars_seq = postfixes(gens[1:])

    for var, vars in zip(var_seq, vars_seq):
        _solutions = set([])

        for values, dom in solutions:
            H, mapping = [], list(zip(vars, values))

            for g in G:
                _vars = (var,) + vars

                if g.has_only_gens(*_vars) and g.degree(var) != 0:
                    h = g.ltrim(var).eval(dict(mapping))

                    if g.degree(var) == h.degree():
                        H.append(h)

            p = min(H, key=lambda h: h.degree())
            zeros = p.ground_roots()

            for zero in zeros:
                if not zero.is_Rational:
                    dom_zero = dom.algebraic_field(zero)
                else:
                    dom_zero = dom

                _solutions.add(((zero,) + values, dom_zero))

        solutions = _solutions

    solutions = list(solutions)

    for i, (solution, _) in enumerate(solutions):
        solutions[i] = solution

    return sorted(solutions, key=default_sort_key)
