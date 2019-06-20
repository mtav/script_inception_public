#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import io
import os
import re
import sys
import code
import numpy
import argparse
import subprocess
import tempfile
import textwrap

from utilities.common import float_array
from MPB.MPB_parser import MPB_data

import bfdtd.GeometryObjects

float_pattern = '\s*((?:[\de.-]|\+)+)\s*'
vector_pattern = '\({},{},{}\)'.format(float_pattern, float_pattern, float_pattern)

# TODO: nicer print format
# TODO: store lattices in transposed form for easier access to vectors?
# TODO: if, elif, else for matches? (should not have overlapping matches...)
# TODO: transpose not necessary if only 1 dim -> simplify dot product?
# TODO: merge with lattice class from h5utils + minimize attributes (reciprocal lattice can be calculated from lattice vectors). Check out MPB/MEEP code for reference.

class MEEP_data(MPB_data):
  def __init__(self):
    super(MPB_data, self).__init__() # python 2+3 compatible super() call
    self.size = None
    self.resolution = None
    self.header = ['frequency, transmitted_flux, reflected_flux']
    self.data = []
    return
    
  def __str__(self):
    s='size = {}\n'.format(self.size)
    s='resolution = {}\n'.format(self.resolution)
    s+='header = {}\n'.format(self.header)
    s+='data:\n {}'.format(self.data)
    return(s)

  def getData(self):
    if not self.header:
      self.header = ['frequency, transmitted_flux, reflected_flux']
    data = numpy.array(self.data, dtype={'names':self.header, 'formats':[int] + (len(self.header)-1)*[float]})
    return(data)

  def writeCSV(self, fname):
    
    data = self.getData()
    
    # format header entries for easier processing in other tools
    header = []
    for i in data.dtype.names:
      header.append(i.replace('/','_over_').replace(' ','_'))
      
    delimiter = '; '
    comments = ''
    fmt = len(header)*['%.18e']
    
    numpy.savetxt(fname, data, delimiter=delimiter, header=delimiter.join(header), fmt=fmt, comments=comments)
    return (header, data)

def parse_MEEP(infile, verbosity=0):

  MEEP_data_list = []

  lattice = numpy.eye(3)
  reciprocal_lattice = numpy.eye(3)
  k_points = []
  header = []
  data = []

  coord_pattern = '\s*\((.+),(.+),(.+)\)\s*'

  for idx, line in enumerate(infile):
    
    #print(idx, line)

    computational_cell_match = re.match(r'Computational cell is ([\d.]+) x ([\d.]+) x ([\d.]+) with resolution (\d+)', line)
    if computational_cell_match:
      print(computational_cell_match.group(0))
      print(computational_cell_match.groups())
      lattice[0,0] = float(computational_cell_match.group(1))
      lattice[1,1] = float(computational_cell_match.group(2))
      lattice[2,2] = float(computational_cell_match.group(3))

    lattice_match = re.match(r'Lattice vectors:', line)
    if lattice_match:
      if data:
        MEEP_data_object = MEEP_data()
        MEEP_data_object.lattice = lattice
        MEEP_data_object.reciprocal_lattice = reciprocal_lattice
        MEEP_data_object.k_points = k_points
        MEEP_data_object.header = header
        MEEP_data_object.data = data
        MEEP_data_list.append(MEEP_data_object)
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

  MEEP_data_object = MEEP_data()
  MEEP_data_object.lattice = lattice
  MEEP_data_object.reciprocal_lattice = reciprocal_lattice
  MEEP_data_object.k_points = k_points
  MEEP_data_object.header = header
  MEEP_data_object.data = data
  MEEP_data_list.append(MEEP_data_object)

  return(MEEP_data_list)

def writeCSV(infile, verbosity=0):
  
  MEEP_data_list = parse_MEEP(infile, verbosity)

  (outfile_base, ext) = os.path.splitext(infile.name)

  for idx, obj in enumerate(MEEP_data_list):
    print('=== dataset {} ==='.format(idx))
    if len(MEEP_data_list) > 1:
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

