#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import platform
import os
import sys
import getopt

def getuserdir():
  '''
  Returns the platform's "user directory".
  '''
  if 'Windows' in platform.platform():
      # print('Windows detected')
      if 'MYDOCUMENTS' in os.environ:
        return os.environ['MYDOCUMENTS']
      elif 'USERPROFILE' in os.environ:
        return os.environ['USERPROFILE']
      else:
        sys.stderr.write('WARNING: no suitable user directory found.\n')
        return ''
  else:
      # print('non-Windows detected')
    return os.path.expanduser('~')

  # alternative method on windows left for reference
  # import ctypes

  # dll = ctypes.windll.shell32
  # buf = ctypes.create_unicode_buffer(300)
  # dll.SHGetSpecialFolderPathW(None, buf, 0x0005, False)
  # print(buf.value)

if __name__ == "__main__":
  print(getuserdir())
