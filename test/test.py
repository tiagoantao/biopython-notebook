import os
import sys

from nbconvert.preprocessors.execute import ExecutePreprocessor
from nbconvert.nbconvertapp import NbConvertApp
from nbconvert.preprocessors import ExecutePreprocessor
from nbconvert.preprocessors.execute import CellExecutionError
import nbformat

folder = 'notebooks'
os.chdir(folder)
nblist = ['01 - Introduction.ipynb',
          '02 - Quick Start.ipynb',
          '03 - Sequence Objects.ipynb',
          '04 - Sequence Annotation objects.ipynb',
          '05 - Sequence Input and Output.ipynb',
          '12 - Bio.PopGen - Population Genetics.ipynb',
          '13 - Phylogenetics with Bio.Phylo.ipynb',
          '17 - Graphics including GenomeDiagram.ipynb',
          '99 - Credits.ipynb']

ex = ExecutePreprocessor()
ex.timeout = 180  # seconds
ex.interrupt_on_timeout = True

has_error = False
for notebook in nblist:
    nb = nbformat.read(notebook, as_version=4)
    try:
        nb_executed, resources = ex.preprocess(nb, resources={})
        print('Pass: ' + notebook)
    except CellExecutionError as e:
        print('Fail: '  + notebook + ': ' + e.traceback[-1])
        has_error = True

os.chdir('..')
sys.exit(-1 if has_error else 0)
