def ibvp(des, bcs, ics):
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

    result += '\\\\\n'.join(align_list)

    result += r'\end{alignat*}'
    return result

def weak_forms(weak_forms):
    result = ''
    result += 'Find '
    function_list = []
    for function in weak_forms['functions']:
        function_list.append('$%s \in %s$'%(function['var'],function['space']))
    result += ', '.join(function_list)
    result += ' such that'
    result += '\n'

    result += r'\begin{gather*}'
    result += '\n'
    # for equation in weak_form['equations']:
    #     result += equation['equation']
    #     result += '\\\\'
    #     result += '\n'

    result += '\\\\\n'.join([i['equation'] for i in weak_forms['equations']])

    result += r'\end{gather*}'
    result += '\n'

    result += 'for all '
    function_list = []
    for function in weak_forms['test_functions']:
        function_list.append('$%s \in %s$'%(function['var'],function['space']))
    result += ', '.join(function_list)
    result += '.'
    result += '\n'

    return result

def forms(forms):
    result = ''
    result += r'The variational forms are defined as'
    result += '\n'

    result += r'\begin{align*}'
    result += '\n'

    align_list = []
    for form in forms:
        align_list.append('%s &= %s'%(form['symbol'], form['definition']))

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
        align_list.append('%s &= %s &&= %s'%(
            form['discrete_symbol'],
            form['discrete_subs'],
            form['discrete_definition'],
        ))

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
