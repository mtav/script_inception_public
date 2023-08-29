#!/usr/bin/env python3
# -*- coding: utf-8 -*-

'''
Module containing the basic geometry objects available in BFDTD.
'''

import sys
import utilities
import utilities.geometry

from numpy.linalg import norm
from numpy import array, rad2deg, cross, dot, sqrt, ceil, deg2rad
from utilities.common import *
import utilities.geometry
from .meshobject import MeshObject, MeshingParameters

class GeometryObject(object):
  # .. todo:: rename permittivity, conductivity to relative permittivity, conductivity
  # .. todo:: finish implementing pre/post str() functions in other str() functions.
  def __init__(self):
    self.name = self.__class__.__name__
    self.layer = self.__class__.__name__
    self.group = self.__class__.__name__
    self.meshing_parameters = MeshingParameters()
    
    self.permittivity = 1 # vacuum by default
    self.conductivity = 0
    
    self.useForMeshing = True # set to False to disable use of this object during automeshing
    self.location = array([0,0,0]) # TODO: Make all GeometryObject subclasses use this one. (i.e. centro->location)
    
    ### rotation parameters
    # .. todo:: Yay, lot of ways of rotating... Fix this? Use single rotation matrix/quaternion/whatever, or a list of rotations?

    self.rotation_list = []

    # .. todo:: implement quaternions?
    #self.rotation_quaternion = Quaternion()
    
    # temporary quick solution:
    self.rotation_axis_angle = [0,0,1,0] # based on Blender defaults
    
  def getName(self):
    return(self.name)

  def setName(self, name):
    self.name = name
    return
    
  def writeRotations(self, FILE):
    for r in self.rotation_list:
      r.write_entry(FILE)
    return
    
  def translate(self, vec3):
    self.location += vec3
    return

  def rotate(self, axis_point, axis_direction, angle_degrees):
    self.rotation_list.append(Rotation(axis_point = axis_point, axis_direction = axis_direction, angle_degrees = angle_degrees))
  
  def setRotationAxisAngle(self, rotation_axis_angle):
    self.rotation_axis_angle = rotation_axis_angle
    return
  def getRotationAxisAngle(self):
    return(self.rotation_axis_angle)
    
  def getRotationMatrix(self):
    R = numpy.eye(3)
    for r in self.rotation_list:
      R = numpy.dot(r.getRotationMatrix(), R)
    return(R)

  def __pre_str__(self):
    '''Returns a string to print name, permittivity, conductivity and location. With a newline ending.'''
    ret  = 'name = '+self.name+'\n'
    ret += 'permittivity = '+str(self.permittivity)+'\n'
    ret += 'conductivity = '+str(self.conductivity)+'\n'
    ret += 'location = {}'.format(self.location) + '\n'
    return(ret)

  def __post_str__(self):
    '''Returns a string to print the rotation list. Without newline ending.'''
    ret = '--->object rotation_list'
    for i in range(len(self.rotation_list)):
      ret += '\n'
      ret += '-->object rotation '+str(i)+':\n'
      ret += self.rotation_list[i].__str__()
    return(ret)
  
  def __str__(self):
    ''' Returns a string object, so that print(object) prints useful information about the object instance. '''
    ret = self.__pre_str__() + self.__post_str__()
    return(ret)
      
  def setRefractiveIndex(self,n):
    self.permittivity = pow(n,2)

  def getRefractiveIndex(self):
    return numpy.sqrt(self.permittivity)

  def setRelativePermittivity(self, permittivity):
    # .. todo:: support diagonal/matrix permittivities like in MEEP... Warning: May break a lot of things...
    if isinstance(permittivity, int) or isinstance(permittivity, float):
      self.permittivity = permittivity
    else:
      if len(permittivity) == 1:
        # self.permittivity = 3*[permittivity]
        self.permittivity = permittivity[0]
      else:
        self.permittivity = permittivity
    return(self.permittivity)
  
  def setRelativeConductivity(self, conductivity):
    self.conductivity = conductivity

  def getRelativePermittivity(self, mean=True):
    if mean and isinstance(self.permittivity, list):
      return sum(self.permittivity)/len(self.permittivity)
    return(self.permittivity)

  def getRelativeConductivity(self):
    return(self.conductivity)

  # this function requires the child objects to define a getCentro() and translate() method
  # TODO: It might make more sense to have each child object have its own setCentro function?
  #def setCentro(self, nova_centro):
    #nova_centro = numpy.array(nova_centro)    
    #nuna_centro = self.getCentro()
    #self.translate(nova_centro - nuna_centro)
    
  def setLocation(self, location):
    self.location = array(location)
    return

  def getLocation(self):
    return array(self.location)

  def getLowerAbsolute(self):
    return array(self.location) + array(self.getLowerRelative()) # note that the plus sign is because getLowerRelative() already returns an "algebraic vector"

  def getUpperAbsolute(self):
    return array(self.location) + array(self.getUpperRelative())

  def getExtension(self):
    return fixLowerUpper(self.getLowerAbsolute(), self.getUpperAbsolute())

  def AABB_intersects(self, obj):
    '''Returns true if the bounding box of the object intersects with the one of the object *obj*.'''

    minBB_cyl, maxBB_cyl = self.getAABB()
    minBB_obj, maxBB_obj = obj.getAABB()
    val = utilities.geometry.AABB_intersect(minBB_cyl, maxBB_cyl, minBB_obj, maxBB_obj)
    return(val)

