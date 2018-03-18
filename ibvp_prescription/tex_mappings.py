
def ibvp(des, bcs, ics=None):
    result = ''
    result = 'Our initial-boundary value problem reads'
    result += '\n'
    result += r'\begin{alignat*}{4}'
    result += '\n'

    align_list = []
    for de in des:
        line = ''
        line += de['equation'].replace('=','&=')
        line += r'\quad && \text{for} \quad && x\in '
        line += de['domain']
        align_list.append(line)

    for bc in bcs:
        line = ''
        line += bc['equation'].replace('=','&=')
        line += r'\quad && \text{for} \quad && x\in '
        line += bc['domain']
        align_list.append(line)

    if ics:
        for ic in ics:
            line = ''
            line += ic['equation'].replace('=','&=')
            line += r'\quad && \text{for} \quad && x\in '
            line += ic['domain']
            if 'time_domain' in ic:
                line += ', t \in %s'%ic['time_domain']

            align_list.append(line)


    result += '\\\\\n'.join(align_list)

    result += r'\end{alignat*}'
    return result

def weak_forms(weak_forms, forms):
    result = ''
    result += r'\begin{mdframed}'
    result += 'Find '
    function_list = []

    for function in weak_forms['functions']:
        function_list.append('$%s \in %s$'%(function['var'],function['space']))

    result += ', '.join(function_list)
    result += ' such that'
    result += '\n'

    result += r'\begin{gather*}'
    result += '\n'

    symbol_dict = {}
    for form in forms:
        symbol_dict[form['symbol']] = '(%s)'%(', '.join(form['args']))

    equation_list = []

    for i in weak_forms['equations']:
        tokens = i['equation'].split(' ')
        for n, token in enumerate(tokens):
            if token in symbol_dict:
                tokens[n] = token+symbol_dict[token]
        equation_list.append(' '.join(tokens))

    # for equation in weak_form['equations']:
    #     result += equation['equation']
    #     result += '\\\\'
    #     result += '\n'

    result += '\\\\\n'.join(equation_list)

    result += r'\end{gather*}'
    result += '\n'

    result += 'for all '
    function_list = []
    for function in weak_forms['test_functions']:
        function_list.append('$%s \in %s$'%(function['var'],function['space']))
    result += ', '.join(function_list)
    result += '.'
    result += '\n'
    result += r'\end{mdframed}'

    return result

def forms(forms):
    result = ''
    result += r'The variational forms are defined as'
    result += '\n'

    result += r'\begin{align*}'
    result += '\n'

    align_list = []
    for form in forms:
        line = ''
        line += form['symbol']
        line += '(%s)'%(', '.join(form['args']))
        line += ' &= '
        line += form['definition']
        align_list.append(line)

    result += '\\\\\n'.join(align_list)
    result += r'\end{align*}'
    result += '\n'

    return result

def discretization(forms):
    result = ''
    result += r'The system matrices and/or vectors are defined as'
    result += '\n'

    result += r'\begin{alignat*}{3}'
    result += '\n'

    align_list = []
    for form in forms:
        if not ('discrete_symbol' in form and 'discrete_args' in form and 'discrete_definition' in form):
            continue

        line = ''
        line += form['discrete_symbol']
        line += ' &= '
        line += form['symbol']
        line += '(%s)'%(', '.join(form['discrete_args']))
        line += ' &&= '
        line += form['discrete_definition']
        align_list.append(line)

    if not align_list:
        return ''

    result += '\\\\\n'.join(align_list)
    result += r'\end{alignat*}'

    return result

def system(system):
    result = ''
    result += r'We have the following system solution/update equations:'
    result += '\n'

    result += r'\begin{gather*}'
    result += '\n'

    gather_list = []
    for equation in system:
        gather_list.append(equation['equation'])
        # gather_list.append('%s &= %s'%(form['symbol'], form['definition']))

    result += '\\\\\n'.join(gather_list)
    result += r'\end{gather*}'
    result += '\n'

    return result


def section(section):
    return '\\section*{%s}\n'%section
