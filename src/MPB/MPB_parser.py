#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# test data in: ~/DATA/MPB/k-point-import-tests
# example: ~/DATA/MPB/k-point-import-tests/test.out

import os
import re
import sys
import code
import numpy
import argparse
import matplotlib
# import matplotlib.pyplot as plt # This causes problems when called from Matlab's system() function.
from utilities.common import float_array

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
    self.gap_list = None
    return
    
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

def parse_MPB(infile, verbosity=0, merge_datasets=False):
  '''
  Parses an MPB output ".out" file (command-line output from MPB).
  Returns a list of **MPB_data** instances.
  '''

  MPB_data_list = []
  gap_list = []

  lattice = numpy.eye(3)
  reciprocal_lattice = numpy.eye(3)
  k_points = []
  header = []
  data = []

  coord_pattern = '\s*\((.+),(.+),(.+)\)\s*'

  for idx, line in enumerate(infile):
    
    #print(idx, line)

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
    
    k_points_match = re.match(r'(\d+) k-points:', line)
    if k_points_match:
      Nkpoints = int(k_points_match.group(1))
      k_points = []
      for idx_k in range(Nkpoints):
        coord_line = infile.readline()
        try:
          coord_match = re.match(coord_pattern, coord_line)
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

    fill_factor_match = re.match(r'epsilon: (\d+(?:\.\d+)?)-(\d+(?:\.\d+)?), mean (\d+(?:\.\d+)?), harm. mean (\d+(?:\.\d+)?), (\d+(?:\.\d+)?)% > 1, (\d+(?:\.\d+)?)% "fill"', line)
    if fill_factor_match:
      # output-nrod_2.40.nbg_1.00/nrod_2.40.nbg_1.00.rn_0.21.out
      # epsilon: 1-5.76, mean 3.84056, harm. mean 2.05085, 65.4663% > 1, 59.6756% "fill"
      # epsilon: 1-1, mean 1, harm. mean 1, 0% > 1, 100% "fill"

      # from mpb/mpb/epsilon.c :
      # mpi_one_printf("epsilon: %g-%g, mean %g, harm. mean %g, "
      # "%g%% > 1, %g%% \"fill\"\n",
      # eps_low, eps_high, eps_mean, eps_inv_mean,
      # (100.0 * fill_count) / N, 
      # eps_high == eps_low ? 100.0 :
      # 100.0 * (eps_mean-eps_low) / (eps_high-eps_low));
      # N = mdata->nx * mdata->ny * mdata->nz;
      # eps_mean /= N;
      # // arithmetic mean
      # eps_mean = eps_mean/N;
      # // harmonic mean
      # eps_inv_mean = N/eps_inv_mean;
      # if (epsilon[i] > 1.0001) ++fill_count;
      # mpi_one_printf("epsilon: %g-%g, mean %g, harm. mean %g, %g%% > 1, %g%% \"fill\"\n",
      # eps_low,
      # eps_high,
      # eps_mean,
      # eps_inv_mean,
      # (100.0 * fill_count) / N, // how many percent have eps > 1.0001
      # eps_high == eps_low ? 100.0 : 100.0 * (eps_mean-eps_low) / (eps_high-eps_low));
      # if eps_high == eps_low:
      #   100.0
      # else:
      #   100.0 * (eps_mean-eps_low) / (eps_high-eps_low));
      eps_low = fill_factor_match.group(1)
      eps_high = fill_factor_match.group(2)
      eps_arithmetic_mean = fill_factor_match.group(3)
      eps_harmonic_mean = fill_factor_match.group(4)
      FF_bigger_than_one = fill_factor_match.group(5)
      FF_mean_position = fill_factor_match.group(6)

    # gap_match = re.match(r'epsilon: (\d+(?:\.\d+)?)-(\d+(?:\.\d+)?), mean (\d+(?:\.\d+)?), harm. mean (\d+(?:\.\d+)?), (\d+(?:\.\d+)?)% > 1, (\d+(?:\.\d+)?)% "fill"', line)
    gap_match = re.match(r'Gap from band (\d+) \((\d+(?:\.\d+)?)\) to band (\d+) \((\d+(?:\.\d+)?)\), (\d+(?:\.\d+)?)%', line)    
    if gap_match:
      # Gap from band 2 (0.5131975478560308) to band 3 (0.515014566007033), 0.3534325508334174%
      # print(line)
      # print(gap_match.groups())
      gap = MPB_Gap(gap_match.groups())
      # print(gap)
      gap_list.append(gap)
      
      # (lower_band, gap_min, upper_band, gap_max, gap_size) = gap_match.groups()
      # print((lower_band, gap_min, upper_band, gap_max, gap_size))
      # raise Exception('GAGGA')


    geometric_objects_match = re.match(r'Geometric objects:', line)
    #if geometric_objects_match:
      #raise
      #p=re.compile('Geometric objects:.*Geometric object tree', re.DOTALL)
      #print(p.search(s).group(0))
      #raise
     #sphere, center = (0,0,0)
          #radius 1
          #dielectric constant epsilon = 12
     #cylinder, center = (0,0,0)
          #radius 1, height 2, axis (0.381, 0.508001, 0.635001)
          #dielectric constant epsilon = 12
     #cone, center = (0,0,0)
          #radius 1, height 2, axis (0.381, 0.508001, 0.635001)
          #radius2 6
          #dielectric constant epsilon = 12
     #block, center = (0,0,0)
          #size (1,2,3)
          #axes (0.406138,0.507673,0.609208), (0.442719,0.505964,0.56921), (0.458831,0.504715,0.550598)
          #dielectric constant epsilon = 12
     #ellipsoid, center = (0,0,0)
          #size (1,2,3)
          #axes (0.406138,0.507673,0.609208), (0.442719,0.505964,0.56921), (0.458831,0.504715,0.550598)
          #dielectric constant epsilon = 12

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
  MPB_data_list.append(MPB_data_object)

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
  parser = argparse.ArgumentParser()
  parser.add_argument('-n', '--dry-run', action='store_true')
  parser.add_argument('-v', '--verbose', action='count', dest='verbosity', default=0)
  parser.add_argument('-m', '--merge-datasets', action='store_true')
  parser.add_argument('-a', '--angles', action='store_true', help='print the angles in degrees of k relative to the Z axis')
  parser.add_argument('--saveas', default='', help='basename for output files. Example: "foo" -> "foo.csv", "foo.png"')
  parser.add_argument('infile', type=argparse.FileType('r'))

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

if __name__ == '__main__':
  main()
