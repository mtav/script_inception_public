import bpy
op = bpy.context.active_operator

op.view_align = False
op.rotation = (0.0, 0.0, 0.0)
op.location = (0.0, 0.0, 0.0)
op.scale = (2.0, 2.0, 2.0)
op.origin = (-1.0, -1.0, -1.0)
op.wiremode = True
