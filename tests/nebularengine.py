import inspect
from sympy import simplify
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


def print_traceback(task, traceback):
    print traceback,
    print "Caused by assertion at"
    print '  File "{}", line {}, in {}'.format(task.actual_func.func_code.co_filename,
                                               task.actual_func.func_code.co_firstlineno,
                                               task.func_name)
    print "    assert {} == {}".format(task.input_str, task.expected_str)


def process_result(task, async_res):
    actual, status, number_of_steps = '', 'Failed', 0
    try:
        actual, number_of_steps = async_res.get()
        status = 'Passed'
    except Exception as e:
        actual = e.actual if hasattr(e, 'actual') else '{}: {}'.format(e.__class__.__name__,
                                                                       str(e.message).replace("\n", " "))
        status = 'Answer' if isinstance(e, AssertionError) else 'Exception'
        number_of_steps = e.number_of_steps if hasattr(e, 'number_of_steps') else 0

        print_traceback(task, async_res._value.traceback)
        if isinstance(e, AssertionError):
            print '{} != {}'.format(actual, task.expected_str)
        print
    finally:
        return actual, status, number_of_steps


def enqueue_tasks(pool):
    return [(t, pool.apply_async(exec_task, args=(i,))) for i, t in enumerate(TASKS)]


def assert_matches(expected, actual):
    if hasattr(expected, 'is_number') and expected.is_number:
        assert simplify(expected - actual) == 0
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
        if is_moriarty:
            e.number_of_steps = len([s for s in last_solution() if s.startswith('_')])
        raise
    else:
        number_of_steps = len([s for s in last_solution() if s.startswith('_')]) if is_moriarty else 0
        return actual, number_of_steps
