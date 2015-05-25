import inspect
from sympy import *
from sympy.core.relational import Relational
from sympy.logic.boolalg import BooleanAtom
from sympy.printing import srepr
import nebulartests
from macropy.case_classes import macros, case

try:
    from sympy.utilities.solution import last_solution, reset_solution

    is_moriarty = True
except ImportError:
    is_moriarty = False


@case
class Task(func_name, input_str, sympylized, expected_str, expected_func, actual_func): pass


TASKS = []


def collect_tasks():
    for func_name, func in inspect.getmembers(
            nebulartests, lambda f: hasattr(f, 'func_name') and f.func_name.startswith("test_")):
        for input_str, sympylized, expected_str, expected_func, actual_func in func():
            TASKS.append(Task(func_name, input_str, sympylized, expected_str, expected_func, actual_func))


def print_traceback(task, traceback, actual, e):
    print traceback,
    print "Caused by assertion at"
    print '  File "{}", line {}, in {}'.format(task.actual_func.func_code.co_filename,
                                               task.actual_func.func_code.co_firstlineno,
                                               task.func_name)
    print "    assert {} == {}".format(task.input_str, task.expected_str)
    if isinstance(e, AssertionError):
        expected = e.expected if hasattr(e, 'expected') else task.expected_str
        print '{} != {}'.format(srepr(actual), srepr(expected))
    print


def process_result(task, async_res):
    actual, status, number_of_steps = '', 'Failed', 0
    try:
        actual, number_of_steps = async_res.get()
        status = 'Passed'
    except Exception as e:
        actual = e.actual if hasattr(e, 'actual') \
            else '{}: {}'.format(e.__class__.__name__, str(e.message).replace("\n", " "))
        status = 'Answer' if isinstance(e, AssertionError) else 'Exception'
        number_of_steps = e.number_of_steps if hasattr(e, 'number_of_steps') else 0

        print_traceback(task, async_res._value.traceback, actual, e)
    finally:
        return actual, status, number_of_steps


def enqueue_tasks(pool):
    return [(t, pool.apply_async(exec_task, args=(i,))) for i, t in enumerate(TASKS)]


def assert_matches(expected, actual):
    if hasattr(expected, 'is_number') and expected.is_number:
        assert simplify(expected - actual) == 0
        return
    if isinstance(expected, (And, Or, Relational, Interval, BooleanAtom, bool)) and len(expected.free_symbols) == 1:
        int_exp = as_interval(expected)
        int_act = as_interval(actual)
        assert (int_exp - int_act).is_EmptySet and (int_act - int_exp).is_EmptySet
        return
    if hasattr(expected, 'dummy_eq'):
        assert expected.dummy_eq(actual)
        return
    try:
        assert expected == actual
    except AssertionError:
        if isinstance(expected, list):
            assert isinstance(actual, list) and len(expected) == len(actual)
            for e, a in zip(expected, actual):
                assert_matches(e, a)
        elif isinstance(expected, dict):
            assert isinstance(actual, dict) and expected.keys() == actual.keys()
            for k in expected.keys():
                assert_matches(expected[k], actual[k])
        else:
            raise


def as_interval(expr):
    if isinstance(expr, Interval):
        return expr
    if expr in (False, S.false):
        return S.EmptySet
    if expr in (True, S.true):
        return Interval(-oo, oo)
    if len(expr.free_symbols) != 1:
        raise ValueError('There must be exactly one variable in the expression: {}'.format(srepr(expr)))
    if isinstance(expr, LessThan):  # x <= 2 ; 2 <= x
        return Interval(-oo, expr.rhs) if expr.lhs.is_Symbol else Interval(expr.lhs, oo)
    if isinstance(expr, StrictLessThan):  # x < 2 ; 2 < x
        return Interval(-oo, expr.rhs, right_open=True) if expr.lhs.is_Symbol \
            else Interval(expr.lhs, oo, left_open=True)
    if isinstance(expr, GreaterThan):  # x >= 2 ; 2 >= x
        return Interval(expr.rhs, oo) if expr.lhs.is_Symbol else Interval(-oo, expr.lhs)
    if isinstance(expr, StrictGreaterThan):  # x > 2 ; 2 > x
        return Interval(expr.rhs, oo, left_open=True) if expr.lhs.is_Symbol \
            else Interval(-oo, expr.lhs, right_open=True)
    if isinstance(expr, Equality):  # x == 2
        return FiniteSet(expr.rhs if expr.lhs.is_Symbol else expr.lhs)
    if isinstance(expr, Unequality):  # x != 2
        point = expr.rhs if expr.lhs.is_Symbol else expr.lhs
        return Interval(-oo, point, right_open=True).union(Interval(point, oo, left_open=True))
    if isinstance(expr, And):
        return reduce(Set.intersect, map(as_interval, expr.args))
    if isinstance(expr, Or):
        return reduce(Set.union, map(as_interval, expr.args))
    raise ValueError('Cannot convert to Interval: {}'.format(srepr(expr)))


def exec_task(task_no):
    actual, actual_is_computed, t = None, False, TASKS[task_no]
    try:
        if is_moriarty:
            reset_solution()
        expected = t.expected_func()
        actual, actual_is_computed = t.actual_func(), True
        assert_matches(expected, actual)
    except Exception as e:
        if actual_is_computed:
            e.actual = actual
            e.expected = expected
        if is_moriarty:
            e.number_of_steps = len([s for s in last_solution() if s.startswith('_')])
        raise
    else:
        number_of_steps = len([s for s in last_solution() if s.startswith('_')]) if is_moriarty else 0
        return actual, number_of_steps
