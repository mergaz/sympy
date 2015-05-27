import macropy.activate
import billiard as mp

from nebularengine import collect_tasks, process_result, enqueue_tasks, is_moriarty

TIMEOUT = 10  # seconds


def run_tests():
    collect_tasks()

    pool = mp.Pool(timeout=TIMEOUT, initializer=collect_tasks)
    log_name = 'nebular-moriarty.csv' if is_moriarty else 'nebular-master.csv'
    with open(log_name, 'w') as f:
        f.write(format_header())
        for task, async_res in enqueue_tasks(pool):
            actual, status, number_of_steps = process_result(task, async_res)
            f.write(format_record(actual, number_of_steps, status, task))
            f.flush()


def format_record(actual, number_of_steps, status, t):
    return '{func_name},"{input}","{sympylized}","{expected}","{actual}",{status}{steps}\n'.format(
        func_name=t.func_name, input=t.input_str, sympylized=t.sympylized,
        expected=t.expected_str.replace("\n", " "), actual=actual, status=status,
        steps=',' + str(number_of_steps) if is_moriarty else '')


def format_header():
    return 'func_name,input,sympylized,expected,{actual},status{steps}\n'.format(
        actual='moriarty' if is_moriarty else 'master',
        steps=',steps' if is_moriarty else '')


if __name__ == '__main__':
    mp.freeze_support()
    run_tests()
