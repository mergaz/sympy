""" Convert solution log to the various text formats. Primary to the latex"""

def log_as_latex(log):
    """ Convert solution log to the latex format.
    
    Returns:
    --------
    Latex document as an array of strings.
    
    Example of usage:
    -----------------
    import sympy as sp
    from sympy.utilities.solution import *
    from sympy.utilities.solution_log import log_as_latex, log_to_file

    x = sp.Symbol('x')
    sp.solve(sp.sin(x), x)
    log_to_file('report.tex', log_as_latex(last_solution()))
    """
    
    lines = []
    
    lines.append('\\documentclass[12pt,fleqn]{article}')
    lines.append('\\usepackage[russian]{babel}')
    lines.append('\\usepackage[utf8]{inputenc}')
    lines.append('\\usepackage{amsmath,amssymb, amsthm}')
    lines.append('\\setlength{\\parindent}{0pt}')
    lines.append('\\begin{document}')
    
    for expr in log:
        if (expr.startswith('_')):
            lines.append(expr.replace('_', ''))
        else:
            lines.append('$$' + expr + '$$')
    
    lines.append('\\end{document}')
    
    return lines

def log_to_file(filename, lines):
    text_file = open(filename, 'w')
    for line in lines:
        text_file.write(line + '\n')
    text_file.close()