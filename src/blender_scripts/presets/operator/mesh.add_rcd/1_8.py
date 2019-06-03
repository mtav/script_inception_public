import bpy
op = bpy.context.active_operator

op.view_align = False
op.location = (-0.125, -0.125, -0.125)
op.rotation = (0.0, 0.0, 0.0)
op.size = 1.0
op.shifted = False
op.radius = 0.0
