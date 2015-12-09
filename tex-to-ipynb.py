import pypandoc
import nbformat
from nbformat.sign import NotebookNotary

# TODO Utility to choose .tex files to convert, choose folder or supply list

f = 'Tutorial/chapter_align.tex' # file to convert
fsave = 'Tutorial/chapter_align.ipynb' # save converted file to location
cf = 'conv_file.tex'
notary = NotebookNotary()

with open(f, 'r') as tex:
    with open('conv_file.tex', 'w') as conv_file:
        for line in tex:
            # if """\\begin{verbatim}""" in line or '\end{verbatim}' in line:
            #     print(line)
            newline = line.replace("""begin{verbatim}""", """begin{verbatim}STARTCODE""")
            newline = newline.replace("""\end{verbatim}""", """ENDCODE\end{verbatim}""")
            conv_file.write(newline)
# TODO cleanup conv_file.tex
output = pypandoc.convert(cf, to='markdown', outputfile="temp.txt")

with open('temp.txt', 'r') as mdfile:
    with open('Tutorial/chapter_align.ipynb', 'w') as nbfile:
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
                line = line.strip('>>> ').strip('... ')
                code_section = code_section + line
            elif codeflag and '>>> ' not in line and '... ' not in line and 'ENDCODE' not in line:
                if code_section:
                    nb.cells.append(nbformat.v4.new_code_cell(source=code_section))
                code_section = ""
                codeflag = True # till in code block?
            elif 'ENDCODE' in line:
                print(code_section)
                if code_section:
                    nb.cells.append(nbformat.v4.new_code_cell(source=code_section))
                code_section = ""
                codeflag = False
            else:
                print(codeflag, line)
                break
        notary.sign(nb)
        nbfile.write(nbformat.v4.writes_json(nb))
# TODO cleanup temp.tex