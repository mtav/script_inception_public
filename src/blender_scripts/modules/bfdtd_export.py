#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# To make Blender happy:
bl_info = {"name":"bfdtd_export - EXPERIMENTAL",
            "category": "Import-Export",
            'warning': 'Under construction!'
}

"""
Name: 'Bristol FDTD (*.in,*.geo,*.inp)'
Blender: 249
Group: 'Export'
Tooltip: 'Export to Bristol FDTD'
"""

import Blender
import bpy
import BPyMesh

def write(filename):
  
  Blender.Window.WaitCursor(1)
  
  if not filename.lower().endswith('.begc'):
    filename += '.begc'
  out = file(filename, "w")
  objects = Blender.Object.GetSelected()
  
  num_objects = 0
  for object in objects:
    if object.type == 'Mesh':
      num_objects = num_objects + 1
      
  out.write('%d\n' % num_objects)
  node_offset = 0
  for object in objects:
    if object.type == 'Mesh':
      out.write(object.name)
      out.write('\n')
  for object in objects:
    if object.type == 'Mesh':

      mesh = BPyMesh.getMeshFromObject(object, None, True, False, bpy.data.scenes.active)
      #mesh  = object.getData(0,1)
      mesh.transform(object.matrixWorld)
      faces = mesh.faces
      nodes = mesh.verts
      out.write('%d' % len(nodes))
      out.write(' %d\n' % len(faces))
      for n in nodes:
        #out.write("%e " % n.co[0])
        #out.write("%e " % n.co[1])
        #out.write("%e\n" % n.co[2])
        out.write("%e "  % n.co[0])
        out.write("%e "  % n.co[1])
        out.write("%e\n" % n.co[2])
      for f in faces:
        N = len(f.verts)
        if N < 3 and N > 4:
          Blender.Draw.PupMenu('Error%t|Only triangles and quads allowed')
          return
        out.write("%d" % N)
        for v in f.verts:
          out.write(' %d' % (v.index + node_offset))
        out.write('\n')
      node_offset = node_offset + len(nodes)

  Blender.Window.WaitCursor(0)

###############################
# IMPORTS
###############################
import os
import pickle

###############################
# INITIALIZATIONS
###############################
cfgfile = Blender.Get("datadir")+'/BlenderExport.txt'

###############################
# EXPORT FUNCTION
###############################
def exportBristolFDTD(dir_name):
    ''' export BristolFDTD geometry '''
    print(('----->Exporting as bristol FDTD geometry into: ' + dir_name))
    Blender.Window.WaitCursor(1);

    if os.path.isdir(dir_name) == False:
      dir_name = os.path.dirname(dir_name)
      
    # save export path
    FILE = open(cfgfile, 'w');
    pickle.dump(dir_name, FILE);
    FILE.close();
    
    print('dir_name=', dir_name)
    
    #########################
    # Not yet implemented:
    # Flag
    # structured_entries.flag;
    # Boundaries
    # structured_entries.boundaries;
    #########################
    
    Blender.Window.WaitCursor(0);
    print('...done')

###############################
# MAIN FUNCTION
###############################
def main():
  ''' MAIN FUNCTION '''
  ###################
  # load export path
  ###################
  default_path = os.getenv('DATADIR')
  print(('cfgfile = ', cfgfile))

  if os.path.isfile(cfgfile) and os.path.getsize(cfgfile) > 0:
    with open(cfgfile, 'r') as FILE:
      default_path = pickle.load(FILE);
  ###################

  ###################
  # export file
  ###################
  Blender.Window.FileSelector(exportBristolFDTD, "Export Bristol FDTD file...", default_path);

if __name__ == "__main__":
  main()