class Sphere(GeometryObject):
  def __init__(self):
    super().__init__()
    self.inner_radius = 0
    self.outer_radius = 0.5
    
  def setOuterRadius(self, outer_radius):
    self.outer_radius = outer_radius
    return(self.outer_radius)
    
  def setSize(self, size_vec3):
    '''setSize wrapper for use in BFDTD export scripts'''
    return self.setOuterRadius(0.5*size_vec3[2]) # We use the z-component because for the blender icospheres, it is the closest to the diametre used when creating them.
  
  def setInnerRadius(self, inner_radius):
    self.inner_radius = inner_radius
    return(self.inner_radius)
    
  def getOuterRadius(self):
    return(self.outer_radius)
  
  def getInnerRadius(self):
    return(self.inner_radius)

  def getSize(self):
    ''' get the size of the sphere as an array of size 3 '''
    d = 2*self.getOuterRadius()
    return([d, d, d])

  def __str__(self):
    ''' Returns a string object, so that print(object) prints useful information about the object instance. '''
    ret = self.__pre_str__() # includes name, location, material infos and ends with a newline
    ret += 'inner_radius = ' + str(self.inner_radius) + '\n'
    ret += 'outer_radius = ' + str(self.outer_radius) + '\n'
    ret += self.__post_str__() # includes rotation list
    return ret

  def read_entry(self,entry):
    if entry.name:
      self.name = entry.name
    self.location = float_array([entry.data[0],entry.data[1],entry.data[2]])
    self.outer_radius = float(entry.data[3])
    self.inner_radius = float(entry.data[4])
    self.permittivity = float(entry.data[5])
    self.conductivity = float(entry.data[6])
    return(0)
    
  def write_entry(self, FILE=sys.stdout):
    '''BFDTD sphere object:
    
    * 1-5 Coordinates of the sphere ( xc yc zc r1 r2 )
    * 6 permittivity
    * 7 conductivity
    '''
    FILE.write('SPHERE  **name='+self.name+'\n')
    FILE.write('{\n')
    FILE.write("%E **XC\n" % self.location[0])
    FILE.write("%E **YC\n" % self.location[1])
    FILE.write("%E **ZC\n" % self.location[2])
    FILE.write("%E **outer_radius\n" % self.outer_radius)
    FILE.write("%E **inner_radius\n" % self.inner_radius)
    FILE.write("{:E} **relative permittivity -> n=sqrt(mu_r*epsilon_r)={:.2f}\n".format(self.permittivity, sqrt(self.permittivity)))
    FILE.write("%E **relative conductivity\n" % self.conductivity)
    FILE.write('}\n')
    FILE.write('\n')

  def writeCTL(self, FILE=sys.stdout, offset=numpy.array([0,0,0])):
    centro = self.getLocation() + offset
    FILE.write('  (make sphere\n')
    FILE.write('    (material (make medium (epsilon {})) )\n'.format(self.getRelativePermittivity()))
    FILE.write('    (center (vector3 {} {} {}) )\n'.format(*centro))
    FILE.write('    (radius {})\n'.format(self.getOuterRadius()))
    FILE.write('  )\n')

  def getLowerRelative(self):
    return array(3*[-self.outer_radius])

  def getUpperRelative(self):
    return array(3*[self.outer_radius])

