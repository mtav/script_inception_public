#!/usr/bin/env python3

'''
for future ref: functions of interest in python/matlab/octave are eval, exec and genvarname

csv options to consider for general reader/writer/printing functions:
  * delimiter
  * field names
  * printing format

current main csv files:
  * probe output
  * epsilon snapshots
  * time snapshots
  * frequency snapshots
  * harminv output
  * harminv selection output (from plotProbe)

.. todo:: finish this
.. todo::  interesting things from numpy doc: Structured Arrays (and Record Arrays), Standard Binary Formats: HDF5: PyTables, FITS: PyFITS

Links:

* http://docs.scipy.org/doc/numpy/user/basics.creation.html
* http://docs.scipy.org/doc/numpy/user/basics.rec.html#structured-arrays-and-record-arrays
'''

import os
import csv
import sys
import code
import numpy
from numpy import unique, size
from numpy import array, cos, sin, tan, degrees, radians, arccos, arcsin, arctan, floor, ceil, ones, zeros, pi
from collections import OrderedDict
from numpy.lib.recfunctions import append_fields

def genvarname():
  ''' should act like genvarname from Matlab/Octave
  
  .. todo:: finish if still needed...
  '''
  return ['Time', 'Ex', 'Ey', 'Ez', 'Hx', 'Hy', 'Hz']

def prnToVariables(prn_file):
  ''' A function reading in a .prn file and putting the data directly into usable variables named after the column headers. It then drops you into an interactive python session. '''
  with open(prn_file, mode='r', newline='') as csvfile:
    reader = csv.DictReader(csvfile, delimiter=' ', skipinitialspace=True)
    
    # remove empty fields (happens when lines end with spaces)
    reader.fieldnames = list( f for f in reader.fieldnames if len(f)>0 )
        
    print('-----------------')
    for f in reader.fieldnames:
      print(f)
      s = str(f) + ' = []'
      exec(s)
    print('-----------------')
    for row in reader:
      for k,v in row.items():
        if k is not None: # skip empty fields (happens when lines end with spaces)
          s = str(k)+' += ['+str(v)+']'
          exec(s)
    
  code.interact(local=locals())
  return

def readHarminvOutputDirect(filename):
  harminv_output = []
  with open(filename, newline='') as f:
    reader = csv.DictReader(f, skipinitialspace=True, delimiter=',')
    for row in reader:
      for key, value in row.items():
        row[key] = float(value)
      harminv_output.append(row)
  return harminv_output

def printHarminvOutputDirect(harminv_output):
  #code.interact(local=locals())
  keys = list(harminv_output[0].keys())
  N = len( harminv_output )
    
  print('frequency, decay constant, Q, amplitude, phase, error')
  for i in range(N):
    print('{}, {}, {}, {}, {}, {}'.format(harminv_output[i]['frequency'],
                                          harminv_output[i]['decay constant'],
                                          harminv_output[i]['Q'],
                                          harminv_output[i]['amplitude'],
                                          harminv_output[i]['phase'],
                                          harminv_output[i]['error']
                                          ))
  return

def readHarminvOutput(filename):

  harminv_output = dict()
  with open(filename, newline='') as f:

    # get header and keys
    header = f.readline()
    keys = [ i.strip() for i in header.split(',')]
    
    # set up dictionary
    for k in keys:
      harminv_output[k] = []
      
    # read data
    reader = csv.reader(f, skipinitialspace=True, delimiter=',')
    for row in reader:
      for col_idx, k in enumerate(keys):
        harminv_output[k].append(float(row[col_idx]))
      
  return harminv_output

def printHarminvOutput(harminv_output):
  keys = list(harminv_output.keys())
  N = len( harminv_output[ keys[0] ] )
  print('frequency, decay constant, Q, amplitude, phase, error')
  for i in range(N):
    print('{}, {}, {}, {}, {}, {}'.format(harminv_output['frequency'][i],
                                          harminv_output['decay constant'][i],
                                          harminv_output['Q'][i],
                                          harminv_output['amplitude'][i],
                                          harminv_output['phase'][i],
                                          harminv_output['error'][i]
                                          ))
  return

def readHarminvOutputSelection(filename):

  selection = dict()
  with open(filename, newline='') as f:

    # get header and keys
    header = f.readline()
    keys = [ i.strip() for i in header.split('\t')]
    
    # set up dictionary
    for k in keys:
      selection[k] = []
      
    # read data
    reader = csv.reader(f, skipinitialspace=True, delimiter='\t')
    for row in reader:
      for col_idx, k in enumerate(keys):
        selection[k].append(float(row[col_idx]))

  return selection

