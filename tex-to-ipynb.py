# WARNING This is very much a draft, it seems to work.
# Some code in the examples is not marked as docstrings i.e. There is no >>> before the line of code.
# TODO, BUGFIX, assumes docstring like code in verbatim tag,
# TODO cont. ignores everything with without >>> or ....

import pypandoc
import nbformat
from nbformat.sign import NotebookNotary
from os import listdir
from os.path import isfile, join

notary = NotebookNotary()

def convert_file(texfile, ipynbfile):
    """
    convert file from .tex to ipynb, separates text cells from code cells
    """
    with open(texfile, 'r') as tex:
        with open('temp.tex', 'w') as conv_file: # could not get a stingIO object to work
            for line in tex:
                # if '\\begin{verbatim}' in line or '\end{verbatim}' in line:
                #     print(line)
                newline = line.replace("""begin{verbatim}""", """begin{verbatim}STARTCODE""")
                newline = newline.replace("""\end{verbatim}""", """ENDCODE\end{verbatim}""")
                conv_file.write(newline)
    # TODO cleanup conv_file.tex
    output = pypandoc.convert('temp.tex', to='markdown', outputfile="temp.txt")
    
    with open('temp.txt', 'r') as mdfile:
        with open(ipynbfile+'.ipynb', 'w') as nbfile:
            nb = nbformat.v4.new_notebook()
            mb_section = ""
            code_section = ""
            codeflag = False #assume we don't start with a code block
            for line in mdfile:
                if not codeflag:
                    if "STARTCODE" not in line:
                        mb_section = mb_section + line
                    elif "STARTCODE" in line:
                        nb.cells.append(nbformat.v4.new_markdown_cell(mb_section))
                        codeflag = True
                        mb_section = ""
                elif codeflag and ('>>> ' in line or '... ' in line):
                    # This should be code
                    codeflag += 1
                    line = line.strip('>>> ').strip('... ')
                    code_section = code_section + line
                elif codeflag == 1 and not 'ENDCODE' in line:
                    # codeflag is still 1, no code seen yet, This might be a section marked verbatium
                    # but not code, will write this to a code block.
                    code_section = code_section + line
                elif codeflag > 1 and '>>> ' not in line and '... ' not in line and 'ENDCODE' not in line:
                    # This should be the results of the code
                    # lets write what we have to a code cell
                    if code_section:
                        nb.cells.append(nbformat.v4.new_code_cell(source=code_section))
                    code_section = ""
                    codeflag += 1 # still in code block?
                elif 'ENDCODE' in line and codeflag == 1:
                    #print(code_section)
                    if code_section:
                        # if we got here this is probably a verbatium section.
                        code_section = '```\n' + code_section.lstrip('    ').replace('\n    ', '\n') + '\n```'
                        nb.cells.append(nbformat.v4.new_markdown_cell(code_section))
                    code_section = ""
                    codeflag = False
                elif 'ENDCODE' in line and codeflag > 1:
                    #print(code_section)
                    if code_section:
                        # if we got here this is probably a verbatium section.
                        nb.cells.append(nbformat.v4.new_code_cell(source=code_section))
                    code_section = ""
                    codeflag = False
                else:
                    #print(codeflag, line)
                    break
            notary.sign(nb)
            nbfile.write(nbformat.v4.writes_json(nb))
    # TODO cleanup temp.tex

def convert_set(files, outfolder=''):
    """
    :param list: list of files to convert or a folder of which all .tex files will be converted
    :param outfolder: save files to this location
    :return: Tuple: count of files listed, count of files converted, count of files ignored
    """
    if isinstance(files, str): # convert folder
        files = [files + f for f in listdir(files) if isfile(join(files, f)) and f.endswith('.tex')]
        for tfile in files:
            #print(tfile)
            ipynbfile = outfolder + tfile.replace('.tex', '').split('/')[-1]
            #print(ipynbfile)
            #print(ipynbfile)
            try:
                convert_file(tfile, ipynbfile)
            except Exception as e:
                print('Failed :' + ipynbfile)
                print(e)
    elif isinstance(files, (list, tuple)):
        for tfile in files:
            #print(tfile)
            ipynbfile = outfolder + tfile.replace('.tex', '').split('/')[-1]
            #print(ipynbfile)
            try:
                convert_file(tfile, ipynbfile)
            except Exception as e:
                print('Failed :' + ipynbfile)
                print(e)

    # TODO count files


convert_set('/Users/vincentdavis/VersionControl/biopython/Doc/Tutorial/', 'Tutorial/')