class Block(GeometryObject):
  ''' Create a Block. '''
  def __init__(self):
    ''' Constructor '''
    super().__init__()
    
    # These are specified relative to location
    self.lower_relative = array([-0.5,-0.5,-0.5])
    self.upper_relative = array([0.5,0.5,0.5])

  def __str__(self):
    ''' Returns a string object, so that print(object) prints useful information about the object instance. '''
    ret = self.__pre_str__() # includes name, location, material infos and ends with a newline
    ret += 'lower_relative = '+str(self.lower_relative)+'\n'
    ret += 'upper_relative = '+str(self.upper_relative)+'\n'
    ret += 'lower_absolute = '+str(self.getLowerAbsolute())+'\n'
    ret += 'upper_absolute = '+str(self.getUpperAbsolute())+'\n'
    ret += self.__post_str__() # includes rotation list
    return ret
    
  def read_entry(self, entry):
    '''read an entry extracted from a .geo file'''
    if entry.name:
      self.name = entry.name
    try:
      lower_absolute = array(float_array(entry.data[0:3]))
      upper_absolute = array(float_array(entry.data[3:6]))
      self.permittivity = float(entry.data[6])
      self.conductivity = float(entry.data[7])
    except:
      raise Exception('Incorrect format for BLOCK entry. Correct format is 8 float values: LX, LY, LZ, UX, UY, UZ, permittivity, conductivity')
    self.setLocation( (array(lower_absolute) + array(upper_absolute))/2 )
    self.setLowerAbsolute(lower_absolute)
    self.setUpperAbsolute(upper_absolute)
    
  def write_entry(self, FILE=sys.stdout):
    '''write an entry to a file object'''
    self.lower_relative, self.upper_relative = fixLowerUpper(self.lower_relative, self.upper_relative)
    FILE.write('BLOCK **name='+self.name+'\n')
    FILE.write('{\n')
    L = self.getLowerAbsolute()
    U = self.getUpperAbsolute()
    FILE.write("%E **XL\n" % L[0])
    FILE.write("%E **YL\n" % L[1])
    FILE.write("%E **ZL\n" % L[2])
    FILE.write("%E **XU\n" % U[0])
    FILE.write("%E **YU\n" % U[1])
    FILE.write("%E **ZU\n" % U[2])
    FILE.write("{:E} **relative permittivity -> n=sqrt(mu_r*epsilon_r)={:.2f}\n".format(self.permittivity, sqrt(self.permittivity)))
    FILE.write("%E **relative conductivity\n" % self.conductivity)
    FILE.write('}\n')
    FILE.write('\n')
    
    #print(self.rotation_axis_angle)
    if self.rotation_axis_angle[0] != 0:
      rot = Rotation(name = self.name+'_rotation', axis_point = self.getCentro(), axis_direction = self.rotation_axis_angle[1:4], angle_degrees = rad2deg(self.rotation_axis_angle[0]))
      rot.write_entry(FILE)
      
  def writeCTL(self, FILE=sys.stdout, offset=numpy.array([0,0,0])):
    centro = self.getLocation() + offset
    FILE.write('  (make block\n')
    FILE.write('    (material (make medium (epsilon {})) )\n'.format(self.getRelativePermittivity()))
    FILE.write('    (center (vector3 {} {} {}) )\n'.format(*centro))
    FILE.write('    (size (vector3 {} {} {}) )\n'.format(*self.getSize()))
    FILE.write('    (e1 (vector3 1 0 0))\n')
    FILE.write('    (e2 (vector3 0 1 0))\n')
    FILE.write('    (e3 (vector3 0 0 1))\n')
    FILE.write('  )\n')
  
  def setLowerRelative(self, lower_relative):
    self.lower_relative = array(lower_relative)
  
  def setUpperRelative(self, upper_relative):
    self.upper_relative = array(upper_relative)

  def setLowerAbsolute(self, lower_absolute):
    self.lower_relative = array(lower_absolute) - self.location
  
  def setUpperAbsolute(self, upper_absolute):
    self.upper_relative = array(upper_absolute) - self.location
  
  def getLowerRelative(self):
    return array(self.lower_relative)

  def getUpperRelative(self):
    return array(self.upper_relative)
        
  def getCentro(self):
    '''
    Returns the centre of the block (which can be different from its location).
    At the moment, the origin of a block can be arbitrarily defined, so keeping this around is useful.
    '''
    return array(0.5*(self.getLowerAbsolute()+self.getUpperAbsolute()))
  
  def setOriginToGeometry(self):
    ''' Sets the origin of the block (i.e. the location) to the geometric centre of the block, without changing the absolute lower and upper coordinates. '''
    lower_absolute = self.getLowerAbsolute()
    upper_absolute = self.getUpperAbsolute()
    new_location = (lower_absolute + upper_absolute) / 2
    self.setSize(upper_absolute - lower_absolute)
    self.setLocation(new_location)
    return
  
  #def translate(self, vec3):
    #'''
    #.. todo:: translate should just change the location property and be the same for all objects. Redefine lower and upper when writing, etc. They should be relative.
    #'''
    #self.lower_relative = numpy.array(self.lower_relative)
    #self.upper_relative = numpy.array(self.upper_relative)
    #self.lower_relative = self.lower_relative + vec3
    #self.upper_relative = self.upper_relative + vec3
  
  def getMeshingParameters(self,xvec,yvec,zvec,epsx,epsy,epsz):
    ''' get meshing parameters '''
    objx = numpy.sort([self.getLowerAbsolute()[0],self.getUpperAbsolute()[0]])
    objy = numpy.sort([self.getLowerAbsolute()[1],self.getUpperAbsolute()[1]])
    objz = numpy.sort([self.getLowerAbsolute()[2],self.getUpperAbsolute()[2]])
    eps = self.permittivity
    xvec = numpy.vstack([xvec,objx])
    yvec = numpy.vstack([yvec,objy])
    zvec = numpy.vstack([zvec,objz])
    epsx = numpy.vstack([epsx,eps])
    epsy = numpy.vstack([epsy,eps])
    epsz = numpy.vstack([epsz,eps])
    return xvec,yvec,zvec,epsx,epsy,epsz
    
  def getSize(self):
    ''' get the size of the block as an array of size 3 '''
    return abs(self.getUpperRelative() - self.getLowerRelative())

  def setSize(self, size_vec3):
    ''' size_vec3 can be a vector of size 3 or a simple int or float (vector of size 1, scalar) '''
    self.lower_relative = -0.5*numpy.array(size_vec3)
    self.upper_relative = 0.5*numpy.array(size_vec3)
    return
  
  def getAABB(self):
    '''
      Returns the lower and upper corners of an Axis-Aligned Bounding Box (AABB) in absolute coordinates in the form **(minBB, maxBB)**, where *minBB = [xmin,ymin,zmin]* and *maxBB = [xmax,ymax,zmax]*.
    '''
    return (self.getLowerAbsolute(), self.getUpperAbsolute())

  def getMEEPobject(self):
    import meep
    meep_block = meep.Block( meep.Vector3(*self.getSize()),
                 center = meep.Vector3(*self.getLocation()),
                 material = meep.Medium(epsilon=self.getRelativePermittivity()) )
    return(meep_block)

