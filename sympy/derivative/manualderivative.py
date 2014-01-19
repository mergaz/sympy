from sympy import *
from sympy.utilities.solution import *


def _table_derivative(func, arg, x):
    u = Symbol("x")
    if arg != x:
        add_comment("Use the chain rule")
    add_comment("The derivative of the function ")
    add_exp(func(u))
    add_comment("can be found in the derivative table and is equal to")
    add_exp(func(u).diff(u))
    if arg != x:
        derivative(arg, x)
        add_comment("Therefore we have")
        add_eq(Derivative(func(arg), x), func(arg).diff(x))


def derivative(f, x):
    add_comment("Find the derivative")
    add_exp(Derivative(f, x))
    if not x in f.free_symbols:
        add_comment("The function is constant therefore the derivative is 0")
    elif f == x:
        add_comment("The derivative of this function is equal to 1")
    elif f.func in [exp, sin, cos, tan, cot, sec, csc, asin, acos, atan, acot, sinh, cosh, tanh, coth, asinh,
                  acosh, atanh, acoth,]:
        _table_derivative(f.func, f.args[0], x)
    elif f.func == Add:
        add_comment("The function is a sum. Find the derivative of every summand.")
        result = 0
        for a in f.args:
            result += derivative(a, x)
        add_comment("Therefore the derivative of the sum is")
        add_eq(Derivative(f, x), result)
    elif f.func == Pow:
        base = f.args[0]
        power = f.args[1]
        if not x in base.free_symbols:
            u = Dummy()
            _table_derivative(Lambda(u, base**u), power, x)
        elif not x in power.free_symbols:
            u = Dummy()
            _table_derivative(Lambda(u, u**power), base, x)
        else:
            add_comment("Use the formula")
            g, h = symbols("g h", cls=Function)
            add_eq(Derivative(g(x)**h(x), x), g(x)**h(x) * (Derivative(g(x), x) * h(x) / g(x) + Derivative(h(x), x) * log(g(x))))
            if base != x:
                derivative(base, x)
            if power != x:
                derivative(power, x)
            add_comment("Finally we get")
            add_eq(Derivative(f, x), f.diff(x))
    elif f.func == log:
        if len(f.args) == 1:
            _table_derivative(f.func, f.args[0], x)
        elif len(f.args) == 2:
            u = Dummy()
            _table_derivative(Lambda(u, log(u, f.args[1])), f.args[0], x)
    elif f.func == Mul:
        num, den = f.as_numer_denom()
        if den != 1 and x in den.free_symbols and x in num.free_symbols:
            add_comment("Use the formula")
            g, h = symbols("g h", cls=Function)
            add_eq(Derivative(g(x)/h(x), x), (Derivative(g(x), x) * h(x) - g(x) * Derivative(h(x), x)) / h(x)**2)
            if num != x:
                derivative(num, x)
            if den != x:
                derivative(den, x)
            add_comment("Finally we get")
            add_eq(Derivative(f, x), f.diff(x))
        else:
            coeff = 1
            other = 1
            for arg in f.args:
                if not x in arg.free_symbols:
                    coeff *= arg
                else:
                    other *= arg
            if coeff != 1:
                add_comment("Move the constant outside the derivative sign")
                add_eq(Derivative(f, x), Mul(coeff, Derivative(other, x), evaluate=false))
                derivative(other, x)
                add_comment("Finally we get")
                add_eq(Derivative(f, x), f.diff(x))
            else:
                add_comment("Use the formula")
                g, h = symbols("g h", cls=Function)
                add_eq(Derivative(g(x) * h(x), x), Derivative(g(x), x) * h(x) + g(x) * Derivative(h(x), x))
                for arg in f.args:
                    derivative(arg, x)
                add_comment("Therefore we get")
                add_eq(Derivative(f, x), f.diff(x))

    return f.diff(x)