import inspect
import billiard as mp
import sys
from sympy.core.compatibility import exec_

TIMEOUT = 10

TASKS = []


def add_expectation(func):
    TASKS.append(func)


def load_test_files():
    filename = 'nebulartests.py'
    gl = {'__file__': filename, 'add_expectation': add_expectation}
    try:
        with open(filename) as f:
            source = f.read()

        code = compile(source, filename, "exec")
        exec_(code, gl)
    except (SystemExit, KeyboardInterrupt):
        raise
    except ImportError:
        print("import error", sys.exc_info())
        return

    funcs = [gl[f] for f in gl.keys() if f.startswith("test_") and
             (inspect.isfunction(gl[f]) or inspect.ismethod(gl[f])) and
             (inspect.getsourcefile(gl[f]) == filename)]
    for f in funcs:
        f()

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
            comment = e
        print 'example,expected,actual,{},{}'.format('Passed' if passed else 'Failed', comment)


if __name__ == '__main__':
    mp.freeze_support()
    runtests()
