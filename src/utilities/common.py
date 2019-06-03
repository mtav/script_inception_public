#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
import getopt
import numpy
import math
import re
import datetime
import os
import subprocess
from numpy import array, ceil, arange
import decimal
import warnings

def eng_string( x, format='%s', si=False):
    '''
    Returns float/int value <x> formatted in a simplified engineering format -
    using an exponent that is a multiple of 3.

    format: printf-style string used to format the value before the exponent.

    si: if true, use SI suffix for exponent, e.g. k instead of e3, n instead of
    e-9 etc.

    E.g. with format='%.2f'::
    
        1.23e-08 => 12.30e-9
             123 => 123.00
          1230.0 => 1.23e3
      -1230000.0 => -1.23e6

    and with si=True::
    
          1230.0 => 1.23k
      -1230000.0 => -1.23M

    References/sources:

      * http://stackoverflow.com/questions/12311148/print-number-in-engineering-format
      * http://stackoverflow.com/questions/17973278/python-decimal-engineering-notation-for-mili-10e-3-and-micro-10e-6
      * http://stackoverflow.com/questions/12985438/print-numbers-in-terms-of-engineering-units-in-python
    '''
    sign = ''
    if x < 0:
        x = -x
        sign = '-'
    exp = int( math.floor( math.log10( x)))
    exp3 = exp - ( exp % 3)
    x3 = x / ( 10 ** exp3)

    if si and exp3 >= -24 and exp3 <= 24 and exp3 != 0:
        exp3_text = 'yzafpnum kMGTPEZY'[ ( exp3 - (-24)) // 3 ]
    elif exp3 == 0:
        exp3_text = ''
    else:
        exp3_text = 'e%s' % exp3

    return ( '%s'+format+'%s') % ( sign, x3, exp3_text)

def check_call_and_log(cmd, log_file_object):
  '''
  Custom extension of the *check_call* function from the python *subprocess* module.
  It redirects *stderr* to *stdout* and prints both out to the screen, while also writing them to the file object *log_file_object*.
  
  .. todo:: Creating a custom file object would be nicer and enable use of all the *subprocess* convenience functions.
  '''
  with subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT) as p:
    for line in p.stdout:
      log_file_object.write(line.decode())
      sys.stdout.write(line.decode())
    retcode = p.wait()
    if retcode:
      raise subprocess.CalledProcessError(retcode, cmd)
  return 0

def runCommandAndStoreOutput(cmd, outfilename, verbosity=0):
  
  if verbosity >= 1:
    print('cmd = {}'.format(cmd))
    print('outfilename = {}'.format(outfilename))
  with open(outfilename, 'w') as outFile:
    if verbosity >= 2:
      check_call_and_log(cmd, outFile)
    else:
      subprocess.check_call(cmd, stdout=outFile)
  
  return

def runSimulation(exe, inFileName, outfilename=None, verbosity=0):
  '''
  Just a simple convenience function to run a simulation in the directory of the input file and then going back to the original working directory.
  The output is saved in a file of the form ``basename(inFileName)+'.out'`` by default.
  
  :param str exe: The executable to use.
  :param str inFileName: The input file to use.
  :param str outfilename: The output file to use (i.e. logfile). If *None*, a filename will be built by replacing the extension of *inFileName* with ".out". Default: None
  :param int verbosity: If *verbosity*>=1, the final command used will be printed out. If *verbosity*>=2, the commands output will also be printed to screen. Default: 0
  '''
  
  if not os.path.isfile(inFileName):
    raise UserWarning('File not found: {}'.format(inFileName))
  
  if outfilename is None:
    outfilename = os.path.splitext(os.path.basename(inFileName))[0]+'.out'
  
  orig_cwd = os.getcwd()
  os.chdir(os.path.dirname(os.path.abspath(inFileName)))
  with open(outfilename,'w') as outFile:
    cmd = [exe, os.path.basename(inFileName)]
    if verbosity >= 1:
      print('cmd = {}'.format(cmd))
    if verbosity >= 2:
      check_call_and_log(cmd, outFile)
    else:
      subprocess.check_call(cmd, stdout=outFile)
  os.chdir(orig_cwd)
  return

