#!/usr/bin/env python3
# -*- coding: utf-8 -*-

bl_info = {
    "name": "Add arrow",
    "author": "mtav",
    "version": (1, 0),
    "blender": (3, 6, 0),
    "location": "View3D > Add > Mesh > New Arrow",
    "description": "Adds a new Arrow Mesh Object",
    "warning": "",
    "wiki_url": "",
    "category": "Add Mesh",
    }

import bpy
import numpy
from bpy.types import Operator
from bpy.props import FloatVectorProperty, FloatProperty, EnumProperty, BoolProperty
from bpy_extras.object_utils import AddObjectHelper, object_data_add
from mathutils import Vector

import bfdtd.RCD
from blender_scripts.modules.GeometryObjects import add_arrow
from blender_scripts.modules.blender_utilities import setOrigin, selectObjects, add_array_modifier, createGroup

# .. todo:: Create separate addon for preset vectors? (Or the use standard preset files, prepared in advance?)

class OBJECT_OT_add_arrow(Operator):
    """Create a new Mesh Object"""
    bl_idname = "mesh.add_arrow"
    bl_label = "Add Arrow Mesh Object"
    bl_options = {'REGISTER', 'UNDO', 'PRESET'}

    start_point : FloatVectorProperty(
            name="start_point",
            default=(0,0,0),
            description="start point",
            )

    end_point : FloatVectorProperty(
            name="end_point",
            default=(1,1,1),
            description="end point",
            )

    origin : FloatVectorProperty(
            name="origin",
            default=(0,0,0),
            description="start point",
            )

    vector : FloatVectorProperty(
            name="vector",
            default=(1,1,1),
            description="end point",
            )

    cone_length : FloatProperty(
            name="cone_length",
            default=1/5.0,
            description="cone length",
            min=0,
            )

    cone_radius : FloatProperty(
            name="cone_radius",
            default=1/20.0,
            description="cone radius",
            min=0,
            )

    cylinder_radius : FloatProperty(
            name="cylinder_radius",
            default=1/40.0,
            description="cylinder radius",
            min=0,
            )
    
    method : EnumProperty(items = (("start_and_end","start+end point","start+end point"),
                                      ("origin_and_vector","origin+vector","origin+vector"),
                                      ("arrow_presets","arrow presets","arrow presets"),
                                      ("arrow_group_presets","arrow group presets","arrow group presets"),
                                      ), default='origin_and_vector', name = "Method:")
    
    #(preset_vectors , preset_vectors_groups) = bfdtd.RCD.RCD_vector_dictionary()
    (preset_vectors , preset_vectors_groups) = bfdtd.RCD.RCD111_waveguide_vector_dictionary()
    
    #preset_labels = ['Custom']
    #preset_labels.extend(preset_vectors.keys())
    #preset = EnumProperty(items = ((i,i,i) for i in preset_labels), default=preset_labels[0], name = "Presets:")
    
    preset_vectors_enum : EnumProperty(items = ((i,i,i) for i in preset_vectors.keys()), name = "Preset vectors:")
    preset_vectors_groups_enum : EnumProperty(items = ((i,i,i) for i in preset_vectors_groups.keys()), name = "Preset vector groups:")
    
    # cf /usr/share/blender/scripts/addons/add_mesh_extra_objects/add_mesh_solid.py
    #previous preset, for User-friendly reasons
    #previousSetting = preset_labels[0]
    
    def invoke(self, context, event):
        '''
        Operator.invoke is used to initialize the operator from the context at the moment the operator is called.
        invoke() is typically used to assign properties which are then used by execute().
        '''
        self.report({'INFO'}, 'arrow addon invoke called')
        # Use initial cursor location
        self.start_point = self.origin = self.location = numpy.array(bpy.context.scene.cursor.location)
        return self.execute(context)
    
    def draw(self, context):
      
      # .. todo:: Add vector info box with coords of preset vectors, names, etc? cf tapsterite addon for layout reference
      
      layout = self.layout
      box = layout.box()
      
      box.prop(self, 'method')
      if self.method == 'start_and_end':
        box.prop(self, 'start_point')
        box.prop(self, 'end_point')
      elif self.method == 'origin_and_vector':
        box.prop(self, 'origin')
        box.prop(self, 'vector')
      elif self.method == 'arrow_presets':
        box.prop(self, 'preset_vectors_enum')
        box.prop(self, 'start_point')
      elif self.method == 'arrow_group_presets':
        box.prop(self, 'preset_vectors_groups_enum')
        box.prop(self, 'start_point')
      else:
        raise
      
      #box.prop(self, 'preset')
      
      #if self.preset == self.preset_labels[0]:
        #box.prop(self, 'method')
        
        #if self.method == 'start_and_end':
          #box.prop(self, 'start_point')
          #box.prop(self, 'end_point')
        #elif self.method == 'origin_and_vector':
          #box.prop(self, 'origin')
          #box.prop(self, 'vector')
        #else:
          #raise
      
      box.prop(self, 'cone_length')
      box.prop(self, 'cone_radius')
      box.prop(self, 'cylinder_radius')
      
      return

    def execute(self, context):
      
      V_list = []
      group_name = 'arrow_group'
      
      if self.method == 'start_and_end':
        self.origin = self.start_point
        self.vector = Vector(self.end_point) - Vector(self.start_point)
        V_list.append(('custom_arrow', self.vector))
      elif self.method == 'origin_and_vector':
        self.start_point = self.origin
        self.end_point = Vector(self.origin) + Vector(self.vector)
        V_list.append(('custom_arrow', self.vector))
      elif self.method == 'arrow_presets':
        V_list.append((self.preset_vectors_enum, self.preset_vectors[self.preset_vectors_enum]))
      elif self.method == 'arrow_group_presets':
        group_name = self.preset_vectors_groups_enum
        for k in self.preset_vectors_groups[self.preset_vectors_groups_enum]:
          V_list.append((k, self.preset_vectors[k]))
      else:
        raise Exception(f'self.method undefined: self.method = {self.method}')
      
      obj_list = []
      for (name, V) in V_list:
        arrow = add_arrow(self, self.start_point, Vector(self.start_point) + Vector(V), cone_length=self.cone_length, cone_radius=self.cone_radius, cylinder_radius=self.cylinder_radius)
        arrow.name = name
        obj_list.append(arrow)
      
      if len(obj_list) > 1:
        createGroup(obj_list, active_object=None, context = bpy.context, group_name=group_name)
      return {'FINISHED'}

# Registration
def add_arrow_button(self, context):
    self.layout.operator(
        OBJECT_OT_add_arrow.bl_idname,
        text="Add Arrow Object",
        icon='PLUGIN')

# This allows you to right click on a button and link to the manual
def add_arrow_manual_map():
    url_manual_prefix = "http://wiki.blender.org/index.php/Doc:2.6/Manual/"
    url_manual_mapping = (
        ("bpy.ops.mesh.add_arrow", "Modeling/Objects"),
        )
    return url_manual_prefix, url_manual_mapping

def register():
    bpy.utils.register_class(OBJECT_OT_add_arrow)
    bpy.utils.register_manual_map(add_arrow_manual_map)
    bpy.types.VIEW3D_MT_mesh_add.append(add_arrow_button)

def unregister():
    bpy.utils.unregister_class(OBJECT_OT_add_arrow)
    bpy.utils.unregister_manual_map(add_arrow_manual_map)
    bpy.types.VIEW3D_MT_mesh_add.remove(add_arrow_button)

if __name__ == "__main__":
    register()