def getInfoFromOutFile(infile, verbosity=0):
  MEEP_data_list = parse_MEEP(infile, verbosity=verbosity)
  geo_list = parseGeometry(infile, verbosity=verbosity)
  return (MEEP_data_list, geo_list)

def printInfo(MEEP_data_list, geo_list, verbosity=0):
  for idx, obj in enumerate(MEEP_data_list):
    print('=== dataset {} ==='.format(idx))
    print(obj)
    print('k points in cartesian coordinates:')
    L = obj.get_kpoints_in_cartesian_coordinates()
    for i in L:
      print(i)
  if verbosity > 0:
    for idx, obj in enumerate(geo_list):
      print('====================')
      print('idx = {}'.format(idx))
      print('--------------------')
      print(obj)
      print('====================')
  return (MEEP_data_list, geo_list)

def subcommand_writeCSV(args):
  writeCSV(args.infile, args.verbosity)  
  return

def subcommand_printInfo(args):
  for i in args.infile:
    if args.ctl:
      (MEEP_data_list, geo_list) = getInfoFromCTL(i.name, verbosity=args.verbosity)
    else:
      (MEEP_data_list, geo_list) = getInfoFromOutFile(i, verbosity=args.verbosity)
    printInfo(MEEP_data_list, geo_list, verbosity=args.verbosity)
  return

def vectorstr2float(s):
  # p = re.compile('\(\s*([\de.-]+)\s*,\s*([\de.-]+)\s*,\s*([\de.-]+)\s*\)')
  p = re.compile(vector_pattern)
  m = p.match(s.strip())
  if m is None:
    raise Exception('Failed to match: {}'.format(s))
  v = [float(i) for i in m.groups()]
  return(v)

def parseGeometryObject(txt, verbosity=0):
  if verbosity > 0:
    print('---------')
    print(txt)
    print('---------')
  #generic_pattern = re.compile('\s*([a-z]+), center = \(([\d.]+),([\d.]+),([\d.]+)\)\s*?(.*?)\s*?dielectric constant epsilon diagonal = \(([\d.]+),([\d.]+),([\d.]+)\)\s*', re.DOTALL)
  #generic_pattern = re.compile('\s*([a-z]+), center = \(([\d.]+),([\d.]+),([\d.]+)\)\s*?(.*?)\s*?dielectric constant epsilon diagonal = \(([\d.]+),([\d.]+),([\d.]+)\)\s*', re.DOTALL)
  generic_pattern = re.compile('\s*(?P<type>[a-z]+), center = \((?P<centre_x>[\de.-]+),(?P<centre_y>[\de.-]+),(?P<centre_z>[\de.-]+)\)\s*?(?P<type_specific>.*?)\s*?(?P<diel_text>dielectric constant epsilon diagonal|dielectric constant epsilon) = (?P<diel_value>[\d.,()-]+)\s*', re.DOTALL)
  m = generic_pattern.search(txt)
#  print(m)
#  print(m.group(0))
#  print(m.groups())
#  print(m.group('type'))
#  print(m.group('centre_x'))
#  print(m.group('centre_y'))
#  print(m.group('centre_z'))
#  print(m.group('diel_text'))
#  print(m.group('diel_value'))
#  print(m.group('type_specific'))
#  print('---------')
  
  obj_type = m.group('type')
  centre_x = float(m.group('centre_x'))
  centre_y = float(m.group('centre_y'))
  centre_z = float(m.group('centre_z'))
  location = [centre_x, centre_y, centre_z]
  if 'diagonal' in m.group('diel_text'):
#    print('DIAGONAL')
#    print(m.group('diel_value'))
#    vector_pattern = re.compile('\(\s*([0-9.]+)\s*,\s*([0-9.]+)\s*,\s*([0-9.]+)\s*\)')
#    v = vector_pattern.match(m.group('diel_value').strip())
#    permittivity = [float(i) for i in v.groups()]
    permittivity = vectorstr2float(m.group('diel_value'))
#    permittivity = float()
  else:
#    print('SCALAR')
    permittivity = 3*[float(m.group('diel_value'))]
    
#  print('permittivity = {}'.format(permittivity))
#  print('location = {}'.format(location))
  
  obj = None
  type_specific_txt = m.group('type_specific').strip()
