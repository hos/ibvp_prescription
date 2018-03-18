import yaml
import argparse
import pkg_resources
import shutil
import tempfile
import os
from os.path import join
import logging
# logging.basicConfig(level=logging.DEBUG)

from ibvp_prescription.template import template_content
from ibvp_prescription.tex_mappings import ibvp, weak_forms, forms, discretization, system, section

parser = argparse.ArgumentParser()
parser.add_argument('-i', '--input', type=str, help='Input YAML file')
parser.add_argument('-o', '--output', type=str, help='Output PDF file. If not provided, \
it will be the same as input file with the .pdf extension.')
parser.add_argument('-t', '--template', type=str, help='Create a template YAML to specified path')

lazyeqn_path = pkg_resources.resource_filename('ibvp_prescription','lazyeqn/lazyeqn.sty')
shortsym_path = pkg_resources.resource_filename('ibvp_prescription','shortsym/shortsym.sty')

lazyeqn_content = open(lazyeqn_path).read().replace('\ProvidesPackage{lazyeqn}\n', '')
shortsym_content = open(shortsym_path).read().replace('\ProvidesPackage{shortsym}\n', '')

header = r'''\documentclass{article}
\setlength\parindent{0pt}''' \
    +lazyeqn_content \
    +shortsym_content \
    +r'\begin{document}'

footer = r'''\end{document}'''


def __main__():
    args = parser.parse_args()

    if args.template:
        open(args.template, 'w').write(template_content)
        return

    if not (args.input):
        raise Exception('Input file not specified')

    f = open(args.input)
    doc = yaml.load(f.read())

    temp_dir_path = tempfile.mkdtemp()
    tex_file_path = join(temp_dir_path,'main.tex')
    pdf_file_path = join(temp_dir_path,'main.pdf')

    out = open(tex_file_path, 'w')

    out.write(header)
    out.write('\n')

    out.write(r'\title{%s}'%doc['title'])
    out.write('\n')
    out.write(r'\author{%s}'%doc['author'])
    out.write('\n')
    out.write('\maketitle\n')

    # IBVP
    out.write(section('IBVP'))

    out.write(ibvp(
        doc['differential_equations'],
        doc['boundary_conditions'],
        doc['initial_conditions'],
    ))

    # Weak Form
    out.write(section('Weak Form'))

    out.write(weak_forms(doc['weak_forms']))

    out.write('\n')

    out.write(forms(doc['forms']))

    # Discretization
    out.write(section('Discretization'))

    out.write(discretization(doc['forms']))

    # Discretization
    out.write(section('System Equations'))

    out.write(system(doc['system']))

    out.write(footer)
    out.close()

    # Compile pdf
    os.system('pdflatex -output-directory=%s %s'%(temp_dir_path, tex_file_path))

    if args.output:
        output_path = args.output
    else:
        output_path = args.input

        if output_path.endswith('.yaml'):
            output_path = output_path[:-5]

        output_path += '.pdf'

    shutil.copyfile(pdf_file_path, output_path)
    # os.rename(pdf_file_path, args.output)

    # print(doc)

if __name__ == '__main__':
    __main__()
