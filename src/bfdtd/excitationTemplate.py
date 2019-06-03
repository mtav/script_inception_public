#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from __future__ import division

import sys
import numpy

'''
Excitation template objects, used to generate the template files.

.. todo:: Rewrite into single class accepting python functions as argument to fill the template
.. todo:: Write general .prn file read/write functions with options to support the changing .prn file formats (ex: 2013 with empty lines and earlier versions without)
.. todo:: Create template parent class, improve class names of excitations and templates, review the whole excitation+template system
.. todo:: Add .dat file reading
'''

class ExcitationGaussian1(object):
  '''
  gaussian excitation template object which creates a 2D gaussian surface with a central maximum point
  '''
  def __init__(self,amplitude = 1, beam_centre_x = 0, beam_centre_y = 0, sigma_x = 1, sigma_y = 1, out_col_name='z', column_titles=['x','y','z'], fileName='template.dat'):
    self.amplitude = amplitude
    self.beam_centre_x = beam_centre_x
    self.beam_centre_y = beam_centre_y
    self.sigma_x = sigma_x
    self.sigma_y = sigma_y
    self.out_col_name = out_col_name
    self.column_titles = column_titles
    self.fileName = fileName
    self.x_list = [-1,0,1]
    self.y_list = [-1,0,1]
      
  def writeDatFile(self, fileName, overwrite=True):
    '''Generate template .dat file for a plane excitation'''
    #self.x_list = mesh.getXmesh()
    #self.y_list = mesh.getYmesh()
    #self.z_list = mesh.getZmesh()
    
    x_col = []
    y_col = []
    out_col = []
    
    print('Generating template N='+str(len(self.x_list)*len(self.y_list)))
    for x in self.x_list:
      for y in self.y_list:
        x_col.append(x)
        y_col.append(y)
        X = x-self.beam_centre_x
        Y = y-self.beam_centre_y
        R = abs(numpy.sqrt( pow((X),2) + pow((Y),2) ))
        #out = self.amplitude * numpy.exp( -pow((R-self.c),2) / (2*pow(self.sigma,2)) )
        out = self.amplitude * numpy.exp( -( pow(X,2)/(2*pow(self.sigma_x,2)) + pow(Y,2)/(2*pow(self.sigma_y,2)) ) )
        out_col.append(out)

    # check if file already exists
    if not overwrite and os.path.exists(fileName):
      raise UserWarning('File already exists: ' + fileName)
    
    # write file
    with open(fileName, 'w') as FILE:
      print('Writing excitation template to '+fileName)
      for idx_col in range(len(self.column_titles)):
        if idx_col>0:
          FILE.write('\t')
        FILE.write(self.column_titles[idx_col])
      FILE.write('\n')
      for idx_row in range(len(out_col)):
        #print(x_col[idx_row])
        FILE.write("%15.6E\t%15.6E" % (x_col[idx_row], y_col[idx_row]))
        for idx_col in range(len(self.column_titles)-2):
          if self.column_titles[idx_col+2].lower() in [ x.lower() for x in self.out_col_name ]:
            FILE.write("\t%15.6E" % out_col[idx_row])
          else:
            FILE.write("\t%15.6E" % 0)
        FILE.write('\n')

    return

class ExcitationGaussian2(object):
  '''
  gaussian excitation template object which creates a 2D gaussian surface with a circular maximum of radius c
  '''
  def __init__(self, amplitude = 1, beam_centre_x = 0, beam_centre_y = 0, c = 1, sigma = 2, out_col_name='z', column_titles=['x','y','z'], fileName='template.dat'):
    self.amplitude = amplitude
    self.beam_centre_x = beam_centre_x
    self.beam_centre_y = beam_centre_y
    self.c = c
    self.sigma = sigma
    self.out_col_name = out_col_name
    self.column_titles = column_titles
    self.fileName = fileName
    self.x_list = [-1,0,1]
    self.y_list = [-1,0,1]

  def writeDatFile(self, fileName, overwrite=True):
    '''Generate template .dat file for a plane excitation'''
    #self.x_list = mesh.getXmesh()
    #self.y_list = mesh.getYmesh()
    #self.z_list = mesh.getZmesh()
    
    x_col = []
    y_col = []
    out_col = []
    
    print('Generating template N='+str(len(self.x_list)*len(self.y_list)))
    for x in self.x_list:
      for y in self.y_list:
        x_col.append(x)
        y_col.append(y)
        X = x-self.beam_centre_x
        Y = y-self.beam_centre_y
        R = abs(numpy.sqrt( pow((X),2) + pow((Y),2) ))
        out = self.amplitude * numpy.exp( -pow((R-self.c),2) / (2*pow(self.sigma,2)) )
        #out = self.amplitude * numpy.exp( -( pow(X,2)/(2*pow(self.sigma_x,2)) + pow(Y,2)/(2*pow(self.sigma_y,2)) ) )
        out_col.append(out)

    # check if file already exists
    if not overwrite and os.path.exists(fileName):
      raise UserWarning('File already exists: ' + fileName)

    # write file
    with open(fileName, 'w') as FILE:
      print('Writing excitation template to '+fileName)
      for idx_col in range(len(self.column_titles)):
        if idx_col>0:
          FILE.write('\t')
        FILE.write(self.column_titles[idx_col])
      FILE.write('\n')
      for idx_row in range(len(out_col)):
        #print(x_col[idx_row])
        FILE.write("%15.6E\t%15.6E" % (x_col[idx_row], y_col[idx_row]))
        for idx_col in range(len(self.column_titles)-2):
          if self.column_titles[idx_col+2].lower() in [ x.lower() for x in self.out_col_name ]:
            FILE.write("\t%15.6E" % out_col[idx_row])
          else:
            FILE.write("\t%15.6E" % 0)
        FILE.write('\n')

    return