def printHarminvOutputSelection(harminv_output):
  keys = list(harminv_output.keys())
  N = len( harminv_output[ keys[0] ] )
  
  # TODO: finsh, maybe make general version
  keys = ['PeakNo', 'Frequency(Hz)', 'Wavelength(nm)', 'QFactor', 'Amplitude', 'error', 'decay_constant', 'phase']

  print('PeakNo  Frequency(Hz)   Wavelength(nm)  QFactor Amplitude       error   decay_constant  phase')
  for i in range(N):
    print('{}, {}, {}, {}, {}, {}, {}, {}'.format(harminv_output['PeakNo'][i],
                                          harminv_output['Frequency(Hz)'][i],
                                          harminv_output['Wavelength(nm)'][i],
                                          harminv_output['QFactor'][i],
                                          harminv_output['Amplitude'][i],
                                          harminv_output['error'][i],
                                          harminv_output['decay_constant'][i],
                                          harminv_output['phase'][i]
                                          ))
  return

def readProbeFile(fname):
  (header, data) = readPrnFile(fname)
  time_mus = 1e-12*data['Time']
  all_data = append_fields(data, 'time_mus', time_mus, usemask=False)
  all_header = all_data.dtype.names
  return (all_header, all_data)
  
def readPrnFile(fname):
  #data = numpy.genfromtxt(fname, dtype=<type 'float'>, comments='#', delimiter=None, skiprows=0, skip_header=0, skip_footer=0, converters=None, missing='', missing_values=None, filling_values=None, usecols=None, names=None, excludelist=None, deletechars=None, replace_space='_', autostrip=False, case_sensitive=True, defaultfmt='f%i', unpack=None, usemask=False, loose=True, invalid_raise=True)
  data = numpy.genfromtxt(fname, names=True)
  header = data.dtype.names
  return (header, data)

def writePrnFile(fname, X):
  numpy.savetxt(fname, X, fmt='%.18e', delimiter=' ', newline='\n', header='', footer='', comments='# ')
  data = X
  header = data.dtype.names
  return (header, data)

def readPrnFile_old(filename, max_lines=None, max_cols=None, delimiter='\t'):
  with open(filename, mode='r', newline='') as csvfile:

    # get header (keys)
    header_line = csvfile.readline()
    header = [ i.strip().strip('#') for i in header_line.split()]
    if max_cols:
      header = header[0:max_cols]
    
    # set up dictionary
    data = OrderedDict()
    #data = dict()
    
    for col_idx, k in enumerate(header):
      data[k] = array([])
      
    # read data
    reader = csv.reader(csvfile, skipinitialspace=True, delimiter=' ')
    row_count = 0
    for row_idx, row in enumerate(reader):
      #print(row_idx)
      #print(reader.line_num)
      if max_lines and row_count >= max_lines:
        break
      #print(row)
      if len(row) > 0:
        for col_idx, k in enumerate(header):
          data[k].append(float(row[col_idx]))
        row_count += 1

  return (header, data)
  
def getDimensions(data, header=None):
  if header is None:
    header = list(data.keys())
  
  row_label = header[1]
  col_label = header[0]
  
  Nrows = len(unique(data[row_label]))
  Ncols = len(unique(data[col_label]))
  
  return Nrows, Ncols, row_label, col_label

def reshapeData(data, Nrows=None, Ncols=None, header=None):
  if header is None:
    header = list(data.keys())

  row_label = header[1]
  col_label = header[0]
  
  Ntotal = len(data[header[0]])
  
  if Nrows is None and Ncols is not None:
    Nrows = floor(Ntotal/Ncols)
  elif Nrows is not None and Ncols is None:
    Ncols = floor(Ntotal/Nrows)
  elif Nrows is None and Ncols is None:
    Nrows, Ncols, row_label, col_label = getDimensions(data, header)
  
  col_values = unique(data[col_label])
  row_values = unique(data[row_label])
  
  # set up dictionary
  data_reshaped = OrderedDict()
  for col_idx, k in enumerate(header):
    data_reshaped[k] = array([])

  data_reshaped = data
  
  for idx, name in header:
    data_out = numpy.reshape(data[name],[len(row_values),len(col_values)],'F')
  
  
  return data_reshaped, row_values, col_values, row_label, col_label

if __name__ == '__main__':
  # read in ~/.pystartup to have all the desired modules
  pystartup = os.path.expanduser("~/.pystartup")
  with open(pystartup) as f:
    code_object = compile(f.read(), pystartup, 'exec')
    exec(code_object)

  #prnToVariables(sys.argv[1])
  (h,d) = readPrnFile(sys.argv[1])
  code.interact(local=locals())

#import os
#import sys
#import code
#print('argv = {}'.format(sys.argv))


## read in the BFDTD files
#sim = readBristolFDTD(*sys.argv[1:])

## start the interactive shell
#code.interact(local=locals())
