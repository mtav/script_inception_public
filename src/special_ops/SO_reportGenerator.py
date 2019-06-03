#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import getopt
import fnmatch
import os
import string
from optparse import OptionParser
import glob
import re
from subprocess import call
import textwrap
import shutil
import tempfile

def reportGenerator(texfile, title_list, picture_list):
  with open(texfile, 'w') as f:
    f.write('\documentclass{beamer}\n')
    f.write('\\usetheme{Copenhagen}\n')
    f.write('\n')
    f.write('\\usepackage{grffile}\n')
    f.write('\n')
    f.write('\\begin{document}\n')
    f.write('\n')

    for i in range(len(picture_list)):
      #width='+str(width_list[i])+' \\textwidth
      title = title_list[i]
      title = textwrap.fill(title, width=51)
      title = title.replace('\n','\\\\')
      title = title.replace('_','\_')
      
      f.write('\\begin{frame}{'+title+'}\\begin{center}\includegraphics[height=70mm,width=110mm,keepaspectratio]{'+picture_list[i]+'}\end{center}\end{frame}\n')
      #f.write('\\begin{frame}{'+title+'}\\begin{center}\includegraphics[totalwidth=\linewidth,height=\\textheight,keepaspectratio]{'+picture_list[i]+'}\end{center}\end{frame}\n')
      #f.write('\\begin{frame}{'+title+'}\\begin{center}Hello\end{center}\end{frame}\n')
    f.write('\n')
    f.write('\end{document}\n')
  
  cmd=['cat', texfile]
  print(cmd)
  call(cmd)
  
  if os.path.dirname(texfile):
    cmd=['pdflatex','-output-directory', os.path.dirname(texfile), texfile]
  else:
    cmd=['pdflatex', texfile]
  #tmpdir = tempfile.mkdtemp(); print 'tmpdir = ',tmpdir
  #texfileCopy = tmpdir+os.sep+os.path.basename(texfile); print 'texfileCopy = ',texfileCopy
  #shutil.copy(texfile, texfileCopy)

  #cmd=['pdflatex','-output-directory', tmpdir, texfileCopy]
  print(cmd)
  call(cmd)

  #shutil.move(os.path.splitext(texfile)[0]+'.pdf', pdfFile)

def main(argv=None):
  #usagestr = "usage: %prog [-o texfile] [ -t title ] [ -w \"widthA;widthB;...\" ] [ --picture_list=\"picA1,picA2,...;picB1,picB2...;...\" ]"
  usagestr = 'usage: %prog [-o texfile] [ -t title ]\n ex:\n '+sys.argv[0]+' -t"Title" -o tmp.tex probeimage.png !(probeimage).png'
  parser = OptionParser(usage=usagestr)

  parser.add_option("-o", "--outfile", action="store", type="string", dest="texfile", default='', help='output texfile. ex: tmp.tex, which will lead to tmp.pdf being created')
  parser.add_option("-t", "--title", action="store", type="string", dest="title", default='', help='title of each frame')
  #parser.add_option("-w", "--width_list", action="store", type="string", dest="width_list", default='0.9;1', help='width of the different picture sections (ex: "0.9;1")')
  #parser.add_option("-p", "--picture_list", action="store", type="string", dest="picture_list", default='', help='list of pictures. "," separates pictures in same section and ";" separates picture sections')
  
  (options, args) = parser.parse_args()
  
  print('options = ', options)
  print('args = ', args)
  
  #width_sections = [float(x) for x in options.width_list.split(';')]

  #picture_sections = options.picture_list.split(';')
  #print 'picture_sections = ',picture_sections
  
  #Nsections = len(picture_sections)
  
  #picture_list = []
  #width_list = []
  #for section_idx in range(Nsections):
    #s = picture_sections[section_idx].split(',')
    #width_list.extend([width_sections[section_idx]]*len(s))
    #for p in s:
      #picture_list.append(p)

  infiles = glob.glob('*.in')
  if not infiles:
    print('no infile found')
  else:
    base = os.path.splitext(infiles[0])[0]

  if not options.title:
    options.title = base
  print('options.title = ', options.title)

  if not options.texfile:
    #options.texfile = base+'.tex'
    options.texfile = base+'.report.tex'
  print('options.texfile = ', options.texfile)

  #if not args:
    #args = glob.glob('probeimage.png !(probeimage).png')
  #print 'args = ', args

  picture_list = args
  Ntotal = len(picture_list)
  
  title_list = [options.title]*Ntotal
  
  print('title_list = ', title_list)
  #print 'width_list = ', width_list
  print('picture_list = ', picture_list)
  #sys.exit(1)
  reportGenerator(options.texfile, title_list, picture_list)
  
if __name__ == "__main__":
  sys.exit(main())