def fixLowerUpper(L,U):
  real_L = [0,0,0]
  real_U = [0,0,0]
  for i in range(3):
    real_L[i] = min(L[i],U[i])
    real_U[i] = max(L[i],U[i])
  return real_L, real_U

def LimitsToThickness(limits):
  return [ limits[i+1]-limits[i] for i in range(len(limits)-1) ]

#def getUnitaryDirection()
#E = subtract(excitation.P2,excitation.P1)
#E = list(E/linalg.norm(E))

def getProbeColumnFromExcitation(excitation):
  print(('excitation = ',excitation))
  probe_col = 0
  if excitation == [1,0,0]:
    probe_col = 2
  elif excitation == [0,1,0]:
    probe_col = 3
  elif excitation == [0,0,1]:
    probe_col = 4
  else:
    print('ERROR in getProbeColumnFromExcitation: Unknown Excitation type')
    sys.exit(-1)
  print(('probe_col', probe_col))
  return probe_col

def symmetrifyEven(vec):
  ''' [1, 2, 3]->[1, 2, 3, 3, 2, 1] '''
  sym = vec[:]; sym.reverse()
  return vec + sym

def symmetrifyOdd(vec):
  ''' [1, 2, 3]->[1, 2, 3, 2, 1] '''
  sym = vec[:]; sym.reverse()
  return vec + sym[1:]

def symmetrifyAndSubtractOdd(vec,max):
  ''' [1, 2, 3]->[1, 2, 3, 8, 9] for max = 10
      [0, 1, 2, 3]->[0, 1, 2, 3, 4, 5, 6] for max = 6 '''
  sym = vec[:]; sym.reverse()
  sym_cut = [max-x for x in sym[1:]]
  return vec + sym_cut

def float_array(A):
    '''
    convert string array to float array
    
    .. todo:: rename to float_list, since it returns a python list and not a numpy array, or replace with [f(i) for i in L]
    '''
    for i in range(len(A)):
        A[i] = float(A[i])
    return(A)
  
def int_array(A):
    '''
    convert string array to int array
    
    .. todo:: rename to int_list, since it returns a python list and not a numpy array, or replace with [f(i) for i in L]
    '''
    for i in range(len(A)):
      A[i] = int(float(A[i]))
    return(A)

def str2list(instr, numeric=True, array=True):
  '''
  Converts strings of the form '[1,2,3],[4,5,6],[7,8,9]' into a list of lists of the form [['1', '2', '3'], ['4', '5', '6'], ['7', '8', '9']]
  
  * If numeric is set to True, converts all elements to float, otherwise leaves them as strings.
  * If array is set to True, converts the lists to numpy arrays.
  * If instr is not of type string, it raises a TypeError.
  
  .. note:: Seems to only be used in the *weijeiWoodpile.py* script at the moment to deal with input from ConfigParser.
  .. note:: This could be done with an eval-like function... I guess this is safer in the end?
  '''
  
  if not isinstance(instr, str):
    raise TypeError('Invalid type for instr: {}. instr should be of type str.'.format(type(instr)))
    #if isinstance(instr, (list, numpy.ndarray)):
      #return(instr)
    #else:
      #raise TypeError('Invalid type for instr: {}. instr should be of type str, list or numpy.ndarray.'.format(type(instr)))
  
  ret = []
  
  listElements = re.compile("([^\[,\]]+)")
  insideBrackets = re.compile("(\[[^\[\]]+\])")

  lists = [m.group(1) for m in insideBrackets.finditer(instr)]
  for i in lists:
    elements = [m.group(1) for m in listElements.finditer(i)]
    ret.append(elements)

  if numeric:
    for A in ret:
      for i in range(len(A)):
        A[i]=float(A[i])

  if array:
    for i in range(len(ret)):
      ret[i] = numpy.array(ret[i])

  return ret

def is_number(s):
    ''' returns true if s can be converted to a float, otherwise false '''
    try:
        float(s)
        return True
    except ValueError:
        return False

def addExtension(filename, default_extension):
    ''' add default_extension if the file does not end in .geo or .inp '''
    
    extension = getExtension(filename)
    if extension == 'geo' or extension == 'inp':
        return filename
    else:
        return filename + '.' + default_extension

