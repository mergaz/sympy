from nosedata import solve_input
from sympy import solve
from nose.plugins.attrib import attr


@attr(version='master')
def test_solve_master_gen():
    with open('nose-solve-master.log', 'w') as f:
        f.write('equation,master\n')

    for input, expected_answer in solve_input:
        yield check_solution_master, input, expected_answer


@attr(version='moriarty')
def test_solve_gen():
    with open('nose-solve.log', 'w') as f:
        f.write('equation,moriarty,length\n')

    for input, expected_answer in solve_input:
        yield check_solution, input, expected_answer


def check_solution_master(input, expected_answer):
    answer = 'Exception'
    try:
        answer = solve(input)
    finally:
        with open('nose-solve-master.log', 'a') as f:
            f.write('"{}","{}"\n'.format(input, answer))
    try:
        assert set(answer) == set(expected_answer)
    except TypeError:
        assert answer == expected_answer


def check_solution(input, expected_answer):
    from sympy.utilities.solution import last_solution, reset_solution

    reset_solution()
    answer = 'Exception'
    try:
        answer = solve(input)
    finally:
        R = last_solution()
        number_of_steps = len([s for s in R if s.startswith('_')])
        with open('nose-solve.log', 'a') as f:
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
