import yaml
import argparse
import pkg_resources
import os
import logging
# logging.basicConfig(level=logging.DEBUG)

from ibvp_prescription.template import template_content
from ibvp_prescription.tex_mappings import ibvp, weak_forms, forms, discretization, system, section
from ibvp_prescription.compile_pdf import compile_pdf

parser = argparse.ArgumentParser()
parser.add_argument('-i', '--input', type=str, help='Input YAML file')
parser.add_argument('-o', '--output', type=str, help='Output PDF file. If not provided, \
it will be the same as input file with the .pdf extension.')
parser.add_argument('-t', '--template', type=str, help='Create a template YAML to specified path')

lazyeqn_path = pkg_resources.resource_filename('ibvp_prescription','lazyeqn/lazyeqn.sty')
shortsym_path = pkg_resources.resource_filename('ibvp_prescription','shortsym/shortsym.sty')

lazyeqn_content = open(lazyeqn_path).read().replace('\ProvidesPackage{lazyeqn}\n', '')
shortsym_content = open(shortsym_path).read().replace('\ProvidesPackage{shortsym}\n', '')

header = r'''\documentclass[10pt,DIV15]{scrartcl}
\setlength\parindent{0pt}
\date{}
\usepackage{mdframed}''' \
    + lazyeqn_content \
    + shortsym_content \
    + r'\newcommand\varn[3]{{D_#2 #1\dtp #3}}' \
    + r'\begin{document}'

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

    result = ''
    result += header
    result += '\n'

    result += r'\title{%s}'%doc['title']
    result += '\n'
    result += r'\author{%s}'%doc['author']
    result += '\n'
    result += '\maketitle\n'

    if 'initial_conditions' in doc:
        ics = doc['initial_conditions']
    else:
        ics = None

    # IBVP
    result += section('IBVP')
    result += ibvp(
        doc['differential_equations'],
        doc['boundary_conditions'],
        ics=ics,
    )

    # Weak Form
    if 'weak_forms' in doc and 'forms' in doc:
        result += section('Weak Form')
        result += weak_forms(doc['weak_forms'], doc['forms'])
        result += '\n'

    # if 'forms' in doc:
        result += forms(doc['forms'])
        # Discretization
        result += section('Discretization')
        result += discretization(doc['forms'])

    # System
    if 'system' in doc:
        result += section('System Equations')
        result += system(doc['system'])

    # Footer
    result += footer


    if args.output:
        output_path = args.output
    else:
        output_path = args.input

        if output_path.endswith('.yaml'):
            output_path = output_path[:-5]

        output_path += '.pdf'

    compile_pdf(result, output_path)

    # print(doc)

if __name__ == '__main__':
    __main__()
