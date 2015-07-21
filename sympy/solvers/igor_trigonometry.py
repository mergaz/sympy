from sympy.core import (C, S, Add, Symbol, Wild, Equality, Dummy, Basic,Expr, Mul, Pow)
from sympy.simplify import (simplify, collect, powsimp, posify, powdenest,
                            nsimplify, denom, logcombine, trigsimp)
from sympy.functions import (log, exp, LambertW, cos, sin, tan, cot, cosh,
                             sinh, tanh, coth, acos, asin, atan, acot, acosh,
                             asinh, atanh, acoth, Abs, sign, re, im, arg,
                             sqrt, atan2)

from sympy.core.numbers import ilcm, Float, pi

from sympy.utilities.solution import add_exp, add_eq, add_step, add_comment, start_subroutine, cancel_subroutine

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

def igor_trigonometry_formulas(f, fi,t):
#         n=f.find("-2*sin(2*x)*cos(2*x)/3")
#         if len(n)>0 :
#             f = f.replace("-2*sin(2*x)*cos(2*x)/3","-(2/3)*sin(2*x)*cos(2*x)")
#             ff=f.args
#             print(f.args)
#         return f
         fi_1 =  igor_arguments(f, fi,t)

         if fi!=fi_1:
             return fi_1

         n=f.find("cos(x+pi/4)")
         #n is set
         if len(n)>0 :
             f = f.replace("cos(x+pi/4)","(sqrt(2)*cos(x)/2 - sqrt(2)*sin(x)/2)")
             return f

         n=f.find("sin(2*x)")
         #n is set
         if len(n)>0 :
             f = f.replace("sin(2*x)","2*sin(x)*cos(x)")
             return f

         n=f.find("sin(3*x)")
         #n is set
         if len(n)>0 :
             f = f.replace("sin(3*x)","3*sin(x)-4*sin(x)**3")
             return f

         n=f.find("cos(3*x)")
         #n is set
         if len(n)>0 :
             f = f.replace("cos(3*x)","4*cos(x)**3-3*cos(x)")
             return f

         n=f.find("sin(4*x)")
         #n is set
         if len(n)>0 :
             f = f.replace("sin(4*x)","(2*cos(2*x)*sin(2*x))")
             print(f)
             return f

         n=f.find("sin(x)**2")
         if len(n)>0 :
             f = f.replace("sin(x)**2","(1-cos(2*x))/2")
             return f

         n=f.find("-cos(x)")
         n1 = f.find("1")
         if len(n)>0 and len(n1)>0:
             f = f.replace("-cos(x)","-2*sin(x/2)**2")
             f = f.replace("1","0")
             return f

         return fi

def igor_arguments(f, fi,t):

    A, B, X = Wild('A'), Wild('B'), Wild('X')
    m = fi.match(A*sin(X) + A*cos(X)  - B)
    #m = fi.match(A*sin(X) - B)

    #A, B, C, F, G, X = Wild("A"), Wild("B"), Wild("C"), Wild("F"), Wild("G"), Wild("X")
    #m = fi.match(A*sin(F) + B*sin(G) + C)
    #m = fi.match(A*sin(F)*B*sin(G) +A*cos(F)*B*cos(G)+ C)

    if not m is None:
      if m[A]!=0:
       m[A] = m[A]*sin(m[X])
       m[A] = simplify(m[A])
       m[B] = simplify(m[B])
       m[X] = simplify(m[X])
       if m[B].has("cos(x)-1"):
         m[B]=2*sin(m[X])**2
         fi=m[A]+m[B]
         return fi
      else:
        if m[B].has("-tan(x)+cot(x)"):
         m[B]=m[A]-2*pi*_k
         fi=m[B]
         return fi

    m = fi.match(A*sin(X)**6 + A*cos(X)**6  + B)
    if not m is None:
      m[B] = simplify(m[B])
      if m[B]!=0 and m[A]!=0:
        m[B]=m[B]+(S(5)/8)+(S(3)/8)*cos(4*x)
        fi=m[B]
        return fi

    A, B, X = Wild('A'), Wild('B'), Wild('X')
    m = fi.match(A*sin(X)*cos(B*X) + 1)
    if not m is None:
      m[A] = simplify(m[A])
      m[B] = simplify(m[B])
      m[X] = simplify(m[X])
      if m[A]==1 and m[B]==4:
        fi = m[X]+(-pi/2)+2*pi*t
        return fi


    A, B, C, D, X = Wild('A'), Wild('B'), Wild('C'),  Wild('D'),Wild('X')
    m = fi.match(A*sin(X) + sin(B*X) - C*cos(X) + D)
    if not m is None:
      m[A] = simplify(m[A])
      m[B] = simplify(m[B])
      m[C] = simplify(m[C])
      m[D] = simplify(m[D])
      m[X] = simplify(m[X])
      if m[C] == 3 and m[B]==2 and m[A]==-3:
          m[D] = m[D]-1
          add_comment('Rewrite the fourth term as')
          eq1 =  m[D] + sin(m[X])**2 + cos(m[X])**2
          add_exp(eq1)
          add_comment('Rewrite the equation as')
          eq2 = (sin(m[X])+cos(m[X]))**2 + 3*(sin(m[X])+cos(m[X])) + 2
          add_exp(eq2)
          add_comment('Finally the given equation write as')
          eq3 = sin(m[X])+cos(m[X]) - 1
          add_exp(eq3)
          fi = sin(m[X])+cos(m[X]) - 1
          return fi

    return fi



