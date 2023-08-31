#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# test data in: ~/DATA/MPB/k-point-import-tests
# example: ~/DATA/MPB/k-point-import-tests/test.out

import io
import os
import re
import sys
import code
import numpy
import argparse
import matplotlib
# import matplotlib.pyplot as plt # This causes problems when called from Matlab's system() function.
from utilities.common import float_array
import textwrap
import bfdtd

# ..todo:: nicer print format
# ..todo:: store lattices in transposed form for easier access to vectors?
# ..todo:: if, elif, else for matches? (should not have overlapping matches...)
# ..todo:: transpose not necessary if only 1 dim -> simplify dot product?
# ..todo:: merge with lattice class from h5utils + minimize attributes (reciprocal lattice can be calculated from lattice vectors). Check out MPB/MEEP code for reference.
# ..todo:: get name of epsilon output files from output
# ..todo:: plot bands, find gaps, etc (i.e. python version of plot_MPB())
# ..todo:: improve support for MPB split (each process outputs same because outputs are merged at end? but all joined into same file, so duplicate datasets are generated.)

class MPB_data():
  def __init__(self):
    self.lattice = numpy.eye(3)
    self.reciprocal_lattice = numpy.eye(3)
    self.k_points = []
    self.header = ['k index', 'k1', 'k2', 'k3', 'kmag/2pi']
    self.data = []
    self.eps_low = None
    self.eps_high = None
    self.eps_arithmetic_mean = None
    self.eps_harmonic_mean = None
    self.FF_bigger_than_one = None
    self.FF_mean_position = None
    self.gap_list = []
    self.geometry = []
    return

  # @property
  # def k_points(self):
  #       return self._k_points
  # @k_points.setter
  # def k_points(self, value):
  #   print('SETTER CALLED')
  #   self._k_points = value

  def __str__(self):
    (a0,a1,a2) = self.getLatticeVectors()
    (b0,b1,b2) = self.getReciprocalLatticeVectors()
    s='lattice:\n {}'.format(self.lattice)
    s+='\n a0 = {}'.format(a0)
    s+='\n a1 = {}'.format(a1)
    s+='\n a2 = {}'.format(a2)
    s+='\n Cell volume: {}'.format(self.getCellVolume())

    s+='\nreciprocal_lattice:\n {}'.format(self.reciprocal_lattice)
    s+='\n b0 = {}'.format(b0)
    s+='\n b1 = {}'.format(b1)
    s+='\n b2 = {}'.format(b2)
    s+='\n Reciprocal cell volume: {}'.format(self.getReciprocalCellVolume())

    s+='\n=== Geometry ==='
    for idx, obj in enumerate(self.geometry):
      s += f'\n->{idx}'
      s += f'\n{obj}'
    #   print(idx, ':', obj)
    s+='\n================'

    s+='\n epsilon: {}-{}, mean {}, harm. mean {}, {}% > 1, {}% "fill"'.format(self.eps_low,
                                                                              self.eps_high,
                                                                              self.eps_arithmetic_mean,
                                                                              self.eps_harmonic_mean,
                                                                              self.FF_bigger_than_one,
                                                                              self.FF_mean_position)

    s+='\nk_points:\n {}'.format(self.k_points)
    s+='\nheader = {}'.format(self.header)
    s+='\ndata:\n {}'.format(self.data)
    
    if len(self.gap_list) > 0:
      s+='\nBand gaps:\n'
      for i in self.gap_list:
        s += ' ' + i.__str__()
    else:
      s+='\nBand gaps: None'
    return(s)

  def getData(self):
    if not self.header:
      self.header = ['k index', 'k1', 'k2', 'k3', 'kmag/2pi']
    data = numpy.array(self.data, dtype={'names':self.header, 'formats':[int] + (len(self.header)-1)*[float]})
    return(data)
  
  def getBandData(self):
    header = ['k index', 'k1', 'k2', 'k3', 'kmag/2pi', 'kx', 'ky', 'kz', 'norm(k_cartesian)', 'angle(degrees)']
    data = []
    # print(self.data[5:])
    data = self.data
    print(self.data)
    print(list(zip(*self.data)))
    return(data)
  
  def getKpointData(self):
    # print('===================')
    header = ['k index', 'k1', 'k2', 'k3', 'kmag/2pi', 'kx', 'ky', 'kz', 'norm(k_cartesian)', 'angle(degrees)']
    
    k_point_data = []
    
    # print('=== self.k_points ===')
    # print(self.k_points)
    # print('-'*10)
    
    # for k_reciprocal in self.k_points:
    for idx, k_reciprocal in enumerate(self.k_points):
      #k_reciprocal_array = numpy.array(k_reciprocal).transpose() # no need because "1-dim array"
      k_cartesian = self.reciprocal_lattice.dot(k_reciprocal)

      L = numpy.linalg.norm(k_cartesian)
      if L > 0:
        theta_deg = numpy.rad2deg( numpy.arccos(k_cartesian[2]/L) )
      else:
        theta_deg = numpy.nan
      
      # print('{} or {} -> {}'.format(k_reciprocal, self.data[idx][0:5], k_cartesian))
      # t = (int(self.data[idx][0]), *self.data[idx][1:5], *k_cartesian, L, theta_deg)
      t = (*self.data[idx][0:5], *k_cartesian, L, theta_deg)
      # print(t)
      k_point_data.append(t)
      
    # print('-'*10)

    # print(len(k_point_data))
    # k_point_data = numpy.zeros(len(self.data), dtype={'names':header, 'formats':[int] + (len(header)-1)*[float]})
    k_point_data = numpy.array(k_point_data, dtype={'names':header, 'formats':[int] + (len(header)-1)*[float]})
    # k_point_data = numpy.zeros(numpy.zeros([3, len(header)], dtype={'names':header, 'formats':[int] + (len(header)-1)*[float]})


    # print('===================')
    return(k_point_data)

  def writeCSV(self, fname, extraInfo=True, sameFile=False):
    data = self.getData()
    (header, data) = writeDataToCSV(data, fname)

    if extraInfo:
      if not sameFile:
        (a,b) = os.path.splitext(fname)
        fname_extradata = a + '.extradata.csv'
        (header_kpoints, kpoints) = self.writeCSV_ExtraData(fname_extradata)
      else:
        import numpy.lib.recfunctions as rfn
        #remove common fields from data1 (simply change to data2 if you wish to remove from data2)
        common_fields = set(kpoints.dtype.names).intersection(set(data.dtype.names))
        data = data[[name for name in data.dtype.names if name not in common_fields]]

        arrays = [kpoints, data]
        m = rfn.merge_arrays(arrays, flatten = True)
        fname_merged = a + '.merged.csv'
        (header_merged, data_merged) = writeDataToCSV(m, fname_merged)
    
    return (header, data)
    
    # # format header entries for easier processing in other tools
    # header = []
    # for i in data.dtype.names:
      # header.append(i.replace('/','_over_').replace(' ','_'))
      
    # delimiter = '; '
    # comments = ''
    # fmt = ['%d']+(len(header)-1)*['%.18e']
    # numpy.savetxt(fname, data, delimiter=delimiter, header=delimiter.join(header), fmt=fmt, comments=comments)
    
    # if extraInfo and not sameFile:
      # kpoints = self.getKpointData()
      # numpy.savetxt(fname_extradata, kpoints, delimiter=delimiter, header=delimiter.join(header), fmt=fmt, comments=comments)
      
    # return (header, data)
    
  def writeCSV_ExtraData(self, fname):
    kpoints = self.getKpointData()
    return writeDataToCSV(kpoints, fname)
  
    # kpoints = self.getKpointData()
    # numpy.savetxt(fname, data, delimiter=delimiter, header=delimiter.join(header), fmt=fmt, comments=comments)

    # if extraInfo and not sameFile:
      # numpy.savetxt(fname, data, delimiter=delimiter, header=delimiter.join(header), fmt=fmt, comments=comments)

      # import os
      # import sys
      # import code
      # print('argv = {}'.format(sys.argv))

      # # # read in ~/.pystartup to have all the desired modules
      # # pystartup = os.path.expanduser("~/.pystartup")
      # # with open(pystartup) as f:
        # # code_object = compile(f.read(), pystartup, 'exec')
        # # exec(code_object)

      # # start the interactive shell
      # code.interact(local=locals())


    # return (header, data)

  def getLatticeVectors(self):
    a0 = self.lattice[:,0]
    a1 = self.lattice[:,1]
    a2 = self.lattice[:,2]
    return (a0,a1,a2)

  def getReciprocalLatticeVectors(self):
    b0 = self.reciprocal_lattice[:,0]
    b1 = self.reciprocal_lattice[:,1]
    b2 = self.reciprocal_lattice[:,2]
    return (b0,b1,b2)

  def getCellVolume(self):
    (a0,a1,a2) = self.getLatticeVectors()
    return abs(a0.dot(numpy.cross(a1,a2)))

  def getReciprocalCellVolume(self):
    (b0,b1,b2) = self.getReciprocalLatticeVectors()
    return abs(b0.dot(numpy.cross(b1,b2)))


  def get_kpoints_in_reciprocal_coordinates(self):
    return(self.k_points)

  def get_kpoints_in_cartesian_coordinates(self):
    '''returns the cartesian coordinates of the k-points'''
    k_path = []
    for k_reciprocal in self.k_points:
      #k_reciprocal_array = numpy.array(k_reciprocal).transpose() # no need because "1-dim array"
      k_cartesian = self.reciprocal_lattice.dot(k_reciprocal)
      k_path.append(k_cartesian)
    return(k_path)
    
  def get_data_kpoints_in_reciprocal_coordinates(self):
    k_path = []
    for data_line in self.data:
      k_path.append(data_line[1:4])
    return(k_path)

  def get_data_kpoints_in_cartesian_coordinates(self):
    k_path = []
    for data_line in self.data:
      k_reciprocal = numpy.array(data_line[1:4]).transpose()
      k_cartesian = self.reciprocal_lattice.dot(k_reciprocal)
      k_path.append(k_cartesian)
    return(k_path)

