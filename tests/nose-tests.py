from functools import partial

from nose.plugins.attrib import attr

from nosedata import solve_generic, solve_9, dsolve_generic, solve_10, solve_10_trig, solve_10_hangs, limit_func, \
    limit_data, diff_data, diff_func, integrate_data, integrate_func, solve_9_hangs
from sympy import solve, simplify
from nosedata import dsolve_func


@attr(version='master', dataset='solve')
def test_solve_master_gen():
    for t in test_gen_master('solve', solve_generic, partial(check_master, solve)):
        yield t


@attr(version='moriarty', dataset='solve')
def test_solve_moriarty_gen():
    for t in test_gen_moriarty('solve', solve_generic, partial(check_moriarty, solve)):
        yield t


@attr(version='master', dataset='solve-9')
def test_solve_9_master_gen():
    for t in test_gen_master('solve-9', solve_9, partial(check_master, solve)):
        yield t


@attr(version='moriarty', dataset='solve-9')
def test_solve_9_moriarty_gen():
    for t in test_gen_moriarty('solve-9', solve_9, partial(check_moriarty, solve)):
        yield t


@attr(version='moriarty', dataset='solve-9-hangs')
def test_solve_9_moriarty_genh():
    for t in test_gen_moriarty('solve-9-hangs', solve_9_hangs, partial(check_moriarty, solve)):
        yield t


@attr(version='moriarty', dataset='solve-10-hangs')
def test_solve_10_moriarty_genh():
    for t in test_gen_moriarty('solve-10-hangs', solve_10_hangs, partial(check_moriarty, solve)):
        yield t


@attr(version='master', dataset='solve-10-hangs')
def test_solve_10_master_genh():
    for t in test_gen_master('solve-10', solve_10_hangs, partial(check_master, solve)):
        yield t

@attr(version='master', dataset='solve-10')
def test_solve_10_master_gen():
    for t in test_gen_master('solve-10', solve_10 + solve_10_hangs, partial(check_master, solve)):
        yield t


@attr(version='moriarty', dataset='solve-10')
def test_solve_10_moriarty_gen():
    for t in test_gen_moriarty('solve-10', solve_10 + solve_10_trig, partial(check_moriarty, solve)):
        yield t


@attr(version='master', dataset='dsolve')
def test_dsolve_master_gen():
    for t in test_gen_master('dsolve', dsolve_generic, partial(check_master, dsolve_func)):
        yield t


@attr(version='moriarty', dataset='dsolve')
def test_dsolve_moriarty_gen():
    for t in test_gen_moriarty('dsolve', dsolve_generic, partial(check_moriarty, dsolve_func)):
        yield t


@attr(version='master', dataset='limit')
def test_limit_master_gen():
    for t in test_gen_master('limit', limit_data, partial(check_master, limit_func)):
        yield t


@attr(version='moriarty', dataset='limit')
def test_limit_moriarty_gen():
    for t in test_gen_moriarty('limit', limit_data, partial(check_moriarty, limit_func)):
        yield t


@attr(version='master', dataset='diff')
def test_diff_master_gen():
    for t in test_gen_master('diff', diff_data, partial(check_master, diff_func)):
        yield t


@attr(version='moriarty', dataset='diff')
def test_diff_moriarty_gen():
    for t in test_gen_moriarty('diff', diff_data, partial(check_moriarty, diff_func)):
        yield t


@attr(version='master', dataset='integrate')
def test_integrate_master_gen():
    for t in test_gen_master('integrate', integrate_data, partial(check_master, integrate_func)):
        yield t


@attr(version='moriarty', dataset='integrate')
def test_integrate_moriarty_gen():
    for t in test_gen_moriarty('integrate', integrate_data, partial(check_moriarty, integrate_func)):
        yield t


def test_gen_master(name, test_data, check_func):
    header = 'equation,expected,master,status'
    for t in test_gen('nose-{}-master.log'.format(name), header, test_data, check_func):
        yield t


def test_gen_moriarty(name, test_data, check_func):
    header = 'equation,expected,moriarty,status,length'
    for t in test_gen('nose-{}-moriarty.log'.format(name), header, test_data, check_func):
        yield t


def test_gen(log_name, log_header, test_data, check_func):
    with open(log_name, 'w') as f:
        f.write(log_header + '\n')

    for input, expected_answer in test_data:
        yield check_func, input, expected_answer, log_name


def check_master(func, input, expected_answer, log_name):
    answer = None
    status = 'Failed'
    try:
        answer = func(input)
        assert_matches(expected_answer, answer)
        status = 'Passed'
    except Exception as e:
        if answer is None:
            answer = e.__class__.__name__
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
            answer = e.__class__.__name__
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