class Distorted(GeometryObject):
  '''
  A cuboid object with arbitrary vertex positioning.

  .. image:: /images/distorted_vertices.png
     :align: center
  
  Vertex indices:
  
  * 0,1,2,3 = top face numbered clockwise viewed from outside
  * 4,5,6,7 = bottom face numbered clockwise viewed from outside
  
  Edges:
  
  * 3 connected to 4
  * 2 connected to 5
  * 0 connected to 7
  * 1 connected to 6
  
  Normal faces viewed from outside:
  
  * [3,2,1,0]
  * [7,6,5,4]
  * [0,1,6,7]
  * [1,2,5,6]
  * [2,3,4,5]
  * [3,0,7,4]  
  '''
  def __init__(self):
    ''' Constructor '''
    GeometryObject.__init__(self)
    
    # relative vertices
    self.vertices_relative = array([[ 0.5, -0.5,  0.5],
                              [-0.5, -0.5,  0.5],
                              [-0.5,  0.5,  0.5],
                              [ 0.5,  0.5,  0.5],
                              [ 0.5,  0.5, -0.5],
                              [-0.5,  0.5, -0.5],
                              [-0.5, -0.5, -0.5],
                              [ 0.5, -0.5, -0.5]])

  def setVerticesRelative(self, vertices_relative):
    ''' Set relative coordinates of the object's vertices. '''
    self.vertices_relative = array(vertices_relative)
    #self.vertices_relative = [ array(v) for v in vertices_relative ]
    return

  def setVerticesAbsolute(self, vertices_absolute):
    ''' Set absolute coordinates of the object's vertices. '''
    #vertices_absolute = [ array(v) for v in vertices_absolute ]
    self.vertices_relative = array(vertices_absolute) - self.location
    return
    
  def getVerticesRelative(self):
    ''' Get relative coordinates of the object's vertices. '''
    return(self.vertices_relative)

  def getVerticesAbsolute(self):
    ''' Get absolute coordinates of the object's vertices. '''
    return(self.location + self.vertices_relative)
  
  def getCentroOfMassAbsolute(self):
    ''' Returns the "centro of mass" of the object, i.e. sum(vertices)/8. '''
    vertices_absolute = self.getVerticesAbsolute()
    return sum(vertices_absolute)/len(vertices_absolute)
    #S = numpy.array([0,0,0])
    #for v in self.vertices_relative:
      #S = S + numpy.array(v)
    #return 1./len(self.vertices_relative)*S
    
  def setOrigin(self, location):
    '''
    Sets the location to the specified location, but so that the vertices keep the same absolute coordinates. This has no effect on BFDTD output, but is useful for placing objects. It is similar to changing the origin of an object in blender, while keeping the mesh in the same place.
    .. todo:: Rotations will complicate things here. May need to make sure it adapts the rotation accordingly.
    '''
    vertices_absolute = self.getVerticesAbsolute()
    self.setLocation(location)
    self.setVerticesAbsolute(vertices_absolute)
    return

  def setOriginToGeometry(self):
    '''
    Sets the origin of the object to its centro of mass.
    '''
    self.setOrigin(self.getCentroOfMassAbsolute())
    return
  
  def __str__(self):
    ''' Returns a string object, so that print(object) prints useful information about the object instance. '''
    ret = self.__pre_str__() # includes name, location, material infos and ends with a newline
    ret += 'vertices_relative = '+str(self.vertices_relative)+'\n'
    ret += self.__post_str__() # includes rotation list
    return ret
  
  def read_entry(self,entry):
    ''' Read a .geo file entry. '''
    if entry.name:
      self.name = entry.name
      
    vertices_absolute = 8*[array([0,0,0])]
    for i in range(8):
      vertices_absolute[i] = array(float_array(entry.data[3*i:3*i+3]))
    
    self.setVerticesAbsolute(vertices_absolute)
    self.setOriginToGeometry()
      
    self.permittivity = float(entry.data[8*3])
    self.conductivity = float(entry.data[8*3+1])
    
  def write_entry(self, FILE=sys.stdout):
    ''' Write a .geo file entry. '''
    FILE.write('DISTORTED **name='+self.name+'\n')
    FILE.write('{\n')

    vertices_absolute = self.getVerticesAbsolute()
    
    for i in range(len(self.vertices_relative)):
      FILE.write("%E **XV%d\n" % (vertices_absolute[i][0],i) )
      FILE.write("%E **YV%d\n" % (vertices_absolute[i][1],i) )
      FILE.write("%E **ZV%d\n" % (vertices_absolute[i][2],i) )
    FILE.write("{:E} **relative permittivity -> n=sqrt(mu_r*epsilon_r)={:.2f}\n".format(self.permittivity, sqrt(self.permittivity)))
    FILE.write("%E **relative conductivity\n" % self.conductivity)
    FILE.write('}\n')
    FILE.write('\n')
    
  #def translate(self, vec3):
    #for i in range(len(self.vertices_relative)):
      #self.vertices_relative[i] = numpy.array(self.vertices_relative[i]) + numpy.array(vec3)
      
  def getMeshingParameters(self,xvec,yvec,zvec,epsx,epsy,epsz):
    ''' todo:: improve meshing system + add support for rotations '''
    
    # determine lower and upper points of distorted object
    vertex_min = numpy.array(self.vertices_relative[0])
    vertex_max = numpy.array(self.vertices_relative[0])
    for vertex in self.vertices_relative:
      #print('vertex = '+str(vertex))
      for i in range(3):
        if vertex[i]<vertex_min[i]: vertex_min[i] = vertex[i]
        if vertex[i]>vertex_max[i]: vertex_max[i] = vertex[i]
    
    #print('vertex_min = '+str(vertex_min))
    #print('vertex_max = '+str(vertex_max))
    
    objx = numpy.sort([vertex_min[0],vertex_max[0]])
    objy = numpy.sort([vertex_min[1],vertex_max[1]])
    objz = numpy.sort([vertex_min[2],vertex_max[2]])
    eps = self.permittivity
    xvec = numpy.vstack([xvec,objx])
    yvec = numpy.vstack([yvec,objy])
    zvec = numpy.vstack([zvec,objz])
    epsx = numpy.vstack([epsx,eps])
    epsy = numpy.vstack([epsy,eps])
    epsz = numpy.vstack([epsz,eps])
    return xvec,yvec,zvec,epsx,epsy,epsz

