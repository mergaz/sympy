# content of conftest.py
import pytest
import sympy
from sympy.core.basic import Basic
from sympy.core.relational import StrictGreaterThan, StrictLessThan, GreaterThan, LessThan
import csv
from sympy.utilities.solution import last_solution, reset_solution
from datetime import datetime
import sys
import threading
try:
    import thread
except ImportError:
    import _thread as thread

from functools import wraps
import errno
import os
import signal
from copy import copy

DEBUG=False

class Tristate(object):
    def __init__(self, value=None):
        if value is None or value == True or value == False:
            self.value = value
        else:
            raise ValueError("Tristate value must be True, False, or None. Got %s" % type(value))
    def __eq__(self, other):
        return self.value is other
    def __ne__(self, other):
        return self.value is not other
    def __nonzero__(self):   # Python 3: __bool__()
        return self.value is True
    def __str__(self):
        return str(self.value)
    def __repr__(self):
        return "Tristate(%s)" % self.value

class TimeoutError(Exception):
    pass

"""
def timeout(seconds=10, error_message=os.strerror(errno.ETIME)):
    def decorator(func):
        def _handle_timeout(signum, frame):
            raise TimeoutError(error_message)
        def wrapper(*args, **kwargs):
            signal.signal(signal.SIGALRM, _handle_timeout)
            signal.alarm(seconds)
            try:
                result = func(*args, **kwargs)
            finally:
                signal.alarm(0)
            return result
        return wraps(func)(wrapper)
    return decorator
"""

class timeout:
    def __init__(self, seconds=1, error_message='Timeout'):
        self.seconds = seconds
        self.error_message = error_message
    def handle_timeout(self, signum, frame):
        raise TimeoutError(self.error_message)
    def __enter__(self):
        signal.signal(signal.SIGALRM, self.handle_timeout)
        signal.alarm(self.seconds)
    def __exit__(self, type, value, traceback):
        signal.alarm(0)

"""
def cdquit(fn_name):
    sys.stderr.flush()
    thread.interrupt_main()

def exit_after(s):
    def outer(fn):
        def inner(*args, **kwargs):
            timer = threading.Timer(s, cdquit, fn.__name__)
            timer.start()
            try:
                result = fn(*args, **kwargs)
            finally:
                timer.cancel()
            return result
        return inner
    return outer
"""

"""
@timeout(5)
def processor(func, arguments):
    return func(*arguments)
"""

def equal(A, B):
    A = sympy.simplify(A)
    B = sympy.simplify(B)
    if DEBUG: print A, B 
    if DEBUG: print type(A), type(B)
    if A == B:
        if DEBUG: print 'Ok'
        return Tristate(True)
    if type(A) is type(B):
        if isinstance(A, Basic):
            if A.is_Boolean:
                # And, Or, Not
                if len(A.args) == len(B.args):
                    counter = 0
                    args2 = list(B.args)
                    for arg in A.args:
                        for arg2 in args2:
                            if equal(arg, arg2) == True:
                                args2.remove(arg2)
                                if DEBUG: print 'Remove equal pair', arg, arg2
                                counter += 1
                                break
                    if counter == len(A.args):
                        return Tristate(True)
                    else:
                        if DEBUG: print '===] ', A.args, args2
                        return Tristate(False)
            elif A.is_Relational:
                # Gt, Lt...
                if len(A.args) == len(B.args):
                    for ind in range(len(A.args)):
                        arg1 = A.args[ind]
                        arg2 = B.args[ind]
                        res = equal(arg1, arg2)
                        if res is not True:
                            if DEBUG: print 'Pair not equal', arg1, arg2
                            return res
                    return Tristate(True)
                pass
            elif A.is_Float:
                if DEBUG: print 'Float:', A, B, A - B, sympy.Abs(A - B) < 0.001
                return Tristate(sympy.Abs(A - B) < 0.001)
        elif isinstance(A, list):
            counter = 0
            args2 = list(B)
            for arg1 in A:
                for arg2 in args2:
                    if equal(arg1, arg2):
                        args2.remove(arg2)
                        counter += 1
                        break
            # test for exact equality
            if len(A) == len(B) == counter:
                return Tristate(True)
            # test for partial equality
            elif counter > 0:
                return Tristate(None)
            else:
                return Tristate(False)
    else:
        if isinstance(A, Basic) and isinstance(B, Basic):
            if A.is_Relational and B.is_Relational and len(A.args)==2 and len(B.args)==2:
                if isinstance(A, StrictLessThan) and isinstance(B, StrictGreaterThan):
                    return equal(A.args[0], B.args[1]) and equal(A.args[1], B.args[0])
                elif isinstance(A, StrictGreaterThan) and isinstance(B, StrictLessThan):
                    return equal(A.args[0], B.args[1]) and equal(A.args[1], B.args[0])
                elif isinstance(A, LessThan) and isinstance(B, GreaterThan):
                    return equal(A.args[0], B.args[1]) and equal(A.args[1], B.args[0])
                elif isinstance(A, GreaterThan) and isinstance(B, LessThan):
                    return equal(A.args[0], B.args[1]) and equal(A.args[1], B.args[0])
            if A.is_Number and B.is_Number:
                return Tristate(A == B)
    return Tristate(False)

@pytest.fixture(scope="session")
def s(request):
    def infrepr():
        return 'inf'
    sympy.S.Infinity.__str__ = infrepr
    sympy.S.Infinity.__repr__ = infrepr
    sympy.S.Infinity.__unicode__ = infrepr
    now = datetime.today()
    file = open('test_{0:%Y%m%d}_{0:%H%M%S}.csv'.format(now), 'wb')
    writer = csv.writer(file)
    writer.writerows([['Function', 'Input', 'Expected', 'Result', 'Solution steps', 'Status']])
    def finish():
        file.close()
    request.addfinalizer(finish)
    def process(*arg):
        func = arg[0] if len(arg) > 0 else None
        args = arg[1:-1] if len(arg) > 1 else None
        answer = arg[-1] if len(arg) > 2 else None
        arguments = []
        sol = []
        status = 'Unknown'
        result = None
        eq = False
        try:
            with timeout(seconds=5):
                if isinstance(func, basestring):
                    func = getattr(sympy, func)
                for a in args:
                    if isinstance(a, basestring):
                        arguments.append(sympy.sympify(a))
                    else:
                        arguments.append(a)
                if answer == '???':
                    answer = None
                if isinstance(answer, basestring):
                    answer = sympy.sympify(answer)
                reset_solution()
                result = func(*arguments)
                sol = last_solution()
                if (isinstance(result, list) and len(result) == 0) or result is None:
                    eq = False
                    status = 'Answer'
                elif answer is None:
                    eq = True
                    status = 'Passed'
                else:
                    eq = equal(result, answer)
                    if eq == True:
                        status = 'Passed'
                    elif eq == False:
                        status = 'Answer'
                    else:
                        status = 'Missed'
        except KeyboardInterrupt:
            status = 'Timeout'
            raise
        except TimeoutError:
            status = 'Timeout'
            raise
        except Exception as e:
            status = 'Exception'
            raise
        finally:
            writer.writerows([[func.__name__, arguments, answer, result, len(sol), status]])
            file.flush()
        return eq
    return process  