# Functions of dubious necessity... For Python beginners. :)
def getExtension(filename):
  '''
    returns extension of filename
    .. todo:: get rid of this and replace it with os.path.splitext wherever used
  '''
  warnings.warn('Please avoid getExtension and use (root, ext) = os.path.splitext(filename) instead to reduce unnecessary dependencies.', category=DeprecationWarning)
  # (root, ext) = os.path.splitext(filename) # with leading dot: .txt
  # return(ext)
  return filename.split(".")[-1] # no leading dot: txt

def substituteExtension(s,oldext,newext):
  '''
  For easier to read code?
  '''
  return re.sub(oldext+'$',newext,s)

def getVecAlphaDirectionFromVar(var):
  ''' Returns ([1,0,0],'x'),etc corresponding to var(alpha or vector) '''
  S = ['x','y','z']
  V = [[1,0,0],[0,1,0],[0,0,1]]
  if var in V:
    return var, S[var.index(1)]
  elif var.lower() in S:
    return V[S.index(var.lower())],var.lower()
  else:
    print('unknown direction: '+str(var))
    sys.exit(-1)
  
def planeNumberName(var):
  ''' Returns numindex(1,2,3) and char('X','Y','Z') corresponding  to var(num or alpha index) '''
  S = ['X','Y','Z']
  if var in [1, 2, 3]:
    return var, S[var-1]
  elif var.upper() in S:
    return S.index(var.upper()) + 1, var.upper()
  else:
    print('unknown plane: ' + str(var))
    sys.exit(-1)

# based on functions from http://stackoverflow.com/questions/2566412/find-nearest-value-in-numpy-array
def findNearest(a, a0):
    ''' Element in nd array `a` closest to the scalar value `a0` 
    returns (idx, a.flat[idx]) = (index of closest value, closest value)'''
    a = array(a)
    idx = numpy.abs(a - a0).argmin()
    return (idx, a.flat[idx])

def findNearestInSortedArray(a, a0, direction):
  '''Find value in a closest to a0. Returns its index and the value.
  
  * direction = -1: if a0 is not in a, choose closest, but smaller value
  * direction = 0: just choose closest
  * direction = +1: if a0 is not in a, choose closest, but larger value

  **NOTES**:
    * Only for ordered/sorted arrays.
    * Supports arrays with duplicate values.
  '''

  # convert to array
  a = array(a)

  # get index range closest to a0
  idx_list = numpy.flatnonzero(abs(a-a0)==min(abs(a-a0)))
  
  # select one index
  if a0 <= a[idx_list[0]]:
    idx = idx_list[0]
  else:
    idx = idx_list[-1]
  
  # handle cases
  if direction < 0 and a0 < a[idx] and idx-1 >= 0:
    return(idx-1, a[idx-1])
  elif direction > 0 and a[idx] < a0 and idx+1 < len(a):
    return(idx+1, a[idx+1])
  else:
    return(idx, a[idx])

def addDoubleQuotesIfMissing(orig):
  
  # simple solution
  orig_quoted = '"'+str(orig).strip('"').strip('\'')+'"'

  ## Complex solution as seen on: http://stackoverflow.com/questions/3584005/how-to-properly-add-quotes-to-a-string-using-python
  #Q = '"'
  #re_quoted_items = re.compile(r'" \s* [^"\s] [^"]* \"', re.VERBOSE)

  ## The orig string w/o the internally quoted items.
  #woqi = re_quoted_items.sub('', orig)

  #if len(orig) == 0:
    #orig_quoted = Q + orig + Q
  #elif len(woqi) > 0 and not (woqi[0] == Q and woqi[-1] == Q):
    #orig_quoted = Q + orig + Q    
  #else:
    #orig_quoted = orig

  return orig_quoted

# time utility functions from http://stackoverflow.com/questions/7065761/how-to-substract-two-datetime-time-values-in-django-template-and-how-to-format-a
def difft(start,end):
    ''' returns the difference in seconds between two datetime.time objects '''
    a,b,c,d = start.hour, start.minute, start.second, start.microsecond
    w,x,y,z = end.hour, end.minute, end.second, end.microsecond
    delt = (w-a)*60*60 + (x-b)*60 + (y-c) + (z-d)/pow(10,6)
    return delt + 24*60*60 if delt<0 else delt