class MPB_Gap():
  lower_band = None
  gap_min = None
  upper_band = None
  gap_max = None
  gap_size = None
  def __init__(self, tuple5):
    (self.lower_band, self.gap_min, self.upper_band, self.gap_max, self.gap_size) = tuple5
  def __str__(self):
    return 'Gap from band {} ({}) to band {} ({}), {}%'.format(self.lower_band, self.gap_min, self.upper_band, self.gap_max, self.gap_size)

def parse_MPB(infile_flexible, verbosity=0, merge_datasets=False):
  '''
  Parses an MPB output ".out" file (command-line output from MPB).
  infile_flexible: A io.TextIOWrapper instance, as returned by f=open(path), or simply a filename string.
  Returns a list of **MPB_data** instances.

  TODO: Test/fix support for mpb split runs, with .out files including mutliple datasets.
  '''

  close_file = False
  if not isinstance(infile_flexible, io.TextIOWrapper):
    if isinstance(infile_flexible, str):
      infile = open(infile_flexible)
      close_file = True
    else:
      raise Exception(f'infile_flexible of type {type(infile_flexible)}, but should be of type io.TextIOWrapper or str.')
  else:
    infile = infile_flexible

  MPB_data_list = []
  gap_list = []

  lattice = numpy.eye(3)
  reciprocal_lattice = numpy.eye(3)
  k_points = []
  header = []
  data = []

  coord_pattern = '\s*\((.+),(.+),(.+)\)\s*'

  # default values
  eps_low = None
  eps_high = None
  eps_arithmetic_mean = None
  eps_harmonic_mean = None
  FF_bigger_than_one = None
  FF_mean_position = None

  for idx, line in enumerate(infile):
    
    lattice_match = re.match(r'Lattice vectors:', line)
    if lattice_match:
      if data:
        MPB_data_object = MPB_data()
        MPB_data_object.lattice = lattice
        MPB_data_object.reciprocal_lattice = reciprocal_lattice
        MPB_data_object.k_points = k_points
        MPB_data_object.header = header
        MPB_data_object.data = data
        MPB_data_list.append(MPB_data_object)
      for i in range(3):
        coord_line = infile.readline()
        try:
          coord_match = re.match(coord_pattern, coord_line)
          lattice[0,i] = float(coord_match.group(1))
          lattice[1,i] = float(coord_match.group(2))
          lattice[2,i] = float(coord_match.group(3))
        except:
          raise Exception('Failed to parse lattice vector. coord_line = {}'.format(coord_line))
      if verbosity>0:
        print('new lattice:\n {}'.format(lattice))
    
    reciprocal_lattice_match = re.match(r'Reciprocal lattice vectors \(/ 2 pi\):', line)
    if reciprocal_lattice_match:
      for i in range(3):
        coord_line = infile.readline()
        try:
          coord_match = re.match(coord_pattern, coord_line)
          reciprocal_lattice[0,i] = float(coord_match.group(1))
          reciprocal_lattice[1,i] = float(coord_match.group(2))
          reciprocal_lattice[2,i] = float(coord_match.group(3))
        except:
          raise Exception('Failed to parse reciprocal lattice vector. coord_line = {}'.format(coord_line))
      if verbosity>0:
        print('new reciprocal_lattice:\n {}'.format(reciprocal_lattice))

    ##### Read k-points
    '''
    CTL output:
      16 k-points:
       (0,0,0)
       (0.1,0,0)
    PY output:
      16 k-points
        Vector3<0.0, 0.0, 0.0>
        Vector3<0.1, 0.0, 0.0>
        Vector3<0.2, 0.0, 0.0>    
    '''
    k_points_match = re.match(r'(\d+) k-points:?', line)
    if k_points_match:
      Nkpoints = int(k_points_match.group(1))
      k_points = []
      for idx_k in range(Nkpoints):
        coord_line = infile.readline()
        try:
          coord_match = re.match(coord_pattern, coord_line)
          if coord_match is None:
            coord_match = re.match('\s*Vector3<([-+eE0-9.]+), ([-+eE0-9.]+), ([-+eE0-9.]+)>\s*', coord_line)
          k = [float(coord_match.group(1)), float(coord_match.group(2)), float(coord_match.group(3))]
          k_points.append(k)
        except:
          raise Exception('Failed to parse k point vector. coord_line = {}'.format(coord_line))
      if verbosity>0:
        print('new k_points:\n {}'.format(k_points))
    
    data_match = re.search('freqs:', line)
    if data_match:
      data_string = line.split(',')
      data_string = [i.strip() for i in data_string]
      if data_string[1]=='k index':
        header = data_string[1:]
        if verbosity>0:
          print('new header = {}'.format(header))
        data = []
      else:
        data_line = tuple(float_array(data_string[1:]))
        data.append(data_line)

    # fill factor line: Not generated when using python MPB
    fill_factor_match = re.match(r'epsilon: (\d+(?:\.\d+)?)-(\d+(?:\.\d+)?), mean (\d+(?:\.\d+)?), harm. mean (\d+(?:\.\d+)?), (\d+(?:\.\d+)?)% > 1, (\d+(?:\.\d+)?)% "fill"', line)
    if fill_factor_match:
      # cf mpb/mpb/epsilon.c
      eps_low = fill_factor_match.group(1)
      eps_high = fill_factor_match.group(2)
      eps_arithmetic_mean = fill_factor_match.group(3)
      eps_harmonic_mean = fill_factor_match.group(4)
      FF_bigger_than_one = fill_factor_match.group(5)
      FF_mean_position = fill_factor_match.group(6)

    gap_match = re.match(r'Gap from band (\d+) \((\d+(?:\.\d+)?)\) to band (\d+) \((\d+(?:\.\d+)?)\), (\d+(?:\.\d+)?)%', line)
    if gap_match:
      gap = MPB_Gap(gap_match.groups())
      gap_list.append(gap)

    geometric_objects_match = re.match(r'Geometric objects:', line)

  infile.seek(0)
  geo_obj_list = parseGeometryObjects(infile.read())

  MPB_data_object = MPB_data()
  MPB_data_object.lattice = lattice
  MPB_data_object.reciprocal_lattice = reciprocal_lattice
  MPB_data_object.k_points = k_points
  MPB_data_object.header = header
  MPB_data_object.data = data
  MPB_data_object.eps_low = eps_low
  MPB_data_object.eps_high = eps_high
  MPB_data_object.eps_arithmetic_mean = eps_arithmetic_mean
  MPB_data_object.eps_harmonic_mean = eps_harmonic_mean
  MPB_data_object.FF_bigger_than_one = FF_bigger_than_one
  MPB_data_object.FF_mean_position = FF_mean_position
  MPB_data_object.gap_list = gap_list
  MPB_data_object.geometry = geo_obj_list

  MPB_data_list.append(MPB_data_object)

  if close_file:
    infile.close()

  return(MPB_data_list)

