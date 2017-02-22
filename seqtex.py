#!/usr/bin/python
import re
import sys
import tempfile
import subprocess
import os

def export_equations(filename,dest,target,dpi=500):
    
    with open(filename,'r') as f:
        s = f.read()

    names = [ dest+re.sub('[\W]','',n) for n in re.findall('%.{,}%\n',s) ] 
    eqns = re.split('%.{,}%\n',s)[1:]
    tmp_name = '.tempfile_latex_to_png'

    print names

    preamble = '''\documentclass[preview]{standalone}
    \n\usepackage{amsmath}
    \usepackage{bm}
    \usepackage{xcolor}
    \usepackage{environ}
    \usepackage{graphicx}
    \n\NewEnviron{lgequation}{%
        \\begin{equation*}
        \scalebox{1.25}{$\BODY$}
        \end{equation*}
    }\n\n'''

    for outfile,eq in zip(names,eqns):
        # if target is specified, only compile that equation
        if target is not None and outfile != (dest+target):
            continue

        # make temporary file
        temp = open(tmp_name+'.tex','w')

        # preamble
        temp.write(preamble)

        # begin main body of latex doc
        temp.write('\\begin{document}\n\n')
        temp.write('\pagestyle{empty}\n\n')
        
        # write equation
        [ temp.write(line+'\n') for line in eq.split('\n') ]
        
        # end latex doc
        temp.write('\end{document}\n')

        # compile
        temp.close()
        subprocess.call(['pdflatex','-interaction=nonstopmode',tmp_name])

        # crop pdf, convert to png
        subprocess.call('pdfcrop %s.pdf %s.pdf'%(tmp_name,outfile),shell=True)
        # subprocess.call('convert -density %i %s.pdf %s.png'%(dpi,outfile,outfile),shell=True)

    # delete all temporary files
    subprocess.call(['rm', tmp_name+'.tex'])
    subprocess.call(['rm', tmp_name+'.pdf'])
    subprocess.call(['rm', tmp_name+'.log'])
    subprocess.call(['rm', tmp_name+'.aux'])

if __name__=="__main__":
    fn = 'equations.tex'
    dest = './equations/'
    target = None if len(sys.argv)<2 else str(sys.argv[1])
    export_equations(fn,dest,target)