def difft_string(start,end):
    ''' prints the difference between two datetime.time objects in a nice format '''
    delt = difft(start,end)

    hh,rem = divmod(delt,60*60)
    hh = int(hh)
    mm,rem = divmod(rem,60)
    mm = int(mm)
    ss = int(rem)
    ms = (rem - ss)*pow(10,6)
    ms = int(ms)

    SS = '%sh %smn %ss %sms'
    return SS % (hh,mm,ss,ms)
    
def todatetime(time):
    ''' converts a datetime.time object to a datetime.datetime object using the current date '''
    return datetime.datetime.today().replace(hour=time.hour, minute=time.minute, second=time.second, 
                                             microsecond=time.microsecond, tzinfo=time.tzinfo)

def timestodelta(starttime, endtime):
    ''' returns the difference in seconds between two datetime.time objects '''
    return todatetime(endtime) - todatetime(starttime)

# TODO: Start splitting up all those utilities into different files?
def rotation_matrix3(axis, theta):
  '''Returns a rotation matrix of size 3 to rotate something around vector v by angle theta.
  
  Usage::
  
    v = numpy.array([3,5,0])
    axis = numpy.array([4,4,1])
    theta = 1.2 
    print(numpy.dot(rotation_matrix3(axis,theta),v))
  
  source: http://stackoverflow.com/questions/6802577/python-rotation-of-3d-vector
  
  TODO: Replace with some existing complete geometry module???
  '''
  
  # this rotates the opposite way. Older version from website?:
  
  #axis = axis/numpy.sqrt(numpy.dot(axis,axis))
  #a = numpy.cos(theta/2)
  #b,c,d = -axis*numpy.sin(theta/2)
  #return numpy.array([[a*a+b*b-c*c-d*d, 2*(b*c-a*d), 2*(b*d+a*c)],
                   #[2*(b*c+a*d), a*a+c*c-b*b-d*d, 2*(c*d-a*b)],
                   #[2*(b*d-a*c), 2*(c*d+a*b), a*a+d*d-b*b-c*c]])

  axis = numpy.asarray(axis)
  theta = numpy.asarray(theta)
  L = math.sqrt(numpy.dot(axis, axis))
  if L==0:
    raise Exception('Unable to rotate around zero length axis.')
  axis = axis/L
  a = math.cos(theta/2.0)
  b, c, d = -axis*math.sin(theta/2.0)
  aa, bb, cc, dd = a*a, b*b, c*c, d*d
  bc, ad, ac, ab, bd, cd = b*c, a*d, a*c, a*b, b*d, c*d
  return numpy.array([[aa+bb-cc-dd, 2*(bc+ad), 2*(bd-ac)],
                   [2*(bc-ad), aa+cc-bb-dd, 2*(cd+ab)],
                   [2*(bd+ac), 2*(cd-ab), aa+dd-bb-cc]])

def rotation_matrix4(axis, theta):
  '''Returns a rotation matrix of size 4 to rotate something around vector v by angle theta.
  
  Usage::
  
    v = numpy.array([3,5,0])
    axis = numpy.array([4,4,1])
    theta = 1.2 
    print(numpy.dot(rotation_matrix(axis,theta),v))
  
  source: http://stackoverflow.com/questions/6802577/python-rotation-of-3d-vector
  
  .. todo:: Replace with some existing complete geometry module???
  '''
  axis = axis/numpy.sqrt(numpy.dot(axis,axis))
  a = numpy.cos(theta/2)
  b,c,d = -axis*numpy.sin(theta/2)
  return numpy.array([[a*a+b*b-c*c-d*d, 2*(b*c-a*d), 2*(b*d+a*c), 0],
                   [2*(b*c+a*d), a*a+c*c-b*b-d*d, 2*(c*d-a*b), 0],
                   [2*(b*d-a*c), 2*(c*d+a*b), a*a+d*d-b*b-c*c, 0],
                   [0,0,0,1]])

def Angle(p, q):
   ''' return the angle w.r.t. another 3-vector '''
   ptot2 = numpy.dot(p,p)*numpy.dot(q,q)
   if ptot2 <= 0:
      return 0.0
   else:
      arg = numpy.dot(p,q)/numpy.sqrt(ptot2)
      if arg >  1.0: arg =  1.0
      if arg < -1.0: arg = -1.0
      return numpy.arccos(arg)