#  print(type_specific_txt)
  
  # float_pattern = '\s*((?:[\de.-]|\+)+)\s*'
  # vector_pattern = '\({},{},{}\)'.format(float_pattern, float_pattern, float_pattern)
  
  if obj_type == 'sphere':
    obj = bfdtd.GeometryObjects.Sphere()
    type_specific_pattern = re.compile('radius ([\d.]+)')
    type_specific_match = type_specific_pattern.match(type_specific_txt)
    obj.setOuterRadius(float(type_specific_match.group(1)))
  elif obj_type == 'cylinder':
    obj = bfdtd.Cylinder()
    type_specific_pattern = re.compile('radius (?P<radius>[\d.]+), height (?P<height>[\d.]+), axis (?P<axis>{vector_pattern})'.format(vector_pattern=vector_pattern))
    type_specific_match = type_specific_pattern.match(type_specific_txt)
    obj.setOuterRadius(float(type_specific_match.group('radius')))
    obj.setHeight(float(type_specific_match.group('height')))
    obj.setAxis(vectorstr2float(type_specific_match.group('axis')))
  elif obj_type == 'cone':
    obj = bfdtd.Cone()
    type_specific_pattern = re.compile('radius (?P<radius1>[\d.]+), height (?P<height>[\d.]+), axis (?P<axis>{vector_pattern})\s+radius2 (?P<radius2>[\d.]+)'.format(vector_pattern=vector_pattern))
    type_specific_match = type_specific_pattern.match(type_specific_txt)
    obj.setOuterRadius(float(type_specific_match.group('radius1')))
    obj.setOuterRadius2(float(type_specific_match.group('radius2')))
    obj.setHeight(float(type_specific_match.group('height')))
    obj.setAxis(vectorstr2float(type_specific_match.group('axis')))
  elif obj_type == 'block' or obj_type == 'ellipsoid':
    if obj_type == 'block':
      obj = bfdtd.Parallelepiped()
    else:
      obj = bfdtd.Ellipsoid()
    type_specific_pattern = re.compile('size (?P<size>{vector_pattern})\s+axes (?P<e0>{vector_pattern}), (?P<e1>{vector_pattern}), (?P<e2>{vector_pattern})'.format(vector_pattern=vector_pattern))
    type_specific_match = type_specific_pattern.match(type_specific_txt)
    if type_specific_match is None:
      raise Exception('Failed to match: {}'.format(type_specific_txt))
    obj.setSize( vectorstr2float(type_specific_match.group('size')) )
    e0 = vectorstr2float(type_specific_match.group('e0'))
    e1 = vectorstr2float(type_specific_match.group('e1'))
    e2 = vectorstr2float(type_specific_match.group('e2'))
    obj.setAxes(e0, e1, e2)
  else:
    raise
  obj.setLocation(location)
  obj.setRelativePermittivity(permittivity)
  
#  print(obj)
  
  return(obj)

def getWrapperCode(infile):
  template = textwrap.dedent('''\
    (define (run-until cond? . step-funcs) 0 )
    (define (at-every dT . step-funcs) 0 )
    (define (system* x . y) 0 )
    (define (init-fields) 0 )
    (define (output-epsilon) 0 )
    (define (exit) 0)
    (define (print-object obj) (display-geometric-object-info 5 obj))
    (define (print-geometry) (map print-object geometry))
    (include "{}")
    
    (define (init-fields)
      (if (null? structure) (init-structure k-point))
      (set! fields (new-meep-fields structure
            (if (= dimensions CYLINDRICAL) m 0)
            (if (and special-kz? k-point)
                (vector3-z k-point) 0.0)
            (not accurate-fields-near-cylorigin?)))
      (if verbose? (meep-fields-verbose fields))
      (if (not (or force-complex-fields?
             (and (= dimensions CYLINDRICAL) (not (zero? m)))
             (not (for-all? symmetries
                (lambda (s)
            (zero? (imag-part
              (object-property-value s 'phase))))))
             (not (or (not k-point)
          (and special-kz?
               (= (vector3-x k-point) 0)
               (= (vector3-y k-point) 0))
          (vector3= k-point (vector3 0))))))
          (meep-fields-use-real-fields fields)
          (print "Meep: using complex fields.\n"))
      (if k-point (meep-fields-use-bloch fields
                 (if special-kz?
               (vector3 (vector3-x k-point)
                  (vector3-y k-point))
               k-point)))
      (map (lambda (s) (add-source s fields)) sources)
      (map (lambda (thunk) (thunk)) init-fields-hooks))
    
    (init-fields)
    (quit)
    ''')
    
  return template.format(infile)

