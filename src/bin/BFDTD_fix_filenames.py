#!/usr/bin/env python3
# -*- coding: utf-8 -*-

'''
.. todo:: Add option to fix only NTFS/FAT32 incompatible filenames or create/look for script to make filenames NTFS/FAT32 compatible

          ex: recode, convmv, detox
          
          cf: http://ubuntuforums.org/showthread.php?t=1479470

          cf: http://techtots.blogspot.co.uk/2010/01/removing-invalidencoded-characters-from.html

          convmv -r --notest -f windows-1255 -t UTF-8 FILE

Note: On bluecrystal, you can use (old rename binary)::

  find . -name "*.prn" -exec rename ":" "10" {} \;
  find . -name "p??id.prn" -exec rename "p" "p0" {} \;
  rename : 10 *.prn
  rename p p0 p??id.prn

Example usage::

  BFDTD_fix_filenames.py -v --action=symlink --output-directory=. --offset 26 --output-format=dummy --id="_id_" -d ../part_2/ 

.. todo:: Add conversion to .h5 format (Note: check out h5totxt and h5fromtxt and possibly lots of other existing csv<->.h5 tools)
.. todo:: Add more type specifiers for arguments
.. todo:: better error handling using try/with/etc instead of lots of if tests.
.. todo:: Make it work for more than 836 files or whatever I have at the moment on BC2. (weird unicode characters)
.. todo:: BFDTD 2003 vs 2008/2013 formats
.. todo:: i:a.prn, etc do not seem supported.
'''

import sys
import getopt
import fnmatch
import os
import string
import argparse
import shutil
import textwrap
import utilities.brisFDTD_ID_info as brisFDTD_ID_info

def processFiles(arguments):

  src = arguments.files

  # add .prn files in specified directories recursively
  if arguments.directory:
    for directory in arguments.directory:
      matches = []
      for root, dirnames, filenames in os.walk(directory):
        for filename in fnmatch.filter(filenames, '*.prn'):
          matches.append(os.path.join(root, filename))
      
      src.extend(matches)
  
  dst = len(src)*[0]
  
  for i in range(len(src)):
    #print(src[i])
    numID, snap_plane, probe_ident, snap_time_number, fixed_filename, object_type = brisFDTD_ID_info.alphaID_to_numID(src[i], arguments.expected_object_type, arguments.probe_ident)
    #print(numID, snap_plane, probe_ident, snap_time_number, fixed_filename, object_type)
    if fixed_filename is not None:
      (directory, basename) = os.path.split(fixed_filename)

      # temporary quick hack (TODO: generalize use of offset and implement actual format specifier)
      if arguments.output_format and object_type=='fsnap':
        #print(snap_time_number)
        basename, alphaID, pair = brisFDTD_ID_info.numID_to_alphaID_FrequencySnapshot(numID + arguments.offset, snap_plane, probe_ident, snap_time_number)

      if arguments.output_directory:
        directory = arguments.output_directory
      
      if basename is None:
        continue
        
      fixed_filename = os.path.join(directory, basename)

      dst[i] = fixed_filename
      if dst[i]:
        if arguments.verbose:
          print( arguments.action + ' ' + src[i] + ' -> ' + dst[i] )
        if os.path.isfile(src[i]):
          if (not os.path.isfile(dst[i])) or arguments.force:
            if (not arguments.no_act):
              if arguments.action == 'move':
                os.rename(src[i], dst[i])
              elif arguments.action == 'copy':
                shutil.copy(src[i], dst[i])
              elif arguments.action == 'copyfile':
                shutil.copyfile(src[i], dst[i]) # when the filesystem does not support chmod permissions (i.e. Windows)
              elif arguments.action == 'hardlink':
                os.link(src[i], dst[i])
              elif arguments.action == 'symlink':
                os.symlink(src[i], dst[i])
              else:
                print('action not recognized : action = ' + arguments.action,file=sys.stderr)
                sys.exit(-1)
          else:
            print('WARNING: Skipping '+src[i]+' -> '+dst[i]+' : destination file exists', file=sys.stderr)
        else:
          print('WARNING: Skipping '+src[i]+' -> '+dst[i]+' : source file does not exist', file=sys.stderr)
      else:
        print('WARNING: ' + src[i] + ' could not be converted', file=sys.stderr)

  # left in for reference
  #for filename in fnmatch.filter(filenames, '*:*.prn'):
    #dst.append(os.path.join(root, string.replace(filename,':','10')))
  #for filename in fnmatch.filter(filenames, 'p??id.prn'):
    #dst.append(os.path.join(root, string.replace(filename,'p','p0',1)))
  return

def get_argument_parser():
  # command-line option handling  
  parser = argparse.ArgumentParser(formatter_class=argparse.RawDescriptionHelpFormatter, fromfile_prefix_chars='@',
          description=textwrap.dedent('''\
                 Rename .prn files produced by BFDTD to NTFS compatible names (as well as human readable).
                 
                 Example usage:
                   BFDTD_fix_filenames.py -v --action=symlink --output-directory=. --offset 26 --output-format=dummy --id="_id_" -d ../part_2/
                 '''))
  
  parser.add_argument("-v", "--verbose", action="store_true", dest="verbose", default=False, help="Verbose: print names of files successfully renamed.")
  parser.add_argument("-n", "--no-act", action="store_true", dest="no_act", default=False, help="No Action: show what files would have been renamed.")
  parser.add_argument("-f", "--force", action="store_true", dest="force", default=False, help="Force: overwrite existing files.")
  parser.add_argument("-d", "--directory", action="append", dest="directory", help="rename all .prn files in this directory recursively. Multiple directories can be specified with -d DIR1 -d DIR2")
  parser.add_argument('files', action="store", nargs='*', help='input files (.prn)')
  parser.add_argument("--id", action="store", dest="probe_ident", default=None, help="specify a probe identifier")
  parser.add_argument("--type", action="store", dest="expected_object_type", choices=['fsnap','tsnap','mfprobe','probe'], default=None, help="specify the type of .prn file")
  parser.add_argument('--offset', type=int, default=0, help='numID offset')
  parser.add_argument("--output-format", action="store", default=None, help="specify format of the output files")
  parser.add_argument("--output-directory", action="store", help="Optional output directory (should exist). If not specified, output will go into the same directory as original file.")
  parser.add_argument("--action", action="store", choices=['move','copy','copyfile','hardlink','symlink'], default='move', help="move (rename), copy, hardlink or symlink to the new destination/filename?")

  return parser

def main(args=None):
  parser = get_argument_parser()
  arguments = parser.parse_args() if args is None else parser.parse_args(args)
  
  # Only works if func has been defined (for example with subcommand and set_defaults())
  #arguments.func(arguments)  # call the appropriate subcommand function

  if not len(sys.argv) > 1:
    parser.print_help()
  else:
    print('---------')
    print(arguments)
    print('---------')

    processFiles(arguments)
  return(0)

if __name__ == "__main__":
    sys.exit(main())