class Parallelepiped(Distorted):
  '''
  A parallelepiped (i.e., a brick, possibly with non-orthogonal axes).
  
  Properties:
  
  * location [vector3]: Center point of the object. default value: [0,0,0]
  * size [vector3]: The lengths of the block edges along each of its three axes. Not really a 3-vector, but it has three components, each of which should be nonzero. default value: [1,1,1]
  * e0, e1, e2 [vector3]: The directions of the axes of the block; the lengths of these vectors are ignored. Must be linearly independent. They default to the three lattice directions. 
  
  .. todo:: This should be merged with the GWL Parallelepiped.
    And we should add a GWL writing system to Distorted.
    idea: objects are as general as possible, following CAD-like standards/systems. They then just get extended with special read/write functions depending on the application.
    
  .. todo:: Think about class design a bit more... parallepiped, block, distorted, ellipsoid...
  '''
  def __init__(self):
    ''' Constructor '''
    super().__init__()
    self.e0 = [1,0,0]
    self.e1 = [0,1,0]
    self.e2 = [0,0,1]
    self.size = [1,1,1]
    self.updateVertices()
    return
  
  def __str__(self):
    ''' Returns a string object, so that print(object) prints useful information about the object instance. '''
    ret = self.__pre_str__() # includes name, location, material infos and ends with a newline
    ret += 'e0 = {}\n'.format(self.e0)
    ret += 'e1 = {}\n'.format(self.e1)
    ret += 'e2 = {}\n'.format(self.e2)
    ret += 'size = {}\n'.format(self.size)
    ret += self.__post_str__() # includes rotation list
    return ret

  def setSize(self, size):
    self.size = size
    self.updateVertices()
    
  def getSize(self):
    return self.size
  
  def setAxes(self, e0, e1, e2):
    self.e0 = e0
    self.e1 = e1
    self.e2 = e2
    self.updateVertices()
    return
    
  def getAxes(self):
    return (numpy.array(self.e0), numpy.array(self.e1), numpy.array(self.e2))
    
  def updateVertices(self):
    self.setDirectionsAndSize(self.e0, self.e1, self.e2, self.size)
    
  def setDirectionsAndSize(self, e0, e1, e2, size):
    '''
    .. todo:: There is no protection against an "inverted cuboid" at the moment.
    '''
    e0 = array(e0)
    e1 = array(e1)
    e2 = array(e2)
    
    u0 = size[0]*e0/norm(e0)
    u1 = size[1]*e1/norm(e1)
    u2 = size[2]*e2/norm(e2)

    v_list = [[0.5,-0.5,0.5],[-0.5,-0.5,0.5],[-0.5,0.5,0.5],[0.5,0.5,0.5],[0.5,0.5,-0.5],[-0.5,0.5,-0.5],[-0.5,-0.5,-0.5],[0.5,-0.5,-0.5]]
    
    v_list_new = [ v[0]*u0 + v[1]*u1 + v[2]*u2 for v in v_list]
    
    self.setVerticesRelative(v_list_new)
    return

class Ellipsoid(Parallelepiped):
  def __init__(self):
    ''' Constructor '''
    super().__init__()