class ExcitationUniform(object):
  '''
  gaussian excitation template object which creates a 2D gaussian surface with a circular maximum of radius c
  '''
  def __init__(self,
   amplitude = None,
   out_col_name = None,
   column_titles = None,
   fileName = None,
   x_list = None,
   y_list = None):
    
    if amplitude is None: amplitude = 10
    if out_col_name is None: out_col_name = ['Z1','Z3','Z5']
    if column_titles is None: column_titles = ['x','y','z1','z2','z3','z4','z5']
    if fileName is None: fileName = 'template.dat'
    if x_list is None: x_list = [-1,0,1]
    if y_list is None: y_list = [-1,0,1]
    
    self.amplitude = amplitude
    self.out_col_name = out_col_name
    self.column_titles = column_titles
    self.fileName = fileName
    self.x_list = x_list
    self.y_list = y_list

  def writeDatFile(self, fileName, overwrite=True):
    '''Generate template .dat file for a plane excitation'''

    print('Generating template N='+str(len(self.x_list)*len(self.y_list)))

    # check if file already exists
    if not overwrite and os.path.exists(fileName):
      raise UserWarning('File already exists: ' + fileName)

    # write file
    with open(fileName, 'w') as FILE:
      print('Writing excitation template to '+fileName)
      
      # writing column title line
      for idx_col in range(len(self.column_titles)):
        if idx_col>0:
          FILE.write('\t')
        FILE.write(self.column_titles[idx_col])
      FILE.write('\n')
      
      # fill in all columns whose name is in self.out_col_name
      for x in self.x_list:
        for y in self.y_list:
          FILE.write("%15.6E\t%15.6E" % (x, y))
          for idx_col in range(len(self.column_titles)-2):
            if self.column_titles[idx_col+2].lower() in [ x.lower() for x in self.out_col_name ]:
              FILE.write("\t%15.6E" % self.amplitude)
            else:
              FILE.write("\t%15.6E" % 0)
          FILE.write('\n')
        #FILE.write('\n')
      
    return
    #self.x_list = mesh.getXmesh()
    #self.y_list = mesh.getYmesh()
    #self.z_list = mesh.getZmesh()

    x_col = []
    y_col = []
    out_col = []
    
    print('Generating template N='+str(len(self.x_list)*len(self.y_list)))
    for x in self.x_list:
      for y in self.y_list:
        x_col.append(x)
        y_col.append(y)
        out_col.append(self.amplitude)
    
    # TODO: Why is there a second writing to the same file, overwriting it here? Looks like unfinished code...
    
    # write file
    with open(fileName, 'w') as FILE:
      print('Writing excitation template to '+fileName)
      
      # writing column title line
      for idx_col in range(len(self.column_titles)):
        if idx_col>0:
          FILE.write('\t')
        FILE.write(self.column_titles[idx_col])
      FILE.write('\n')
      
      # fill in all columns whose name is in self.out_col_name
      for idx_row in range(len(out_col)):
        #print(x_col[idx_row])
        FILE.write("%15.6E\t%15.6E" % (x_col[idx_row], y_col[idx_row]))
        for idx_col in range(len(self.column_titles)-2):
          if self.column_titles[idx_col+2].lower() in [ x.lower() for x in self.out_col_name ]:
            FILE.write("\t%15.6E" % out_col[idx_row])
          else:
            FILE.write("\t%15.6E" % 0)
        FILE.write('\n')

    return

# for testing
if __name__ == "__main__":
  obj = ExcitationUniform()
  obj.writeDatFile('tmp.dat')