def createWrapperFile(infile, verbosity=0):
  
  fd, fname = tempfile.mkstemp()
  os.close(fd)

  with open(fname, 'w') as f:
    f.write(getWrapperCode(infile))

  if verbosity > 0:
    subprocess.run(['/bin/cat', fname])
    print('infile = {}'.format(infile))
    print('fname = {}'.format(fname))
  return(fname)

def getInfoFromCTL(infile, verbosity=0):
  # .. todo:: use this in the blender import (support .ctl files instead of just .out files)
  # .. todo:: find way to output source info + probes, snapshots, etc (input/output objects)
  
  # with open('/tmp/caca.ctl', 'w') as f:
    # s = getWrapperCode(infile)
    # f.write(s)
  
  p = subprocess.run(['meep'], input=getWrapperCode(infile), universal_newlines=True, stdout=subprocess.PIPE, check=True)
  outfile = io.StringIO(p.stdout)
  (MEEP_data_list, geo_list) = getInfoFromOutFile(outfile)
  
  return (MEEP_data_list, geo_list)

def parseGeometry(infile, verbosity=0):
#  print('=== parseGeometry ===')
  infile.seek(0)
  txt = infile.read()
  #print(txt)
  
  meep_geometry_block = '(Computational cell is .*time for set_epsilon = )'
  mpb_geometry_block = '(Geometric objects:.*Geometric object tree)'
  #p = re.compile('Computational cell is .*time for set_epsilon = ', re.DOTALL)
  #p = re.compile('Geometric objects:.*Geometric object tree', re.DOTALL)
  p = re.compile('|'.join([meep_geometry_block, mpb_geometry_block]), re.DOTALL)
  
  geometry_txt = p.search(txt).group(0)
#  print(geometry_txt)
  
  #object_pattern = re.compile('[a-z]+,')
  object_pattern = re.compile('[a-z]+,.*?dielectric constant epsilon.*?\n', re.DOTALL)
  #object_pattern = re.compile('     [a-z]+,.*?(?=\n     [a-z])', re.DOTALL)
  
  
  obj_iterator = object_pattern.finditer(geometry_txt)
#  print(obj_iterator)
  
  geo_list = []
  
  for idx, s in enumerate(obj_iterator):
#    print('====================')
#    print('idx = {}'.format(idx))
#    print('--------------------')
#    print(s.group(0))
#    print('====================')
    geo_list.append(parseGeometryObject(s.group(0)))
  
     #sphere, center = (0,0,0)
          #radius 1
          #dielectric constant epsilon = 12
    #pass
  return(geo_list)

def main():
  parser = argparse.ArgumentParser()
  parser.add_argument('-v', '--verbose', action='count', dest='verbosity', default=0)
  parser.add_argument('--ctl', action='store_true')
  parser.add_argument('infile', type=argparse.FileType('r'), nargs='+')

  subparsers = parser.add_subparsers(help='Available subcommands', dest='chosen_subcommand')

  parser_printInfo = subparsers.add_parser('printInfo', help='Print info based on infile.')
  parser_printInfo.set_defaults(func=subcommand_printInfo)

  # TODO: Add formatting options? presets like .prn reader compatible format?
  parser_writeCSV = subparsers.add_parser('writeCSV', help='Write data from outfile to one CSV file per dataset.')
  parser_writeCSV.set_defaults(func=subcommand_writeCSV)

  args = parser.parse_args()
  
  print(args)
  
  if not args.chosen_subcommand:
    args.chosen_subcommand='printInfo'
    args.func=subcommand_printInfo
  
  args.func(args)
      
  return(0)

if __name__ == '__main__':
	main()