class Cylinder(GeometryObject):
  def __init__(self,
    inner_radius = None,
    outer_radius = None,
    height = None,
    angle_deg = None):

    if inner_radius is None: inner_radius = 0
    if outer_radius is None: outer_radius = 0.5
    if height is None: height = 1
    if angle_deg is None: angle_deg = 0
    
    super(Cylinder, self).__init__() # python 2+3 compatible super() call
    self.inner_radius = inner_radius
    self.outer_radius = outer_radius
    self.height = height
    self.angle_deg = angle_deg
    
    # quick hack to make life easy
    #self.axis = array([0,1,0])
  
  def getCentro(self):
    raise Exception('WARNING: getCentro() is deprecated. Please use getLocation() instead.')
    return self.getLocation()

  def setSize(self, dimensions):
    ''' sets size from a 3d vector of the form [2*outer_radius, 2*outer_radius, height] (if the first 2 values are different, it takes the maximum) '''
    # TODO: inner radius? (Problem: this is used by the current BFDTD export prototype and supposed to be the same for all objects.)
    self.outer_radius = 0.5*max(dimensions[0],dimensions[2])
    self.height = dimensions[1]
  
  # deprecated old functions
  #def getLower(self):
    #return [self.location[0]-self.outer_radius,self.location[1]-0.5*self.height,self.location[2]-self.outer_radius]
  
  #def getUpper(self):
    #return [self.location[0]+self.outer_radius,self.location[1]+0.5*self.height,self.location[2]+self.outer_radius]
  
  # .. todo:: Make these functions return the bounding box values!!! (AABB + non-AABB values?)
  def getLowerRelative(self):
    '''
      Returns the lower corner of an Axis-Aligned Bounding Box (AABB) in coordinates relative to the location (centre of the cylinder).
    '''
    #return array([-self.outer_radius, -0.5*self.height, -self.outer_radius])
    (minBB, maxBB) = self.getAABB()
    return(minBB - self.getLocation())

  def getUpperRelative(self):
    '''
      Returns the upper corner of an Axis-Aligned Bounding Box (AABB) in coordinates relative to the location (centre of the cylinder).
    '''
    #return array([self.outer_radius, 0.5*self.height, self.outer_radius])
    (minBB, maxBB) = self.getAABB()
    return(maxBB - self.getLocation())
  
  def getAABB(self):
    '''
      Returns the lower and upper corners of an Axis-Aligned Bounding Box (AABB) in absolute coordinates in the form **(minBB, maxBB)**, where *minBB = [xmin,ymin,zmin]* and *maxBB = [xmax,ymax,zmax]*.
    '''
    start_point, end_point = self.getStartEndPoints()
    return utilities.geometry.getAABBCylinder(start_point, end_point, self.getOuterRadius())

  def setDiametre(self,diametre):
    self.outer_radius = 0.5*diametre

  # TODO: Implement inner/outer radius visualization, check it actually works in Bristol FDTD
  
  def setInnerRadius(self, inner_radius):
    self.inner_radius = inner_radius
  def getInnerRadius(self):
    return(self.inner_radius)

  def setOuterRadius(self, outer_radius):
    self.outer_radius = outer_radius
  def getOuterRadius(self):
    return(self.outer_radius)
    
  def setHeight(self, height):
    self.height = height
  def getHeight(self):
    return(self.height)

  def getAxis(self):
    # TODO
    # quick hack to make life easy
    #return(self.axis)
    # .. todo:: fix NaN returns if axis = Y axis for example
    
    rotation_axis_angle = self.getRotationAxisAngle()
    angle_radians = rotation_axis_angle[0]
    axis_direction = rotation_axis_angle[1:4]
    
    # hack because when we write, we use both rotation systems at the moment... :/
    
    # first rotation using a single axis/angle definition
    R1 = rotation_matrix3(axis_direction, angle_radians)
    cylinder_axis = numpy.dot(R1, [0,1,0])
    
    # second rotation using the BFDTD rotation list system
    R2 = self.getRotationMatrix()
    cylinder_axis = numpy.dot(R2, cylinder_axis)
    
    return( utilities.common.unitVector(cylinder_axis) )

  def setAxis(self, axis_vec3):
    
    # quick hack to make life easy
    #self.axis = axis_vec3
    
    angle_radians = Angle([0,1,0], axis_vec3)
    axis_direction = cross([0,1,0], axis_vec3)
    
    if numpy.dot(axis_direction, axis_direction) == 0:
      if angle_radians == 0:
        self.setRotationAxisAngle([0, 0, 1, 0])
      else:
        self.setRotationAxisAngle([numpy.pi, 0, 0, 1])
    else:
      self.setRotationAxisAngle([angle_radians, axis_direction[0], axis_direction[1], axis_direction[2]])

    return

  def setStartEndPoints(self, start_point_vec3, end_point_vec3):
    start_point_vec3 = array(start_point_vec3)
    end_point_vec3 = array(end_point_vec3)
    self.setAxis(end_point_vec3 - start_point_vec3)
    self.height = norm(end_point_vec3 - start_point_vec3)
    self.location = 0.5*(start_point_vec3 + end_point_vec3)
    return
    
  def getStartEndPoints(self):
    A = self.getLocation() - 0.5*self.getHeight()*self.getAxis()
    B = self.getLocation() + 0.5*self.getHeight()*self.getAxis()
    return(A,B)
  
  def __str__(self):
    ''' Returns a string object, so that print(object) prints useful information about the object instance. '''
    ret = self.__pre_str__() # includes name, location, material infos and ends with a newline
    ret += 'inner_radius = ' + str(self.inner_radius) + '\n'
    ret += 'outer_radius = ' + str(self.outer_radius) + '\n'
    ret += 'height = ' + str(self.height) + '\n'
    ret += 'angle_deg = ' + str(self.angle_deg) + '\n'
    ret += 'axis = ' + str(self.getAxis()) + '\n'
    ret += self.__post_str__() # includes rotation list
    return ret
  
  def read_entry(self,entry):
    if entry.name:
      self.name = entry.name
    self.location = float_array([entry.data[0],entry.data[1],entry.data[2]])
    self.inner_radius = float(entry.data[3])
    self.outer_radius = float(entry.data[4])
    self.height = float(entry.data[5])
    self.permittivity = float(entry.data[6])
    self.conductivity = float(entry.data[7])
    if(len(entry.data)>8): self.angle_deg = float(entry.data[8])
    return(0)
  
  #def computeRotationObjects(self):
    #rotation_objects = []

    #Rotation(name = 'cylinder_rotation',
      #axis_point = self.location,
      #axis_direction = cross([0,1,0],self.axis),
      #angle_degrees = rad2deg(Angle([0,1,0],self.axis)))

    #return rotation_objects
    
  # TODO: disable the old self.angle_deg parameter to avoid conflicts with rotation? But first find out how BFDTD handles it + discuss with Chris Railton.
  def write_entry(self, FILE=sys.stdout):
    '''
    cylinder
    {
    1-7 Coordinates of the material volume ( xc yc zc r1 r2 h )
    7 permittivity
    8 conductivity
    9 angle_deg of inclination
    }
    
    * xc, yc and zc are the coordinates of the centro of the cylinder. r1 and r2 are the inner and outer radius respectively
    * h is the cylinder height
    * angle_deg is the angle of inclination in degrees
      The cylinder is aligned with the y direction if =0 and with the x direction if =90
      i.e. angle_deg = Angle of rotation in degrees around -Z=(0,0,-1)
    '''
  
    FILE.write('CYLINDER **name='+self.name+'\n')
    FILE.write('{\n')
    FILE.write("%E **X centro\n" % self.location[0])
    FILE.write("%E **Y centro\n" % self.location[1])
    FILE.write("%E **Z centro\n" % self.location[2])
    FILE.write("%E **inner_radius\n" % self.inner_radius)
    FILE.write("%E **outer_radius\n" % self.outer_radius)
    FILE.write("%E **height\n" % self.height)
    FILE.write("{:E} **relative permittivity -> n=sqrt(mu_r*epsilon_r)={:.2f}\n".format(self.permittivity, sqrt(self.permittivity)))
    FILE.write("%E **relative conductivity\n" % self.conductivity)
    FILE.write("%E **angle of rotation in degrees around -Z=(0,0,-1)\n" % self.angle_deg)
    FILE.write('}\n')
    FILE.write('\n')
    
    #angle_degrees = rad2deg(Angle([0,1,0],self.axis))
    #if angle_degrees != 0:
      #rot = Rotation(name = 'cylinder_rotation', axis_point = self.location, axis_direction = cross([0,1,0],self.axis), angle_degrees = angle_degrees)
      #rot.write_entry(FILE)
    
    # TODO: BFDTD cylinders are along the Y axis by default, so rotation_axis_angle needs to be adapted for that... Just rotate back to Y first?
    #print(self.rotation_axis_angle)
    # HACK: We just always rotate for now. Adding the custom BFDTD object adder in Blender should fix this (but then for MPB/MEEP/etc... :/ )
    #rot = Rotation(name = self.name+'_rotation', axis_point = self.getCentro(), axis_direction = [1,0,0], angle_degrees = -90)
    #rot.write_entry(FILE)
    if self.rotation_axis_angle[0] != 0:
      rot = Rotation(name = self.name+'_rotation', axis_point = self.getLocation(), axis_direction = self.rotation_axis_angle[1:4], angle_degrees = rad2deg(self.rotation_axis_angle[0]))
      rot.write_entry(FILE)
      
    self.writeRotations(FILE)

  # TODO: take inner_radius into account, create 4 square meshing regions, implement per object meshing finesse (for all object types)
  def getMeshingParameters(self,xvec,yvec,zvec,epsx,epsy,epsz):
    objx = numpy.sort([self.location[0]-self.outer_radius,self.location[0]+self.outer_radius])
    objy = numpy.sort([self.location[1]-0.5*self.height,self.location[1]+0.5*self.height])
    objz = numpy.sort([self.location[2]-self.outer_radius,self.location[2]+self.outer_radius])
    eps = self.permittivity
    xvec = numpy.vstack([xvec,objx])
    yvec = numpy.vstack([yvec,objy])
    zvec = numpy.vstack([zvec,objz])
    epsx = numpy.vstack([epsx,eps])
    epsy = numpy.vstack([epsy,eps])
    epsz = numpy.vstack([epsz,eps])
    return xvec,yvec,zvec,epsx,epsy,epsz
    
  def getSize(self):
    # TODO: Take rotations into account?
    return numpy.array([2*self.outer_radius, self.height, 2*self.outer_radius])
    
  def writeCTL(self, FILE=sys.stdout, offset=numpy.array([0,0,0])):
    centro = self.getLocation() + offset
    FILE.write('  (make cylinder\n')
    FILE.write('    (material (make medium (epsilon {})) )\n'.format(self.getRelativePermittivity()))
    FILE.write('    (center (vector3 {} {} {}) )\n'.format(*centro))
    FILE.write('    (radius {})\n'.format(self.getOuterRadius()))
    FILE.write('    (height {})\n'.format(self.getHeight()))
    FILE.write('    (axis (vector3 {} {} {}) )\n'.format(*self.getAxis()))
    FILE.write('  )\n')

  def getMEEPobject(self):
    import meep
    meep_cylinder = meep.Cylinder(self.getOuterRadius(),
        axis=meep.Vector3(*self.getAxis()),
        height=self.getHeight(),
        material=meep.Medium(epsilon=self.getRelativePermittivity()),
        center=meep.Vector3(*self.getLocation()))
    return(meep_cylinder)

  def createBlenderObject(self, blender_operator, context):
    # Creates an object in blender and returns the created object
    
    # import necessary packages
    import bpy
    import numpy
    from blender_scripts.modules.GeometryObjects import add_cylinder, add_tetra, add_block
    from blender_scripts.modules.blender_utilities import selectObjects
    
    # get cursor location for placement
    cursor_location3 = numpy.array(bpy.context.scene.cursor.location)
    
    A,B = self.getStartEndPoints()
    obj = add_cylinder(self, A, B, name='BFDTD-Cylinder', cylinder_radius=self.getOuterRadius())
    return(obj)


