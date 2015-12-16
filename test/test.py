import os
import sys

from nbconvert.preprocessors.execute import ExecutePreprocessor
from nbconvert.nbconvertapp import NbConvertApp
from nbconvert.preprocessors import ExecutePreprocessor
from nbconvert.preprocessors.execute import CellExecutionError
import nbformat

folder = 'notebooks'
os.chdir(folder)
nb_list = [fname for fname in os.listdir('.') if fname.endswith('.ipynb')]
nb_list.sort()

ex = ExecutePreprocessor()
ex.timeout = 180  # seconds
ex.interrupt_on_timeout = True

has_error = False
for notebook in nb_list:
    print(notebook)
    nb = nbformat.read(notebook, as_version=4)
    try:
        nb_executed, resources = ex.preprocess(nb, resources={})
        print('Pass: ' + notebook)
    except CellExecutionError as e:
        print('Fail: '  + notebook + ': ' + e.traceback[-1])
        has_error = True

os.chdir('..')
sys.exit(-1 if has_error else 0)
