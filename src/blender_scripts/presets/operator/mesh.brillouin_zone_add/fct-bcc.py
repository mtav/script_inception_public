import bpy
op = bpy.context.active_operator

op.view_align = False
op.rotation = (0.0, 0.0, 0.0)
op.location = (0.0, 0.0, 0.0)
op.lattice = 'FCT'
op.updating = False
op.a1 = (1.0, 0.0, 0.0)
op.a2 = (0.0, 1.0, 0.0)
op.a3 = (0.0, 0.0, 1.0)
op.b1 = (1.0, 0.0, 0.0)
op.b2 = (0.0, 1.0, 0.0)
op.b3 = (0.0, 0.0, 1.0)
op.unit_cube_size = (1.0, 1.0, 0.7071067690849304)