def writeDataToCSV(data, fname):
  # a bit of a mess, but just to reduce code duplication in case more things need to be written...

  # format header entries for easier processing in other tools
  header = []
  for i in data.dtype.names:
    header.append(i.replace('/','_over_').replace(' ','_'))
    
  delimiter = '; '
  comments = ''
  fmt = ['%d']+(len(header)-1)*['%.18e']
  numpy.savetxt(fname, data, delimiter=delimiter, header=delimiter.join(header), fmt=fmt, comments=comments)
  
  return (header, data)

def writeCSV(infile, verbosity=0, merge_datasets=False):
  
  MPB_data_list = parse_MPB(infile, verbosity, merge_datasets=merge_datasets)

  if merge_datasets and len(MPB_data_list) > 0:
    merged_data = MPB_data_list[0]
    for idx, obj in enumerate(MPB_data_list[1:]):
      merged_data.data.extend(obj.data)

    MPB_data_list = [merged_data]

  (outfile_base, ext) = os.path.splitext(infile.name)

  for idx, obj in enumerate(MPB_data_list):
    print('=== dataset {} ==='.format(idx))
    if len(MPB_data_list) > 1:
      outfilename = '{}.{}.csv'.format(outfile_base, idx)
    else:
      outfilename = '{}.csv'.format(outfile_base)
    if obj.data:
      print('Writing data to {}'.format(outfilename))
      obj.writeCSV(outfilename)
    else:
      print('no data found')
    #with open(outfilename, 'w', newline='') as outfile:
      #writer = csv.writer(outfile)
      #writer.writerows(someiterable)
    #print(obj)
    #print('k points in cartesian coordinates:')
    #L = obj.get_kpoints_in_cartesian_coordinates()
    #for i in L:
      #print(i)

  #pystartup = os.path.expanduser("~/.pystartup")
  #with open(pystartup) as f:
    #code_object = compile(f.read(), pystartup, 'exec')
    #exec(code_object)

  #code.interact(local=locals())

  return

