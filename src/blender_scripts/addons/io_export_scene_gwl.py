#!/usr/bin/env python3
# -*- coding: utf-8 -*-

bl_info = {
    'name': 'Export GWL Format (.gwl)',
    'author': 'mtav',
    'version': (0, 0, 1),
    'blender': (2, 63, 0),
    'location': 'File > Export > GWL (.gwl)',
    'description': 'Export files to the GWL format (.gwl)',
    'warning': '',
    'wiki_url': '',
    'tracker_url': '',
    'category': 'Import-Export',
    }

import os
import sys
import bpy
from bpy.props import FloatVectorProperty, IntProperty, FloatProperty, BoolProperty, StringProperty, EnumProperty
from bpy.types import Operator

# ExportHelper is a helper class, defines filename and invoke() function which calls the file selector.
from bpy_extras.io_utils import ExportHelper
from blender_scripts.modules import blender_utilities

from GWL.GWL_parser import GWLobject

# TODO: Add "edge following" to draw subdivided lines in one go (test with subdivided woodpile mesh). (maybe blender mesh loops can help? or some bmesh utilities)
# TODO: Custom power compensation formula

def writeVoxel(file_object, vertex, laser_power_at_z0=None, K=None, interfaceAt=0, bool_LaserPowerCommand=False, lastPower=None, bool_InverseWriting=False, float_height=0):
  
  power = None
  
  if laser_power_at_z0 is not None:
    
    # calculate power
    if K is not None:
      if bool_InverseWriting:
        power = (1+K*((float_height-vertex.co[2])+interfaceAt))*laser_power_at_z0
      else:
        power = (1+K*(vertex.co[2]-interfaceAt))*laser_power_at_z0
    else:
      power = laser_power_at_z0

    # restrict the power to valid values
    if power<0: power=0
    if power>100: power=100
    
    # write according to settings
    if bool_LaserPowerCommand:
        if power != lastPower:
#            print((power, lastPower))
            file_object.write("LaserPower %.3f\n" % power)
        file_object.write("%.3f\t%.3f\t%.3f\n" % (vertex.co[0], vertex.co[1], vertex.co[2]))
    else:
        file_object.write("%.3f\t%.3f\t%.3f\t%.3f\n" % (vertex.co[0], vertex.co[1], vertex.co[2], power))
    
  else:
    # write without any power-related settings
    file_object.write("%.3f\t%.3f\t%.3f\n" % (vertex.co[0], vertex.co[1], vertex.co[2]))
  
  return(power)

