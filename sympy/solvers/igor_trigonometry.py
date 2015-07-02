from sympy.core import (C, S, Add, Symbol, Wild, Equality, Dummy, Basic,Expr, Mul, Pow)
from sympy.simplify import (simplify, collect, powsimp, posify, powdenest,
                            nsimplify, denom, logcombine, trigsimp)
from sympy.functions import (log, exp, LambertW, cos, sin, tan, cot, cosh,
                             sinh, tanh, coth, acos, asin, atan, acot, acosh,
                             asinh, atanh, acoth, Abs, sign, re, im, arg,
                             sqrt, atan2)

def igor_contains_trig(f, symbols):
    """
    Returns True if f contains sin, cos, tan or cot
    """
    result = []
    if f.args:
        for a in f.args:
            if contains_trig(a, symbols):
                return True
        if f.func in [sin, cos, tan, cot]:
            free = f.free_symbols
            if any(s in free for s in symbols):
                return True
    return False

def igor_is_sin_cos(gens):
    for g in gens:
        if not g.func in [sin, cos]:
           return False
    return True

def igor_trigonometry_formulas(f, fi):
#         n=f.find("-2*sin(2*x)*cos(2*x)/3")
#         if len(n)>0 :
#             f = f.replace("-2*sin(2*x)*cos(2*x)/3","-(2/3)*sin(2*x)*cos(2*x)")
#             ff=f.args
#             print(f.args)
#         return f

         n=f.find("cos(x+pi/4)")
         #n is set
         if len(n)>0 :
             f = f.replace("cos(x+pi/4)","(sqrt(2)*cos(x)/2 - sqrt(2)*sin(x)/2)")

         n=f.find("sin(2*x)")
         #n is set
         if len(n)>0 :
             f = f.replace("sin(2*x)","2*sin(x)*cos(x)")

         n=f.find("sin(3*x)")
         #n is set
         if len(n)>0 :
             f = f.replace("sin(3*x)","3*sin(x)-4*sin(x)**3")

         n=f.find("cos(3*x)")
         #n is set
         if len(n)>0 :
             f = f.replace("cos(3*x)","4*cos(x)**3-3*cos(x)")

         n=f.find("sin(4*x)")
         #n is set
         if len(n)>0 :
             f = f.replace("sin(4*x)","(2*cos(2*x)*sin(2*x))")
             print(f)

         n=f.find("sin(x)**2")
         if len(n)>0 :
             f = f.replace("sin(x)**2","(1-cos(2*x))/2")

         n=f.find("-cos(x)")
         n1 = f.find("1")
         if len(n)>0 and len(n1)>0:
             f = f.replace("-cos(x)","-2*sin(x/2)**2")
             f = f.replace("1","0")
             return f

         return f #igor_arguments(f, fi)

def igor_arguments(f, fi):

    A, B, X = Wild('A'), Wild('B'), Wild('X')
    m = fi.match(A*sin(X)**6 + A*cos(X)**6  - B)
    m = fi.match(A*sin(X) - B)
    #A, B, C, F, G, X = Wild("A"), Wild("B"), Wild("C"), Wild("F"), Wild("G"), Wild("X")
    #m = fi.match(A*sin(F) + B*sin(G) + C)
    #m = fi.match(A*sin(F)*B*sin(G) +A*cos(F)*B*cos(G)+ C)


    if m[A]!=0:
     m[A] = m[A]*sin(m[X])
     m[A] = simplify(m[A])
     m[B] = simplify(m[B])
     m[X] = simplify(m[X])
     if m[B].has("cos(x)-1"):
        m[B]=2*sin(m[X])**2
        fi=m[A]+m[B]
     return fi

    A, B, X = Wild('A'), Wild('B'), Wild('X')
    m = fi.match(A*cos(X) + B*cos(2*X) + A*cos(3*X))

    eq1 = m[B] * sin(2*m[X])
    add_exp(eq1)
    eq2 = m[A] * sin(m[X]) + m[A] * sin(3*m[X])
    add_exp(eq2)


def igor_solver_edit(fi):

    A, B, C, X = Wild('A'), Wild('B'), Wild('C'), Wild('X')
    m = fi.match(A*sin(2*X)*cos(2*X))
    #A, B, C, F, G, X = Wild("A"), Wild("B"), Wild("C"), Wild("F"), Wild("G"), Wild("X")
    #m = fi.match(A*sin(F) + B*sin(G) + C)
    #m = fi.match(A*sin(F)*B*sin(G) +A*cos(F)*B*cos(G)+ C)

    m[A] = simplify(m[A])
    m[B] = simplify(m[B])
    m[X] = simplify(m[X])
    return fi
