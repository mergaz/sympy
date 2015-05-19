import macropy.activate
import nebulartests
# print nebulartests.u
# nebulartests.omicron()
# for f in nebulartests.omicron():
#     try:
#         f()
#     except AssertionError as e:
#         traceback.print_exc()
#         print 'nok'
#     else:
#         print 'ok'

import inspect
import billiard as mp

TIMEOUT = 10

TASKS = []


def load_test_files():
    funcs = [f for name, f in inspect.getmembers(nebulartests) if name.startswith("test_")]
    for f in funcs:
        for expectation in f():
            TASKS.append(expectation)


def exec_expectation(exp_no):
    TASKS[exp_no]()


def runtests():
    load_test_files()

    pool = mp.Pool(timeout=TIMEOUT, initializer=load_test_files)
    results = [pool.apply_async(exec_expectation, args=(i,)) for i in range(len(TASKS))]
    for r in results:
        passed = False
        comment = ''
        try:
            r.get()
            passed = True
        except Exception as e:
            print r._value.traceback
            comment = e
        print 'example,expected,actual,{},{}'.format('Passed' if passed else 'Failed', comment)


if __name__ == '__main__':
    mp.freeze_support()
    runtests()