def write_GWL(context, filepath, laser_power_at_z0=None, K=None, interfaceAt=0, bool_LaserPowerCommand=False, bool_InverseWriting=False, float_height=0, one_file_per_object=False, obj_list=[]):
      # TODO: Use bpy.ops.mesh.separate(type='LOOSE') or similar algorithm to detect continuous lines properly.
      # .. todo:: Convert to mesh if it is a curve or other...
      
      # print("Exporting selected objects to GWL:", filepath)
      # (filepath_root, filepath_ext) = os.path.splitext(filepath)
      # obj_list = list(context.selected_objects)
      # obj_list.sort(key = lambda x : x.name)
      # return
      
      lastPower = None
      
      with open(filepath, 'w', encoding='utf-8') as f:

        ## method 0: sort by GWLindex
        #obj_list = []
        #for obj in context.selected_objects:
          #if 'GWLindex' in obj.keys():
            #GWLindex = obj['GWLindex']
          #else:
            #GWLindex = -1
          #obj_list.append((obj,GWLindex))
          
        #obj_list.sort(key=lambda x:x[1])

        # method 1: sort by name
        # obj_list = list(context.selected_objects)
        # obj_list.sort(key = lambda x : x.name)

        #for (obj,GWLindex) in obj_list:
        for obj in obj_list:
          
            print(obj.name)
            #if GWLindex<0:
              #print('WARNING: '+obj.name+' has no specified index.',file=sys.stderr)
            
            f.write('% '+obj.name+'\n')
            
            #print(obj)
            #f.write(str(obj)+'\n')

            ### not good, because we transform the mesh before export, so better to make a copy with "obj.to_mesh(...)"
            #mesh = obj.data

            ### for reference, cf: scripts/addons/io_mesh_stl/
            #mesh.transform(global_matrix * ob.matrix_world)
                #global_matrix = axis_conversion(to_forward=self.axis_forward,
                                                #to_up=self.axis_up,
                                                #).to_4x4() * Matrix.Scale(self.global_scale, 4)
            #try:
                #mesh = ob.to_mesh(bpy.context.scene, use_mesh_modifiers, "PREVIEW")
            #except RuntimeError:
                #raise StopIteration

            # get the modifiers (mirrors, arrays, etc)
            try:
                mesh = obj.to_mesh(bpy.context.scene, apply_modifiers=True, settings='PREVIEW')
            except RuntimeError:
                raise StopIteration

            # apply loc, rot, scale
            mesh.transform(obj.matrix_world)
        
            # method 2
            last_vertex = -1
            for edge in mesh.edges:
              A_vertex_idx = edge.vertices[0]
              B_vertex_idx = edge.vertices[1]
              A_vertex = mesh.vertices[A_vertex_idx]
              B_vertex = mesh.vertices[B_vertex_idx]
              
              # TODO: Use GWLobject class for this... (although that would mean looping more than necessary = bad). Using C++ code might work around the speed issues and allow us to combine python, C++, scheme, VTK. etc more nicely possibly.
              
              if (last_vertex < 0):
                # first edge
                lastPower = writeVoxel(f, A_vertex, laser_power_at_z0, K, interfaceAt, bool_LaserPowerCommand, lastPower, bool_InverseWriting, float_height)
                lastPower = writeVoxel(f, B_vertex, laser_power_at_z0, K, interfaceAt, bool_LaserPowerCommand, lastPower, bool_InverseWriting, float_height)
              else:
                if (A_vertex_idx == last_vertex):
                  # new continuing edge
                    lastPower = writeVoxel(f, B_vertex, laser_power_at_z0, K, interfaceAt, bool_LaserPowerCommand, lastPower, bool_InverseWriting, float_height)
                else:
                  # new separate edge
                  f.write('Write\n')
                  lastPower = writeVoxel(f, A_vertex, laser_power_at_z0, K, interfaceAt, bool_LaserPowerCommand, lastPower, bool_InverseWriting, float_height)
                  lastPower = writeVoxel(f, B_vertex, laser_power_at_z0, K, interfaceAt, bool_LaserPowerCommand, lastPower, bool_InverseWriting, float_height)
              
              last_vertex = B_vertex_idx
            
            f.write('Write\n')
            
            ## method 1
            #edge_list = []
            
            #for edge in mesh.edges:
              #edge_list.append((edge.vertices[0],edge.vertices[1]))
            
            #for idx in range(len(mesh.vertices)):
              #vertex = mesh.vertices[idx]
              #f.write("%.3f %.3f %.3f\n" % (vertex.co[0], vertex.co[1], vertex.co[2]))
              #if idx+1<len(mesh.vertices):
                #if (idx,idx+1) not in edge_list:
                  #f.write('Write\n')
            #f.write('Write\n')
            
            ## method 0
            #for vertex in mesh.vertices:
              ##print(vertex.co)
              #f.write("%.3f %.3f %.3f\n" % (vertex.co[0], vertex.co[1], vertex.co[2]))
            #f.write('Write\n')
                
            #vlist=mesh.vertices
            #v=vlist[0]
            #print(v.co)
            #print([v.co[0],v.co[1],v.co[2]])
            
      return {'FINISHED'}

