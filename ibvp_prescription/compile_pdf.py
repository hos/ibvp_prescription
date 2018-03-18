import tempfile
import shutil
from os.path import join
import os

def compile_pdf(content, target_path):
    temp_dir_path = tempfile.mkdtemp()
    tex_file_path = join(temp_dir_path,'main.tex')
    pdf_file_path = join(temp_dir_path,'main.pdf')

    out = open(tex_file_path, 'w')
    out.write(content)
    out.close()

    # Compile pdf
    os.system('pdflatex -output-directory=%s %s'%(temp_dir_path, tex_file_path))

    shutil.copyfile(pdf_file_path, target_path)
    # os.rename(pdf_file_path, args.output)