def Orthogonal(u):
  '''
  get vector v orthogonal to u
  ex: v = Orthogonal(u)
  '''
  if u[0] < 0.0:
    xx = -u[0]
  else:
    xx = u[0]
  if u[1] < 0.0:
    yy = -u[1]
  else:
    yy = u[1]
  if u[2] < 0.0:
    zz = -u[2]
  else:
    zz = u[2]
  if (xx < yy):
    if xx < zz:
      return numpy.array([0,u[2],-u[1]])
    else:
      return numpy.array([u[1],-u[0],0])
  else:
    if yy < zz:
      return numpy.array([-u[2],0,u[0]])
    else:
      return numpy.array([u[1],-u[0],0])

def matlab_range(start, step, stop):
  '''
  Returns a list of values going from *start* to *stop* with a step *step*, but so that all values are less than OR EQUAL TO *stop*.
  i.e. it works like the matlab slice notation start:step:stop
  or like numpy.arange(start, stop, step) but with values on the closed interval [start, stop].
  
  .. todo:: Rewrite using an iterator or generator.
  .. todo:: Check Matlab official doc on how slicing works. (or octave code, or check all possible cases)
  .. todo:: Check if there is not already a similar function somewhere online/in numpy/elsewhere.
  '''
  if step == 0:
    return([])
  else:
    L = list(arange(start, stop, step))
    if len(L) > 0:
      nextval = L[-1] + step
    else:
      nextval = start
    if step > 0:
      if nextval <= stop:
        L.append(nextval)
    else:
      if nextval >= stop:
        L.append(nextval)
      
    return(L)

def checkSnapshotNumber(filename, verbose=False):
  '''
  Returns the number of snapshots and frequency snapshots in the file *filename*.

  :return: (N_time_snaps, N_freq_snaps)
  '''
  # check that we do not have too many snapshots
  with open(filename) as f:
    d = f.read()
    N_time_snaps = len(re.findall(r'^\s*SNAPSHOT\b',d, re.M))
    N_freq_snaps = len(re.findall(r'^\s*FREQUENCY_SNAPSHOT\b',d, re.M))

  #try:
    #N_time_snaps = int(subprocess.check_output(["grep", "--count", "--word-regexp", "SNAPSHOT", filename]))
  #except subprocess.CalledProcessError as err:
    #if err.returncode > 1:
      #raise
    #N_time_snaps = int(err.output)

  if verbose:
    print('N_time_snaps = {}, N_freq_snaps = {}'.format(N_time_snaps, N_freq_snaps))
  
  if N_time_snaps > 99 or N_freq_snaps > 99:
    raise Exception('More than 99 snapshots. This will not end well!!!')
  return (N_time_snaps, N_freq_snaps)

def unitVector(vec):
  vec = numpy.array(vec)
  mag = numpy.linalg.norm(vec)
  if mag == 0:
    return vec
  else:
    return vec/mag

#def splitRange(Nmax_global, Nmax_local):
  #'''
  #To split a range of Nmax_global elements into chunks no bigger than Nmax_local.
  
  #But numpy.array_split() is a much better existing solution!
  
  #cf:
    #http://stackoverflow.com/questions/24483182/python-split-list-into-n-chunks
    #http://stackoverflow.com/questions/312443/how-do-you-split-a-list-into-evenly-sized-chunks
    #http://stackoverflow.com/questions/2130016/splitting-a-list-of-arbitrary-size-into-only-roughly-n-equal-parts
  #'''
  #Nparts = int(ceil(Nmax_global/Nmax_local));
  #n2 = int(floor(Nmax_global/Nparts));
  #n1 = n2 + 1;
  #m1 = Nmax_global - n2*Nparts;
  #m2 = Nparts - m1;
  
  ##range(n1)
  ##range(n2)
  ##ret = [n1*ones(m1,1); n2*ones(m2,1)];
  
  ##msg = sprintf('sum(ret(:))=%d, Nsnaps=%d, max(ret(:))=%d, Nsnaps_max=%d\n', sum(ret(:)), Nsnaps, max(ret(:)), Nsnaps_max);
  ##%printf(msg);
  ##if (sum(ret(:)) ~= Nsnaps) || (max(ret(:)) > Nsnaps_max)
    ##error(msg);
  ##end
  ##return range_list
  #return

if __name__ == '__main__':
  pass
