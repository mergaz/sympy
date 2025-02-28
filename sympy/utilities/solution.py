"""Make step-by-step solution. """

import gc, sys
from sympy.printing.latex import LatexPrinter
from sympy.printing.mathml import MathMLPrinter
from sympy.core import sympify
from sympy.core.relational import Eq
from sympy.utilities.solution_en import solution_comment_table_en
from sympy.utilities.solution_ru import solution_comment_table_ru

solution_list = []
comment_table = solution_comment_table_en()
printer = LatexPrinter()

def find_names(obj):
    frame = sys._getframe()
    for frame in iter(lambda: frame.f_back, None):
        frame.f_locals
    result = []
    for referrer in gc.get_referrers(obj):
        if isinstance(referrer, dict):
            for k, v in referrer.iteritems():
                if v is obj:
                    result.append(k)
    return result

def find_name(obj):
    frame = sys._getframe()
    for frame in iter(lambda: frame.f_back, None):
        frame.f_locals
    for referrer in gc.get_referrers(obj):
        if isinstance(referrer, dict):
            for k, v in referrer.iteritems():
                if v is obj and k != "variable":
                    return k
    return None

def set_comment_table(ct):
    global comment_table
    comment_table = ct

def add_comment(cm, *args):
    c = None
    if cm in comment_table.keys():
        c = comment_table[cm]
        c = c.format(*args)
    else:
        c = cm
        print "Not localized:", c
    solution_list.append('_' + c)
    
def add_step(variable):
    """Add a variable and its value into solution"""
    var = find_name(variable)
    try:
        r = printer._print(Eq(var, variable))
    except:
        r =  var + " = " + repr(variable)
    solution_list.append(r)

def add_eq(l, r):
    """Add an equality into solution"""
    e = Eq(l, r)
    try:
        e = printer._print(e)
    except:
        e = repr(e)
    #try:
    #    r = printer._print(r)
    #except:
    #    r = repr(r)
    solution_list.append(e)

    
def add_exp(exp):
    """Add an expression into solution"""
    print "-> " + str(exp)
    try:
        r = printer._print(exp)
    except:
        r = repr(exp)
    solution_list.append(r)

def reset_solution():
    """Clear previos solution"""
    print("New solution")
    del solution_list[:]

def start_subroutine(name):
    """Start add soubroutine steps"""
    print("Start subroutine", name)

def cancel_subroutine():
    """Cancel all steps of current subroutine"""
    print("Cancel subroutine")

def commit_subroutine():
    """Finish current subroutine"""
    print("Finish subroutine")

def last_solution():
    return solution_list

def setMathMLOutput():
    global printer
    printer = MathMLPrinter()

def setLatexOutput():
    global printer
    printer = LatexPrinter()