def printInfo(infile, verbosity=0, merge_datasets=False, angles=False):
  MPB_data_list = parse_MPB(infile, verbosity, merge_datasets=merge_datasets)
  
  for idx, obj in enumerate(MPB_data_list):
    print('=== dataset {} ==='.format(idx))
    print(obj)
    if not angles:
      print('k points in cartesian coordinates:')
    else:
      print('k points in cartesian coordinates; angle between k and Z in degrees:')
    L = obj.get_kpoints_in_cartesian_coordinates()
    for i in L:
      if not angles:
        print(i)
      else:
        if numpy.linalg.norm(i) > 0:
          theta_deg = numpy.rad2deg( numpy.arccos(i[2]/numpy.linalg.norm(i)) )
        else:
          theta_deg = numpy.nan
        print('{}; {}'.format(i, theta_deg))
    if angles:
      print('angle between k and Z in degrees:')
      for i in L:
        if numpy.linalg.norm(i) > 0:
          theta_deg = numpy.rad2deg( numpy.arccos(i[2]/numpy.linalg.norm(i)) )
        else:
          theta_deg = numpy.nan
        print(theta_deg)
    
  return

def subcommand_writeCSV(args):
  writeCSV(args.infile, args.verbosity, args.merge_datasets)
  return

def subcommand_printInfo(args):
  printInfo(args.infile, args.verbosity, args.merge_datasets, args.angles)
  return

