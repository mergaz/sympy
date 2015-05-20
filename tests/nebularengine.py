import macropy.activate
import nebulartests
import inspect

import billiard as mp
from collections import namedtuple
from sympy import simplify

TIMEOUT = 10

# a task is a tuple func_name, 'solve(a)', 'b', expected_1, actual_1
TASKS = []
Task = namedtuple("Task", ['func_name', 'input_str', 'expected_str', 'expected_func', 'actual_func'])


def exec_task(task_no):
    actual, actual_is_computed, t = None, False, TASKS[task_no]
    try:
        expected = t.expected_func()
        actual, actual_is_computed = t.actual_func(), True
        assert_matches(expected, actual)
    except Exception as e:
        if actual_is_computed:
            e.actual = actual
        raise
    else:
        return actual


def collect_tasks():
    for func_name, func in inspect.getmembers(
            nebulartests, lambda f: hasattr(f, 'func_name') and f.func_name.startswith("test_")):
        for input_str, expected_str, expected_func, actual_func in func():
            TASKS.append(Task(func_name, input_str, expected_str, expected_func, actual_func))


def print_traceback(task, result):
    print result._value.traceback,
    print "Caused by assertion at"
    print '  File "{}", line {}, in {}'.format(task.actual_func.func_code.co_filename,
                                               task.actual_func.func_code.co_firstlineno,
                                               task.func_name)
    print "    assert {} == {}".format(task.input_str, task.expected_str)


def process_result(task, result):
    actual, status = '', 'Failed'
    try:
        actual, status = result.get(), 'Passed'
    except Exception as e:
        actual = e.actual if hasattr(e, 'actual') else '{}: {}'.format(e.__class__.__name__, e.message)
        status = 'Answer' if isinstance(e, AssertionError) else 'Exception'
        print_traceback(task, result)
        if isinstance(e, AssertionError):
            print '{} != {}'.format(actual, task.expected_str)
        print
    finally:
        return actual, status


def run_tests():
    collect_tasks()
    log_name = 'nebular-moriarty.txt'
    pool = mp.Pool(timeout=TIMEOUT, initializer=collect_tasks)
    with open(log_name, 'w') as f:
        f.write('func_name,input,expected,actual,status\n')
        for t, r in [(t, pool.apply_async(exec_task, args=(i,))) for i, t in enumerate(TASKS)]:
            actual, status = process_result(t, r)
            record = '{func_name},"{input}","{expected}","{actual}",{status}\n'.format(
                func_name=t.func_name, input=t.input_str, expected=t.expected_str, actual=actual, status=status)
            f.write(record)
            f.flush()


if __name__ == '__main__':
    mp.freeze_support()
    run_tests()


def check_master(func, input, expected_answer, log_name):
    answer = None
    status = 'Failed'
    try:
        answer = func(input)
        assert_matches(expected_answer, answer)
        status = 'Passed'
    except Exception as e:
        if answer is None:
            answer = "{}: {}".format(e.__class__.__name__, e.message)
        raise
    finally:
        with open(log_name, 'a') as f:
            f.write('"{}","{}","{}",{}\n'.format(input, expected_answer, answer, status))


def check_moriarty(func, input, expected_answer, log_name):
    from sympy.utilities.solution import last_solution, reset_solution

    reset_solution()
    answer = None
    status = 'Failed'
    try:
        answer = func(input)
        assert_matches(expected_answer, answer)
        status = 'Passed'
    except Exception as e:
        if answer is None:
            answer = "{}: {}".format(e.__class__.__name__, e.message)
        raise
    finally:
        number_of_steps = len([s for s in last_solution() if s.startswith('_')])
        with open(log_name, 'a') as f:
            f.write('"{}","{}","{}",{},{}\n'.format(input, answer_to_str(expected_answer), answer_to_str(answer),
                                                    status, number_of_steps))


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
            assert len(expected) == len(actual)
            for e, a in zip(expected, actual):
                assert_matches(e, a)
        elif isinstance(expected, dict):
            assert expected.keys() == actual.keys()
            for k in expected.keys():
                assert_matches(expected[k], actual[k])
        else:
            raise


def answer_to_str(answer):
    """
    This hack is not needed for sympy master
    """
    if isinstance(answer, list):
        return '[' + ', '.join(answer_to_str(a) for a in answer) + ']'
    elif isinstance(answer, dict):
        return '{' + ', '.join(str(k) + ': ' + answer_to_str(v) for k, v in answer.items()) + '}'
    else:
        return str(answer)