class Tube(GeometryObject):
  def __init__(self):
    super().__init__()
    self.endpoint_1 = [1, 2, 3]
    self.a1 = 0.25
    self.b1 = 0.5
    
    self.endpoint_2 = [4, 5, 6]
    self.a2 = 0.5
    self.b2 = 1
    
    self.face_orientation = 'z'
  
  def setInnerRadius2(self, inner_radius_2):
    self.inner_radius_2 = inner_radius_2
    return(self.inner_radius_2)
  def setOuterRadius2(self, outer_radius_2):
    self.outer_radius_2 = outer_radius_2
    return(self.outer_radius_2)
  
  def getInnerRadius2(self):
    return(self.inner_radius_2)
  def getOuterRadius2(self):
    return(self.outer_radius_2)

  def getInnerRadius1(self):
    return(self.getInnerRadius())
  def getOuterRadius1(self):
    return(self.getOuterRadius())

  def write_entry(self, FILE=sys.stdout):
    '''
    TUBE
    {
      1-3 Coordinates of first end: X1, Y1, Z1
      4 **a1** first radius of the elliptical cross-section of the first end
      5 **b1** second radius of the elliptical cross-section of the first end
      6-8 Coordinates of second end: X2, Y2, Z2
      9 **a2** first radius of the elliptical cross-section of the second end
      10 **b2** second radius of the elliptical cross-section of the second end
      11 **face orientation** 1=x, 2=y or 3=z depending on which direction the tube is pointing
      12 **relative permittivity -> n=sqrt(mu_r*epsilon_r)
      13 **relative conductivity
    }
    '''
  
    FILE.write('CYLINDER **name='+self.name+'\n')
    FILE.write('{\n')
    FILE.write("%E **X centro\n" % self.location[0])
    FILE.write("%E **Y centro\n" % self.location[1])
    FILE.write("%E **Z centro\n" % self.location[2])
    FILE.write("%E **inner_radius\n" % self.inner_radius)
    FILE.write("%E **outer_radius\n" % self.outer_radius)
    FILE.write("%E **height\n" % self.height)
    FILE.write("{:E} **relative permittivity -> n=sqrt(mu_r*epsilon_r)={:.2f}\n".format(self.permittivity, sqrt(self.permittivity)))
    FILE.write("%E **relative conductivity\n" % self.conductivity)
    FILE.write("%E **angle of rotation in degrees around -Z=(0,0,-1)\n" % self.angle_deg)
    FILE.write('}\n')
    FILE.write('\n')
    
    #angle_degrees = rad2deg(Angle([0,1,0],self.axis))
    #if angle_degrees != 0:
      #rot = Rotation(name = 'cylinder_rotation', axis_point = self.location, axis_direction = cross([0,1,0],self.axis), angle_degrees = angle_degrees)
      #rot.write_entry(FILE)
    
    # TODO: BFDTD cylinders are along the Y axis by default, so rotation_axis_angle needs to be adapted for that... Just rotate back to Y first?
    #print(self.rotation_axis_angle)
    # HACK: We just always rotate for now. Adding the custom BFDTD object adder in Blender should fix this (but then for MPB/MEEP/etc... :/ )
    #rot = Rotation(name = self.name+'_rotation', axis_point = self.getCentro(), axis_direction = [1,0,0], angle_degrees = -90)
    #rot.write_entry(FILE)
    if self.rotation_axis_angle[0] != 0:
      rot = Rotation(name = self.name+'_rotation', axis_point = self.getLocation(), axis_direction = self.rotation_axis_angle[1:4], angle_degrees = rad2deg(self.rotation_axis_angle[0]))
      rot.write_entry(FILE)
      
    self.writeRotations(FILE)