def subcommand_interactive(args):
  MPB_data_list = parse_MPB(args.infile, args.verbosity, merge_datasets=args.merge_datasets)
  for idx, obj in enumerate(MPB_data_list):
    data = obj.getData()
    kpoints = obj.getKpointData()


    # import os
    # import sys
    # import code
    # print('argv = {}'.format(sys.argv))

    # read in ~/.pystartup to have all the desired modules (and tab completion)
    pystartup = os.path.expanduser("~/.pystartup")
    with open(pystartup) as f:
      code_object = compile(f.read(), pystartup, 'exec')
      exec(code_object)

    # start the interactive shell
    code.interact(local=locals())

  return

def subcommand_plotMPB(args):
  import pandas
  
  # parse input file
  MPB_data_list = parse_MPB(args.infile, args.verbosity, merge_datasets=args.merge_datasets)
  
  # merge multiple datasets into one if requested
  if args.merge_datasets and len(MPB_data_list) > 0:
    merged_data = MPB_data_list[0]
    for idx, obj in enumerate(MPB_data_list[1:]):
      merged_data.data.extend(obj.data)
  
    MPB_data_list = [merged_data]
  
  # get path components
  (outfile_base, ext) = os.path.splitext(args.infile.name)

  if not args.saveas=='':
    outfile_base = args.saveas
  
  # loop through the list of **MPB_data** instances
  for idx, obj in enumerate(MPB_data_list):
    print('=== dataset {} ==='.format(idx))
    if len(MPB_data_list) > 1:
      outfilename = '{}.{}.csv'.format(outfile_base, idx)
      pngfilename = '{}.{}.png'.format(outfile_base, idx)
    else:
      outfilename = '{}.csv'.format(outfile_base)
      pngfilename = '{}.png'.format(outfile_base)
    if obj.data:
      # print(obj.data)
      # print(numpy.shape(obj.data))
      # print(obj.getData())
      
      # print(obj.getBandData())
      # raise
      data = obj.getData()
      kpoints = obj.getKpointData()
      
      # print(a)
      # print(pandas.DataFrame(a, index=range(len(a)), columns=a.dtype.names))
      if args.x_range_auto:
        x_range = []
      else:
        x_range = args.x_range
      if args.y_range_auto:
        y_range = []
      else:
        y_range = args.y_range
      if args.title:
        title=args.title
      else:
        title=args.infile.name
      plotMPB(kpoints, data, title=title, a=args.a, saveas=pngfilename, show=not args.no_show, x_range=x_range, y_range=y_range, y_lambda=args.y_lambda, x_as_index=args.x_as_index, invert_yaxis=args.invert_yaxis, y_divisions=args.y_divisions)
    else:
      print('no data found')

  # https://stackoverflow.com/questions/48129222/matplotlib-make-plots-in-functions-and-then-add-each-to-a-single-subplot-figure
  # fig, (ax1, ax2) = plt.subplots(1,2)
  # plot_something([1,2,3], [2,4,6], ax1, color='blue')
  # plot_something([1,2,3], [1,4,9], ax2, color='red')
  # plt.figure()
  # plot_something([1,2,3], [1,4,9], ax=None, color='red')
  # plt.show()

  return

