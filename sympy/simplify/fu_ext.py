
'''
sympy.simplify.fu extensions

TRx1 - sin and cos of 3x angle
TRx2 - replace sin by cos
TRx3 - replace cos by sin
TRx4 - reduce sin power of 2 (increase angle)
TRx5 - reduce sin power of 3 (increase angle)
TRx6 - reduce sin power of 4 (increase angle)
TRx7 - reduce sin power of 5 (increase angle)
TRx8 - reduce cos power of 3 (increase angle)
TRx9 - reduce cos power of 4 (increase angle)
TRx10 - sin,cos product to sum
TRx11 - cosine of double angle (increase power)
TRx11i - reversed TRx11
TRx12 - cosine of half angle (increase angle)
TRx12i - reversed TRx12
TRx13 - sine of half angle (increase angle)
TRx13i - reversed TRx13
TRx14 - tangent of half angle (increase angle)
TRx15 - sine of double angle to sin*cos product
TRx16 - Pythagorean identity
'''
from sympy.simplify.simplify import bottom_up
from sympy.functions.elementary.trigonometric import cos, sin, sqrt
from sympy.core.mul import Mul
from sympy.core.power import Pow
from sympy.core import Wild

def TRx1(rv):
    '''
    sin(3*x) -> 3*sin(x)-4*sin(x)**3
    cos(3*x) -> 4*cos(x)**3-3*cos(x)
    '''
    def f(rv):
        if rv.func is sin:
            a=rv.args[0]
            return 3*sin(a/3)-4*sin(a/3)**3
        elif rv.func is cos:
            a=rv.args[0]
            return 4*cos(a/3)**3-3*cos(a/3)
        return rv
    return bottom_up(rv, f)

def TRx2(rv):
    '''
    sin(x) -> sqrt(1-cos(x)**2)
    '''
    def f(rv):
        if rv.func is sin:
            a=rv.args[0]
            return sqrt(1-cos(a)**2)
        return rv
    return bottom_up(rv, f)

def TRx3(rv):
    '''
    cos(x) -> sqrt(1-sin(x)**2)
    '''
    def f(rv):
        if rv.func is cos:
            a=rv.args[0]
            return sqrt(1-sin(a)**2)
        return rv
    return bottom_up(rv, f)

def TRx4(rv):
    '''
    sin(x)**2 -> (1-cos(2*x))/2
    '''
    def f(rv):
        if (rv.is_Pow and rv.base.func is sin and rv.exp == 2):
            a=rv.args[0].args[0]
            return (1-cos(2*a))/2
        return rv
    return bottom_up(rv, f)

def TRx5(rv):
    '''
    sin(x)**3 -> (3*sin(x)-sin(3*x))/4
    '''
    def f(rv):
        if (rv.is_Pow and rv.base.func is sin and rv.exp == 3):
            a=rv.args[0].args[0]
            return (3*sin(a)-sin(3*a))/4
        return rv
    return bottom_up(rv, f)

def TRx6(rv):
    '''
    sin(x)**4 -> (3-4*cos(2*x)+cos(4*x))/8
    '''
    def f(rv):
        if (rv.is_Pow and rv.base.func is sin and rv.exp == 4):
            a=rv.args[0].args[0]
            return (3-4*cos(2*a)+cos(4*a))/8
        return rv
    return bottom_up(rv, f)

def TRx7(rv):
    '''
    sin(x)**5 -> (10*sin(x)-5*sin(3*x)+sin(5*x))/16
    '''
    def f(rv):
        if (rv.is_Pow and rv.base.func is sin and rv.exp == 5):
            a=rv.args[0].args[0]
            return (10*sin(a)-5*sin(3*a)+sin(5*a))/16
        return rv
    return bottom_up(rv, f)

def TRx8(rv):
    '''
    cos(x)**3 -> (3*cos(x)+cos(3*x))/4
    '''
    def f(rv):
        if (rv.is_Pow and rv.base.func is cos and rv.exp == 3):
            a=rv.args[0].args[0]
            return (3*cos(a)+cos(3*a))/4
        return rv
    return bottom_up(rv, f)

