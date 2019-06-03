#!/usr/bin/env python3
# -*- coding: utf-8 -*-

bl_info = {
    "name": "hide/hide_render copier",
    "author": "mtav",
    "version": (1, 0),
    "blender": (2, 78, 0),
    "location": "spacebar menu",
    "description": "Makes setting hide=hide_render or vice-versa for all objects easier.",
    "warning": "",
    "wiki_url": "",
    "category": "Object"}

import bpy

class HideToHideRenderOperator(bpy.types.Operator):
    """Tooltip"""
    bl_idname = "object.hide_to_hide_render"
    bl_label = "hide to hide_render"

    @classmethod
    def poll(cls, context):
        return context.active_object is not None

    def execute(self, context):
        for ob in context.scene.objects:
            ob.hide_render = ob.hide
        return {'FINISHED'}

class HideRenderToHideOperator(bpy.types.Operator):
    """Tooltip"""
    bl_idname = "object.hide_render_to_hide"
    bl_label = "hide_render to hide"

    @classmethod
    def poll(cls, context):
        return context.active_object is not None

    def execute(self, context):
        for ob in context.scene.objects:
            ob.hide = ob.hide_render
        return {'FINISHED'}

def register():
    bpy.utils.register_class(HideRenderToHideOperator)
    bpy.utils.register_class(HideToHideRenderOperator)


def unregister():
    bpy.utils.unregister_class(HideRenderToHideOperator)
    bpy.utils.unregister_class(HideToHideRenderOperator)


if __name__ == "__main__":
    register()
