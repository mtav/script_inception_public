import bpy
op = bpy.context.active_operator

op.location = (0.0, 0.0, 0.0)
op.view_align = False
op.rotation = (0.0, 0.0, 0.0)
op.scale = (1.0, 1.0, 1.0)
op.origin = (-0.5, -0.5, -0.5)
op.wiremode = True