def plot_something(x, y, ax=None, **kwargs):
    import matplotlib.pyplot as plt
    ax = ax or plt.gca()
    # Do some cool data transformations...
    return ax.plot(x, y, **kwargs)

def plotMPB(kpoints, data, a = 1, title='', saveas='', show=True, x_range=[], y_range=[], y_lambda=False, x_as_index=False, invert_yaxis=False, y_divisions=8):

  # if not showing plots, avoid using X server, as it can be problematic
  # cf: https://stackoverflow.com/questions/4931376/generating-matplotlib-graphs-without-a-running-x-server
  if not show:
    import matplotlib as mpl
    mpl.use('Agg')

  import matplotlib.pyplot as plt
  
  fig = plt.figure()
  # print(len(kpoints), len(data))
  # x = numpy.linspace(0, 2, 100)
  # print(type(kpoints))
  # print(kpoints.dtype.names)
  if x_as_index:
    x = kpoints['k index']
  else:
    x = kpoints['angle(degrees)']
  x_no_nan = x[numpy.isfinite(x)]
  print('angle range:{} - {} degrees'.format(min(x_no_nan), max(x_no_nan)))

  # print(numpy.array(data))
  # print(data['band 1'])
  # data = numpy.array(data)
  # print(data[:][:][2])
  band_names = data.dtype.names[5:]
  
  dataout = []

  fn_all = []
  Lambda_all = []
  y_all = []
  for idx in range(len(band_names)):
    # print(band_names[idx])
    fn = data[band_names[idx]]
    Lambda = a / fn
    fn_all.extend(fn)
    Lambda_all.extend(Lambda)
    if y_lambda:
      y = Lambda
    else:
      y = fn
    y_all.extend(y)
    plt.plot(x, y, 'k--', label=band_names[idx])

  y_all = numpy.array(y_all)
  fn_all = numpy.array(fn_all)
  Lambda_all = numpy.array(Lambda_all)
  
  y_all_no_nan = y_all[numpy.isfinite(y_all)]
  fn_all_no_nan = fn_all[numpy.isfinite(fn_all)]
  Lambda_all_no_nan = Lambda_all[numpy.isfinite(Lambda_all)]
  print('fn range:{} - {}'.format(min(fn_all_no_nan), max(fn_all_no_nan)))
  print('Lambda range:{} - {} um'.format(min(Lambda_all_no_nan), max(Lambda_all_no_nan)))
  print('y range:{} - {}'.format(min(y_all_no_nan), max(y_all_no_nan)))
  
  if x_range:
    xmin = x_range[0]
    xmax = x_range[1]
    # plt.xlim(0, 45)
  else:
    xmin = min(x_no_nan)
    xmax = max(x_no_nan)

  if y_range:
    ymin = y_range[0]
    ymax = y_range[1]
    # plt.ylim(0.9, 1.7)
  else:
    ymin = min(y_all_no_nan)
    ymax = max(y_all_no_nan)
  
  plt.xlim(xmin, xmax)
  plt.ylim(ymin, ymax)
  
  ax = plt.gca()
  if invert_yaxis:
    ax.invert_yaxis()
  
  # ax.xaxis.set_minor_locator(matplotlib.ticker.MultipleLocator(7.5))
  # ax.xaxis.set_major_locator(matplotlib.ticker.MultipleLocator(15))
  ax.xaxis.set_major_locator(matplotlib.ticker.MultipleLocator( abs(xmax-xmin)/3 ))
  ax.xaxis.set_minor_locator(matplotlib.ticker.MultipleLocator( abs(xmax-xmin)/3/2 ))
  
  # ax.yaxis.set_minor_locator(matplotlib.ticker.MultipleLocator(0.05))
  # ax.yaxis.set_major_locator(matplotlib.ticker.MultipleLocator(0.1))

  ax.yaxis.set_minor_locator(matplotlib.ticker.MultipleLocator(abs(ymax-ymin)/y_divisions/2))
  ax.yaxis.set_major_locator(matplotlib.ticker.MultipleLocator(abs(ymax-ymin)/y_divisions))
  if y_lambda:
    # ax.yaxis.set_minor_locator(matplotlib.ticker.MultipleLocator(0.05))
    # ax.yaxis.set_major_locator(matplotlib.ticker.MultipleLocator(0.1))
    plt.ylabel('Wavelength (µm)')
  else:
    plt.ylabel('Normalized frequency (a/λ)')

  if x_as_index:
    plt.xlabel('k index')
  else:
    plt.xlabel('Angle (degrees)')
  
  if title:
    plt.title(title)
  
  if saveas:
    plt.savefig(saveas)
  
  if show:
    plt.show()
  
  return

