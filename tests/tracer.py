def tracefunc(frame, event, arg, indent=[0]):
    if 'sympy' not in frame.f_code.co_filename:
        return tracefunc
    parent = frame.f_back
    if event == "call":
        print '{}File "{}", line {}, in {}, called {}'.format(
            " " * indent[0], parent.f_code.co_filename,
            parent.f_lineno,
            parent.f_code.co_name,
            frame.f_code.co_name)
        indent[0] += 2
    elif event == "return":
        indent[0] -= 2
    return tracefunc


import sys

from sympy import Symbol, simplify, log

x = Symbol('x', real=True)
# var = log(x, 10)
var = log(x)
sys.settrace(tracefunc)

simplify(var)
