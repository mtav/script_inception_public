#!BPY

# To make Blender happy:
bl_info = {"name":"meep_import", "category": "User"}

"""
Name: 'MEEP (*.ctl)'
Blender: 249
Group: 'Import'
Tooltip: 'Import from MEEP'
"""

import pyscheme.parser
import pyscheme.parser
import pyscheme.scheme
import pyscheme.expressions
import sys
from glob import glob

def parseFile(filename):
  print("Processing "+filename);
  FILE = open(filename,'r');
  str = FILE.read();
  FILE.close();
  program = pyscheme.parser.parse('('+str+')')
  print(program)

if __name__ == '__main__':
  print('Importing MEEP file')

  print('=================')
  for arg in sys.argv:
      print(arg);
  print('=================')

  # blender normal
  # =================
  # C:\Program Files\Blender Foundation\Blender\blender.exe
  # =================

  # blender DOS
  # =================
  # C:\Program Files\Blender Foundation\Blender\blender.exe
  # -P
  # C:\Documents and Settings\ANONYMIZED\Application Data\Blender Foundation\Blender\.blender\scripts\meep_import.py
  # --
  # ...
  # =================

  # blender DOS post start
  # same as Blender DOS, keeps same arguments as well making it unpractical :(

  # python direct
  # =================
  # meep_import.py
  # ...
  # =================

  offset=0;
  if 'blender.exe' in sys.argv[0]:
      if len(sys.argv)>1:
          print('De DOS kaj Blender kun amo!')
          offset=4
      else:
          print('De Blender sole kun amo!')
          offset=1
  else:
      print('De la komanda linio kun amo!')
      offset=1

  # print offset
  # print len(sys.argv)
  if len(sys.argv)>offset:
      # for i in range(len(sys.argv)- 4):
          # print 'Importing ', sys.argv[4+i];
          # importMEEP(sys.argv[4+i]);
      for arg in sys.argv[offset:]:
          filelist = glob(arg);
          # print filelist
          for file in filelist:
              parseFile(file);
          # filelist = glob('*.ctl');
          # print "============"
          # print filelist
          # print "============"
          # parseFile(arg);
  else:
      print('No arguments given')