def main():
  parser = argparse.ArgumentParser(formatter_class=argparse.RawDescriptionHelpFormatter,
                                   description=textwrap.dedent('''\
                                   Parse output from MPB and Python-MPB, i.e. ".out" files obtained using:
                                       mpb example.ctl > example.out
                                     or:
                                       python mpb_example.py > example.out
                                  '''))
  parser.add_argument('-n', '--dry-run', action='store_true')
  parser.add_argument('-v', '--verbose', action='count', dest='verbosity', default=0)
  parser.add_argument('-m', '--merge-datasets', action='store_true')
  parser.add_argument('-a', '--angles', action='store_true', help='print the angles in degrees of k relative to the Z axis')
  parser.add_argument('--saveas', default='', help='basename for output files. Example: "foo" -> "foo.csv", "foo.png"')
  parser.add_argument('infile', type=argparse.FileType('r'), metavar='INFILE', help='.out file to parse')

  subparsers = parser.add_subparsers(help='Available subcommands', dest='chosen_subcommand')

  parser_printInfo = subparsers.add_parser('printInfo', help='Print info based on infile.')
  parser_printInfo.set_defaults(func=subcommand_printInfo)

  # TODO: Add formatting options? presets like .prn reader compatible format?
  parser_writeCSV = subparsers.add_parser('writeCSV', help='Write data from outfile to one CSV file per dataset.')
  parser_writeCSV.set_defaults(func=subcommand_writeCSV)

  # – VIS: 340 - 800 nm
  # – IR: 899.343 - 1712.280 nm 
  parser_plot = subparsers.add_parser('plot', help='plot data')
  parser_plot.add_argument('--no-show', action='store_true')
  parser_plot.add_argument('--x-as-index', action='store_true', help='Use k index on the X axis instead of angle.')
  parser_plot.add_argument('--y-lambda', action='store_true', help='Use lambda on the Y axis instead of normalized frequency.')
  parser_plot.add_argument('--x-range-auto', action='store_true')
  parser_plot.add_argument('--y-range-auto', action='store_true')
  parser_plot.add_argument('--invert-yaxis', action='store_true')
  parser_plot.add_argument('-a', default=1, type=float)
  parser_plot.add_argument('--title', default='')
  parser_plot.add_argument('--x-range', nargs=2, default=[0, 45], metavar=('MIN', 'MAX'), type=float)
  parser_plot.add_argument('--y-range', nargs=2, default=[0.9, 1.7], metavar=('MIN', 'MAX'), type=float)
  parser_plot.add_argument('--y-divisions', type=int, default=8, help='number of divisions on the Y axis (default: 8)')
  parser_plot.set_defaults(func=subcommand_plotMPB)
  
  parser_interactive = subparsers.add_parser('interactive', help='start interactive prompt with data loaded')
  parser_interactive.set_defaults(func=subcommand_interactive)
    
  args = parser.parse_args()
  
  if args.dry_run:
    if args.verbosity > 0:
      print(args)
    return

  if not args.chosen_subcommand:
    args.chosen_subcommand='printInfo'
    args.func=subcommand_printInfo
  
  args.func(args)
      
  return(0)

# We could use the python MPB objects, but then python-meep needs to be set up, which is not always easy.
class mpbMaterial():
  epsilon = 1
  mu = 1

class mpbGeometricObject():
  material = mpbMaterial()
  center = [0,0,0]

class mpbSphere(mpbGeometricObject):
  def __init__(self, center=[0,0,0], radius=1, material=mpbMaterial()):
    self.center = center
    self.radius = radius
    self.material = material

