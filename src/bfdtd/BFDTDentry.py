#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os

class BFDTDentry(object):
  '''
  Base class for anything that can be written to BFDTD .inp or .geo files.
  '''
  def writeToFile(self, fileName, overwrite=True, append=False, call_makedirs=False):
    '''
    Writes entry to a file.
    '''
    
    # create dirs if needed
    if call_makedirs:
      if not os.path.exists(os.path.dirname(fileName)):
        os.makedirs(os.path.dirname(fileName))
    
    if not overwrite:
      mode = 'x' # open for exclusive creation, failing if the file already exists
    elif append:
      mode = 'a' # open for writing, appending to the end of the file if it exists
    else:
      mode = 'w' # open for writing, truncating the file first
    
    with open(fileName, mode=mode) as fid:
      self.write_entry(fid)
    return