class Rotation(object):
  # .. todo:: meshing params in case of rotations
  def __init__(self,
      name = None,
      axis_point = None,
      axis_direction = None,
      angle_degrees = None):
      
    if name is None: name = 'rotation'
    if axis_point is None: axis_point = [0,0,0]
    if axis_direction is None: axis_direction = [0,0,0]
    if angle_degrees is None: angle_degrees = 0
    
    self.name = name
    self.axis_point = axis_point
    self.axis_direction = axis_direction
    self.angle_degrees = angle_degrees
    
  def __str__(self):
    ret  = 'name = '+self.name+'\n'
    ret += 'axis_point = ' + str(self.axis_point) + '\n'
    ret += 'axis_direction = ' + str(self.axis_direction) + '\n'
    ret += 'angle_degrees = ' + str(self.angle_degrees)
    return ret
    
  def read_entry(self,entry):
    if entry.name:
      self.name = entry.name
    self.axis_point = float_array(entry.data[0:3])
    self.axis_direction = float_array(entry.data[3:6])
    self.angle_degrees = float(entry.data[6])
    
  def write_entry(self, FILE=sys.stdout):
    # rotation structure. Actually affects previous geometry object in Prof. Railton's modified BrisFDTD. Not fully implemented yet.
    # Should be integrated into existing structures using a directional vector anyway, like in MEEP. BrisFDTD hacking required... :)
    FILE.write('ROTATION **name='+self.name+'\n')
    FILE.write('{\n')
    FILE.write("%E **X axis_point\n" % self.axis_point[0])
    FILE.write("%E **Y axis_point\n" % self.axis_point[1])
    FILE.write("%E **Z axis_point\n" % self.axis_point[2])
    FILE.write("%E **X axis_direction\n" % self.axis_direction[0])
    FILE.write("%E **Y axis_direction\n" % self.axis_direction[1])
    FILE.write("%E **Z axis_direction\n" % self.axis_direction[2])
    FILE.write("%E **angle_degrees\n" % self.angle_degrees)
    FILE.write('}\n')
    FILE.write('\n')
    
  def getRotationMatrix(self):
    return rotation_matrix3(self.axis_direction, deg2rad(self.angle_degrees))

class MeshBox(GeometryObject):
  '''
  GeometryObject whose only function is to provide a custom "mesh box".
  
  Main attributes are the lists of *MeshParams* objects in X,Y,Z:
  
  * xmesh_params
  * ymesh_params
  * zmesh_params
  
  It also provides a getMeshingParameters() function.
  
  .. note:: I might keep this class, just because of rotations for the meshs... Mmh... Or is GeometryObject enough if it gets the MeshParams stuff?
  .. todo:: should inherit from Block class...
  '''
  def __init__(self,
    name = None,
    layer = None,
    group = None,
    lower = None,
    upper = None):

    raise Exception('MeshBox: This class is currently broken.')

    if name is None: name = 'mesh_box'
    if layer is None: layer = 'mesh_box'
    if group is None: group = 'mesh_box'
    if lower is None: lower = [0,0,0]
    if upper is None: upper = [1,1,1]
    
    GeometryObject.__init__(self)
    self.name = name
    self.layer = layer
    self.group = group
    self.lower = lower
    self.upper = upper
    
    # first mesh object list test case :)
    self.xmesh_params = [MeshingParameters(lower[0],upper[0])]
    self.ymesh_params = [MeshingParameters(lower[1],upper[1])]
    self.zmesh_params = [MeshingParameters(lower[2],upper[2])]
  
  def __str__(self):
    ret  = 'name = '+self.name+'\n'
    ret += 'lower = '+str(self.lower)+'\n'
    ret += 'upper = '+str(self.upper)+'\n'
    ret += 'xmesh_params:\n'
    for i in self.xmesh_params:
      ret += i.__str__() + '\n'
    ret += 'ymesh_params:\n'
    for i in self.ymesh_params:
      ret += i.__str__() + '\n'
    ret += 'zmesh_params:\n'
    for i in self.zmesh_params:
      ret += i.__str__() + '\n'
    ret += GeometryObject.__str__(self)
    return ret

  def getCentro(self):
    return [ 0.5*(self.lower[0]+self.upper[0]), 0.5*(self.lower[1]+self.upper[1]), 0.5*(self.lower[2]+self.upper[2]) ]
  
  def getMeshingParameters(self,xvec,yvec,zvec,epsx,epsy,epsz):
    ''' .. note:: adapting and leaving this until we have time to rework the automeshing function '''
    objx = numpy.sort([self.lower[0],self.upper[0]])
    objy = numpy.sort([self.lower[1],self.upper[1]])
    objz = numpy.sort([self.lower[2],self.upper[2]])
    xvec = numpy.vstack([xvec,objx])
    yvec = numpy.vstack([yvec,objy])
    zvec = numpy.vstack([zvec,objz])
    # .. todo:: Should merge the meshes if there are more than one...
    epsx = numpy.vstack([epsx,self.xmesh_params[0].getPermittivityMin()])
    epsy = numpy.vstack([epsy,self.ymesh_params[0].getPermittivityMin()])
    epsz = numpy.vstack([epsz,self.zmesh_params[0].getPermittivityMin()])
    return xvec,yvec,zvec,epsx,epsy,epsz
    
  def write_entry(self, FILE=sys.stdout):
    ''' .. note:: Does nothing for the moment. Could eventually add a nice little comment to the .geo or .inp file. Or we bypass it in the writeGeoFile function. '''
    return

def testPrinting():
  geolist = [Sphere(),
    Block(),
    Distorted(),
    Parallelepiped(),
    Ellipsoid(),
    Cylinder(),
    Tube()]
  for i in geolist:
    print(f'==={type(i)}===')
    print(i)
  return

if __name__ == '__main__':
  testPrinting()