def parseGeometryObjects(s):
  '''
  Parses a string for geometry objects and returns them as a list of *bfdtd.GeometryObject* objects.
  Objects that are not yet supported will be returned as *None*.

  The input string needs to contain a section of the form:
  "Geometric objects:
    ...
  Geometric object tree..."

  TODO: Convert to cartesian coordinates? -> At the moment, everything is passed as if in a cartesian lattice!
  TODO: Custom MPB objects? Or use MPB module? -> Harder to set up.
  '''
  p = re.compile('Geometric objects:.*Geometric object tree', re.DOTALL)
  # print(p.search(s).group(0))
  s = p.search(s).group(0)


  # p = re.compile('sphere, center = (1, 0, 0)\s+radius\s+0.25\s+epsilon = 12, mu = 1', re.DOTALL)
  # n = '([-+.eE0-9]+)'
  # p = re.compile('sphere, center = \(([-+.0-9]+),([-+.0-9]+),([-+.0-9]+)\)\s+radius ', re.DOTALL)
  # print(p.findall(s))
  # p = re.compile(f'sphere, center = \({n},{n},{n}\)\s+radius {n}', re.DOTALL)
  # print(p.findall(s))
  # p = re.compile(f'sphere, center = \({n},{n},{n}\)\s+radius {n}\s+epsilon = {n}, mu = {n}', re.DOTALL)
  # print(p.findall(s))
  # print('----')
  # p = re.compile(f'sphere, center = \({n},{n},{n}\)\s+radius {n}(\s+epsilon = {n}, mu = {n})?', re.DOTALL)
  # print(p.findall(s))

  # re.search('     [a-z]+,.*\n', s)
  geo_str_list = re.findall('\s{5}[a-z]+,.*\n(?:\s{10}.*\n)+', s)
  # print(geo_str_list)
  # print(len(geo_str_list))

  # import bfdtd

  geo_obj_list = []
  for s in geo_str_list:
    m = re.match('\s{5}([a-z]+),', s)
    obj_type = m.groups()[0]
    # print(obj_type)
    if obj_type == 'sphere':
      geo_obj_list.append(parseSphere(s))
    elif obj_type == 'cylinder':
      geo_obj_list.append(parseCylinder(s))
    elif obj_type == 'block':
      geo_obj_list.append(parseBlock(s))
    else:
      geo_obj_list.append(None)

  return geo_obj_list

def parseVector(s):
  n = '[-+.eE0-9]+'
  v = f'\(({n}),\s*({n}),\s*({n})\)'
  m = re.match(v,s)
  # print(m.groups())
  vec = [float(i) for i in m.groups()]
  return vec

def parseSphere(s):
  n = '([-+.eE0-9]+)'
  m = re.match(f'\s{{5}}sphere, center = \({n},{n},{n}\)\s+radius {n}(\s+epsilon = {n}, mu = {n})?', s, re.DOTALL)
  if m is None:
    print(s)
    raise
  obj = bfdtd.Sphere()
  obj.setLocation([float(i) for i in [m.group(1), m.group(2), m.group(3)]])
  obj.setOuterRadius(float(m.group(4)))
  epsilon = m.group(6)
  mu = m.group(7)
  if epsilon is not None:
    obj.setRelativePermittivity(float(epsilon))
  if mu is not None:
    obj.setRelativeConductivity(float(mu))
  return obj

def parseCylinder(s):
  n = '([-+.eE0-9]+)'
  m = re.match(f'\s{{5}}cylinder, center = \({n},{n},{n}\)\s+radius {n}, height {n}, axis \({n}, {n}, {n}\)(\s+epsilon = {n}, mu = {n})?', s, re.DOTALL)
  if m is None:
    print(s)
    raise
  obj = bfdtd.Cylinder()
  obj.setLocation([float(i) for i in [m.group(1), m.group(2), m.group(3)]])
  obj.setOuterRadius(float(m.group(4)))
  obj.setHeight(float(m.group(5)))
  obj.setAxis([float(i) for i in [m.group(6), m.group(7), m.group(8)]])
  epsilon = m.group(10)
  mu = m.group(11)
  if epsilon is not None:
    obj.setRelativePermittivity(float(epsilon))
  if mu is not None:
    obj.setRelativeConductivity(float(mu))
  return obj

def parseBlock(s):
  n = '[-+.eE0-9]+'
  v = f'\({n},\s*{n},\s*{n}\)'
  m = re.match(f'\s{{5}}block, center = (?P<center>{v})\s+size (?P<size>{v})\s+axes (?P<e1>{v}), (?P<e2>{v}), (?P<e3>{v})(\s+epsilon = (?P<epsilon>{n}), mu = (?P<mu>{n}))?', s, re.DOTALL)
  if m is None:
    print(s)
    raise

  obj = bfdtd.Parallelepiped()
  obj.setLocation(parseVector(m.group('center')))
  obj.setSize(parseVector(m.group('size')))
  obj.setAxes( parseVector(m.group('e1')), parseVector(m.group('e2')), parseVector(m.group('e3')))

  if m.group('epsilon') is not None:
    obj.setRelativePermittivity(float(m.group('epsilon')))
  if m.group('mu') is not None:
    obj.setRelativeConductivity(float(m.group('mu')))
  return obj

if __name__ == '__main__':
  main()
