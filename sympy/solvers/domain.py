"""
Determine domain of function.
"""

from __future__ import print_function, division
from sympy.core.basic import preorder_traversal
from sympy.core import S, Add, Symbol, Equality, Dummy, Expr, Mul, Pow, Wild, expand
from sympy.core.singleton import S
from sympy.core.relational import GreaterThan, StrictLessThan
import sympy.solvers.solvers 
from sympy.solvers.inequalities import *
from sympy.simplify import (simplify, collect, powsimp, posify, powdenest, nsimplify, denom, logcombine, trigsimp)
from sympy.sets import Interval, Set
from sympy.sets.sets import FiniteSet, Union

def domain(eq, symbols=None):
    """
    Returns the domain of equality
    """
    def calc_denoms(denoms, symbol):
        result = Interval(S.NegativeInfinity, S.Infinity)
        for d in denoms:
            if not symbol in d.free_symbols:
                continue
            root = sympy.solvers.solve(d, symbol)
            if isinstance(root, list):
                for r in root:
                    if not r.is_complex:
                        result = result - FiniteSet(r)
            else:
                result = result - FiniteSet(root)
        return result

    def calc_roots(roots, symbol):
        result = Interval(S.NegativeInfinity, S.Infinity)
        for r in roots:
            if not symbol in r.free_symbols:
                continue
            interval = sympy.solvers.reduce_inequalities(StrictLessThan(r, 0), symbols=[symbol])
            #print('Interval', interval)
            if isinstance(interval, list):
                for it in interval:
                    if it is S.false or it is []:
                        result = S.EmptySet
                    elif it is S.true:
                        # nothing changes
                        pass
                    else:
                        result = result - it.as_set()
            elif interval is S.false or interval is []:
                result = S.EmptySet
            elif interval is S.true:
                # nothing changes
                pass
            else:
                result = result - interval.as_set()
        return result

    pot = preorder_traversal(eq)
    dens = set()
    for p in pot:
        den = denom(p)
        if den is S.One:
            continue
        for d in Mul.make_args(den):
            if len(d.free_symbols) > 0:
                dens.add(d)

    sqroots = set()
    for p in eq.atoms(Pow):
        if p.exp < 1 and p.exp > -1:
            sqroots.add(p.base)

    if symbols:
        if not isinstance(symbols, list):
            symbols = [symbols]
        rv = []
        for d in dens:
            free = d.free_symbols
            if any(s in free for s in symbols):
                rv.append(d)
        dens = set(rv)
        srf = []
        for sr in sqroots:
            free = sr.free_symbols
            if any(s in free for s in symbols):
                srf.append(sr)
        sqroots = set(srf)
    else:
        symbols = set()
        for d in dens:
            for free in d.free_symbols:
                symbols.add(free)
        for sr in sqroots:
            for free in sr.free_symbols:
                symbols.add(free)

    result = None
    
    if len(symbols) == 1:
        # one variable
        symbol = symbols.pop()
        result = calc_denoms(dens, symbol)
        result = result.intersect(calc_roots(sqroots, symbol))

    elif len(symbols) > 1:
        # multiple variables
        result = {}
        for symbol in symbols:
            res = calc_denoms(dens, symbol)
            res = res.intersect(calc_roots(sqroots, symbol))
            result[symbol] = res
    else:
        # no variables
        result = Interval(S.NegativeInfinity, S.Infinity)

    #print('Domain', result)
    return result