class ExportGWL(Operator, ExportHelper, GWLobject):
    '''This appears in the tooltip of the operator and in the generated docs'''
    bl_idname = "export_gwl.gwl"  # important since its how bpy.ops.import_test.GWL is constructed
    bl_label = "Export to .gwl"
    bl_options = {'PRESET'}

    # ExportHelper mixin class uses this
    filename_ext = ".gwl"

    filter_glob = StringProperty(
            default="*.gwl",
            options={'HIDDEN'},
            )

    # List of operator properties, the attributes will be assigned
    # to the class instance from the operator settings before calling.
    bool_setPower = BoolProperty(name="Add power coordinate", description="Add power coordinate?", default=False)
    bool_LaserPowerCommand = BoolProperty(name="Use LaserPower comand", description="Use LaserPower comand instead of 4th voxel coordinate", default=False)
    bool_addPowerCompensation = BoolProperty(name="Add power compensation", description="Add power compensation?", default=False)
    bool_InverseWriting = BoolProperty(name="InverseWriting", description="InverseWriting", default=False)

    laser_power_at_z0 = FloatProperty(name="LaserPower at z0", description="LaserPower at z0 = interfaceAt (or for all if power compensation disabled)", default=15, precision=3, min=0, max=100)
    K = FloatProperty(name="K", description="Power compensation slope", default=0.0076, precision=6)
    interfaceAt = FloatProperty(name="interfaceAt", description="interfaceAt", default=0, precision=3)
    float_height = FloatProperty(name="float_height", description="float_height bla bla", default=0, precision=3)

    reverse_line_order_on_write = BoolProperty(name="reverse line order on write", default=False)
    reverse_voxel_order_per_line_on_write = BoolProperty(name="reverse voxel order per line", default=False)

    one_file_per_object = BoolProperty(name="one file per object", default=False)

    def execute(self, context):
      # We could pass all the boolean arguments, but the reduce the length of the argument list (and to allow using an external function), we pass them via their corresponding numerical variables.
      laser_power_at_z0 = self.laser_power_at_z0
      K = self.K
      if not self.bool_setPower:
        laser_power_at_z0 = None
      if not self.bool_addPowerCompensation:
        K = None
      
      print("Exporting selected objects to GWL:", self.filepath)
      (filepath_root, filepath_ext) = os.path.splitext(self.filepath)
      obj_list = list(context.selected_objects)
      obj_list.sort(key = lambda x : x.name)
      if self.one_file_per_object:
        with open(self.filepath, 'w') as f:
          for obj in obj_list:
            f.write('Include {}.{}.gwl\n'.format(os.path.basename(filepath_root), obj.name))
        for obj in obj_list:
          ret = write_GWL(context, '{}.{}.gwl'.format(filepath_root, obj.name), laser_power_at_z0, K, self.interfaceAt, self.bool_LaserPowerCommand, self.bool_InverseWriting, self.float_height, one_file_per_object=self.one_file_per_object, obj_list=[obj])
      else:
        ret = write_GWL(context, self.filepath, laser_power_at_z0, K, self.interfaceAt, self.bool_LaserPowerCommand, self.bool_InverseWriting, self.float_height, one_file_per_object=self.one_file_per_object, obj_list=obj_list)
      
      # return write_GWL(context, self.filepath, laser_power_at_z0, K, self.interfaceAt, self.bool_LaserPowerCommand, self.bool_InverseWriting, self.float_height, one_file_per_object=self.one_file_per_object)
      return(ret)

    def draw(self, context):
        layout = self.layout
        
        box = layout.box()
        box.prop(self, 'one_file_per_object')

        box = layout.box()
        box.prop(self, 'reverse_line_order_on_write')
        box.prop(self, 'reverse_voxel_order_per_line_on_write')
        
        box = layout.box()
        box.prop(self, 'bool_setPower')
        if self.bool_setPower:
          box.prop(self, 'laser_power_at_z0')
          box.prop(self, 'bool_LaserPowerCommand')
          box.prop(self, 'bool_addPowerCompensation')
          if self.bool_addPowerCompensation:
            box.prop(self, 'bool_InverseWriting')
            if self.bool_InverseWriting:
              box.prop(self, 'float_height')
              box.label(text="power(z) = (1+K*((H-z)+interfaceAt))*laser_power_at_z0")
            else:
              box.label(text="power(z) = (1+K*(z-interfaceAt))*laser_power_at_z0")
            box.prop(self, 'K')
            box.prop(self, 'interfaceAt')

        #box.prop(self, 'bool_setPower')
        #box.prop(self, 'Add power coordinate')
        ##box.prop(self, 'outer_radius')
        ##box.prop(self, 'height')
        ##box.prop(self, 'method')
        ##box.prop(self, 'PointDistance')
        ##box.prop(self, 'downwardWriting')
        ##if self.method == 'vertical lines':
          ##box.prop(self, 'zigzag')
        ##if self.method == 'spiral':
          ##box.prop(self, 'rotateSpirals')
        ##box.pro
        

# Only needed if you want to add into a dynamic menu
def menu_func_export(self, context):
    self.layout.operator(ExportGWL.bl_idname, text="Nanoscribe GWL (.gwl)")


def register():
    bpy.utils.register_class(ExportGWL)
    bpy.types.INFO_MT_file_export.append(menu_func_export)


def unregister():
    bpy.utils.unregister_class(ExportGWL)
    bpy.types.INFO_MT_file_export.remove(menu_func_export)


if __name__ == "__main__":
    register()

    # test call
    bpy.ops.export_gwl.gwl('INVOKE_DEFAULT')
    
    #write_GWL(bpy.context, 'untitled.gwl', laser_power_at_z0=None, K=None, interfaceAt=0, bool_LaserPowerCommand=False)
    #write_GWL(bpy.context, 'untitled.P123.gwl', laser_power_at_z0=123, K=None, interfaceAt=0, bool_LaserPowerCommand=False)
    #write_GWL(bpy.context, 'untitled.P123.K1.gwl', laser_power_at_z0=123, K=1, interfaceAt=0, bool_LaserPowerCommand=False)
    #write_GWL(bpy.context, 'untitled.P123.K1.iface-1.gwl', laser_power_at_z0=123, K=1, interfaceAt=-1, bool_LaserPowerCommand=False)

    #write_GWL(bpy.context, 'untitled.LP.gwl', laser_power_at_z0=None, K=None, interfaceAt=0, bool_LaserPowerCommand=True)
    #write_GWL(bpy.context, 'untitled.P123.LP.gwl', laser_power_at_z0=123, K=None, interfaceAt=0, bool_LaserPowerCommand=True)
    #write_GWL(bpy.context, 'untitled.P123.K1.LP.gwl', laser_power_at_z0=123, K=1, interfaceAt=0, bool_LaserPowerCommand=True)
    #write_GWL(bpy.context, 'untitled.P123.K1.iface-1.LP.gwl', laser_power_at_z0=123, K=1, interfaceAt=-1, bool_LaserPowerCommand=True)