def TRx9(rv):
    '''
    cos(x)**4 -> (3+4*cos(2*x)+cos(4*x))/8
    '''
    def f(rv):
        if (rv.is_Pow and rv.base.func is cos and rv.exp == 4):
            a=rv.args[0].args[0]
            return (3+4*cos(2*a)+cos(4*a))/8
        return rv
    return bottom_up(rv, f)

def TRx10(rv):
    '''
    cos(a)*sin(b) -> (sin(a+b)-sin(a-b))/2
    sin(a)*cos(b) -> (sin(a+b)+sin(a-b))/2
    '''
    def f(rv):
        if rv.is_Mul:
            A=rv.args[0]
            B=rv.args[1]
            if A.func is cos and B.func is sin:
                a=A.args[0]
                b=B.args[0]
                return (sin(a+b)-sin(a-b))/2
            elif A.func is sin and B.func is cos:
                a=A.args[0]
                b=B.args[0]
                return (sin(a+b)+sin(a-b))/2
        return rv
    return f(rv)

def TRx11(rv):
    '''
    cos(x) -> cos(x/2)**2-sin(x/2)**2
    '''
    def f(rv):
        if rv.func is cos:
            a=rv.args[0]
            return cos(a/2)**2-sin(a/2)**2
        return rv
    return bottom_up(rv, f)

def TRx11i(rv):
    '''
    cos(x)**2-sin(x)**2 -> cos(2*x)
    '''
    def f(rv):
        A, C, F, G = Wild("A"), Wild("C"), Wild("F"), Wild("G")
        m = rv.match(A*cos(F)**2 - A*sin(F)**2)
        if m:
            return m[A]*cos(2*m[F])
        return rv
    return bottom_up(rv, f)


def TRx12(rv):
    '''
    cos(x/2) -> sqrt((1+cos(x))/2)
    '''
    def f(rv):
        if rv.func is cos:
            a=rv.args[0]
            return sqrt((1-cos(2*a))/2)
        return rv
    return bottom_up(rv, f)

def TRx12i(rv):
    '''
    cos(x) -> 2*cos(x/2)**2-1
    '''
    def f(rv):
        if rv.func is cos:
            a=rv.args[0]
            return 2*cos(a/2)**2-1
        return rv
    return bottom_up(rv, f)

def TRx13(rv):
    '''
    sin(x/2) -> sqrt((1-cos(x))/2)
    '''
    def f(rv):
        if rv.func is sin:
            a=rv.args[0]
            return sqrt((1-cos(a))/2)
        return rv
    return bottom_up(rv, f)

def TRx13i(rv):
    '''
    cos(x) -> 1-2*sin(x/2)**2
    '''
    def f(rv):
        if rv.func is cos:
            a=rv.args[0]
            return 1-2*sin(a/2)**2
        return rv
    return bottom_up(rv, f) 

def TRx14(rv):
    '''
    tan(x/2) -> sin(x)/(1+cos(x))
    (NB: cos(x/2) should not be zero!)
    '''
    def f(rv):
        if rv.func is tan:
            a=rv.args[0]
            return sin(a)/(1+cos(a))
        return rv
    return bottom_up(rv, f)

def TRx15(rv):
    '''
    sin(x) -> 2*sin(x/2)*cos(x/2)
    '''
    def f(rv):
        if rv.func is sin:
            a=rv.args[0]
            return 2*sin(a/2)*cos(a/2)
        return rv
    return bottom_up(rv, f)

def TRx16(rv):
    '''
    cos(x)**2+sin(x)**2 -> 1
    '''
    def f(rv):
        A, F, G= Wild("A"), Wild("F"), Wild("G")
        m = rv.match(A*cos(F)**2 + A*sin(F)**2 + G)
        if m:
            return m[A]+m[G]
        return rv
    return bottom_up(rv, f)