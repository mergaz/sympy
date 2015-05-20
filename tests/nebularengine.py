import macropy.activate
import nebulartests
from nebulartests import ComparisonFailure, EvaluationFailure, Success
from traceback import print_exception
from sys import exc_info
import inspect

import billiard as mp
from sympy import simplify

TIMEOUT = 10

# a task is a tuple 'solve(a)', 'b', expected_1, actual_1
TASKS = []


def exec_expectation(exp_no):
    input_str, expected_str, expected_func, actual_func = TASKS[exp_no]
    actual = None
    try:
        expected = expected_func()
        actual = actual_func()
        assert_matches(expected, actual)
    except Exception as e:
        e.actual = actual
        raise
    else:
        return actual


def load_test_files():
    funcs = [f for name, f in inspect.getmembers(nebulartests) if name.startswith("test_")]
    for f in funcs:
        for tasks in f():
            TASKS.append(tasks)


def run_tests():
    load_test_files()

    pool = mp.Pool(timeout=TIMEOUT, initializer=load_test_files)
    results = [pool.apply_async(exec_expectation, args=(i,)) for i in range(len(TASKS))]
    for i, r in enumerate(results):
        status = 'Failed'
        try:
            actual = r.get()
            status = 'Passed'
        except Exception as e:
            if hasattr(e, 'actual') and e.actual is not None:
                actual = e.actual
            else:
                actual = "{}: {}".format(e.__class__.__name__, e.message)
            if isinstance(e, AssertionError):
                status = 'Answer'
            print r._value.traceback
            print "Caused by example at"
            print '  File "{}", line {}'.format(TASKS[i][3].func_code.co_filename, TASKS[i][3].func_code.co_firstlineno)
            print "    assert {} == {}\n".format(TASKS[i][0], TASKS[i][1])
        print '{input},{expected},{actual},{status}'.format(input=TASKS[i][0],
                                                            expected=TASKS[i][1],
                                                            actual=actual,
                                                            status=status)


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
