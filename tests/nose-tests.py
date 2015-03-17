from functools import partial
from nosedata import solve_generic, solve_9, dsolve_generic
from sympy import solve
from nose.plugins.attrib import attr
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


@attr(version='master', dataset='dsolve')
def test_dsolve_master_gen():
    for t in test_gen_master('dsolve', dsolve_generic, partial(check_master, dsolve_func)):
        yield t


@attr(version='moriarty', dataset='dsolve')
def test_dsolve_moriarty_gen():
    for t in test_gen_moriarty('dsolve', dsolve_generic, partial(check_moriarty, dsolve_func)):
        yield t


def test_gen_master(name, test_data, check_func):
    for t in test_gen('nose-{}-master.log'.format(name), 'equation,master', test_data, check_func):
        yield t


def test_gen_moriarty(name, test_data, check_func):
    for t in test_gen('nose-{}-moriarty.log'.format(name), 'equation,moriarty,length', test_data, check_func):
        yield t


def test_gen(log_name, log_header, test_data, check_func):
    with open(log_name, 'w') as f:
        f.write(log_header + '\n')

    for input, expected_answer in test_data:
        yield check_func, input, expected_answer, log_name


def check_master(func, input, expected_answer, log_name):
    answer = 'Exception'
    try:
        answer = func(input)
    finally:
        with open(log_name, 'a') as f:
            f.write('"{}","{}"\n'.format(input, answer))
    try:
        assert set(answer) == set(expected_answer)
    except TypeError:
        assert answer == expected_answer


def check_moriarty(func, input, expected_answer, log_name):
    from sympy.utilities.solution import last_solution, reset_solution

    reset_solution()
    answer = 'Exception'
    try:
        answer = func(input)
    finally:
        R = last_solution()
        number_of_steps = len([s for s in R if s.startswith('_')])
        with open(log_name, 'a') as f:
            f.write('"{}","{}",{}\n'.format(input, answer_to_str(answer), number_of_steps))
    try:
        assert set(answer) == set(expected_answer)
    except TypeError:
        assert answer == expected_answer


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
