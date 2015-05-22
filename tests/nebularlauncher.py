import macropy.activate
import billiard as mp

from nebularengine import collect_tasks, process_result, enqueue_tasks, is_moriarty

TIMEOUT = 10 # seconds


def run_tests():
    collect_tasks()

    log_name = 'nebular-moriarty.txt' if is_moriarty else 'nebular-master.txt'
    pool = mp.Pool(timeout=TIMEOUT, initializer=collect_tasks)
    with open(log_name, 'w') as f:
        header = 'func_name,input,sympylized,expected,actual,status\n'
        if is_moriarty:
            header = '{},{}\n'.format(header[:-1],'steps')
        f.write(header)
        for t, async_res in enqueue_tasks(pool):
            actual, status, number_of_steps = process_result(t, async_res)
            record = '{func_name},"{input}","{sympylized}","{expected}","{actual}",{status}\n'.format(
                func_name=t.func_name, input=t.input_str, sympylized=t.sympylized,
                expected=t.expected_str.replace("\n", " "), actual=actual, status=status)
            if is_moriarty:
                record = '{},{}\n'.format(record[:-1], number_of_steps)
            f.write(record)
            f.flush()


if __name__ == '__main__':
    mp.freeze_support()
    run_tests()


