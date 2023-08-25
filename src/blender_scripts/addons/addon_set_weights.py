#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# script to color an object by vertex index
# work in progress

bl_info = {
    "name": "Set weights to vertex index",
    "author": "mtav",
    "version": (1, 0),
    "blender": (3, 4, 0),
    "location": "View3D -> SIP menu",
    "description": "Set weights to vertex index",
    "warning": "",
    "wiki_url": "",
    "category": "Object",
    }

import bpy

def SetWeightsToVertexIndices_main(context):
  ob = bpy.context.object
  me = ob.data

  if len(ob.vertex_groups)==0:
      bpy.ops.object.vertex_group_add()

  # vgroups = {i: vgroup.name for i, vgroup in enumerate(ob.vertex_groups)}

  N = len(me.vertices)

  print('Setting weights...')
  for i, vgroup in enumerate(ob.vertex_groups):
      for v_idx, v in enumerate(me.vertices):
          vgroup.add([v_idx], v_idx/(N-1), 'REPLACE')
          #vgroup.add([v_idx], (v.co.x+1)/ob.dimensions[0], 'REPLACE')
          #vgroup.add([v_idx], (v.co.y+1)/ob.dimensions[1], 'REPLACE')
          # vgroup.add([v_idx], (v.co.z+1)/ob.dimensions[2], 'REPLACE')

  # print('------------------------')
  # for v_idx, v in enumerate(me.vertices):
      # print("v_idx = {} Vertex {}".format(v_idx, v.index))
      # for group in v.groups:
          # print("  %s = %f" % (vgroups[group.group], group.weight))
  print('...DONE')
  return

class SetWeightsToVertexIndices(bpy.types.Operator):
    """Tooltip"""
    bl_idname = "object.set_weights_to_vertex_indices"
    bl_label = "Set weights to vertex indices"

    @classmethod
    def poll(cls, context):
      return context.active_object is not None

    def execute(self, context):
      SetWeightsToVertexIndices_main(context)
      return {'FINISHED'}

def register():
  bpy.utils.register_class(SetWeightsToVertexIndices)

def unregister():
  bpy.utils.unregister_class(SetWeightsToVertexIndices)

if __name__ == "__main__":
  register()
  
  # test call
  # bpy.ops.object.set_weights_to_vertex_indices()
