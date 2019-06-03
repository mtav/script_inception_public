import bpy
op = bpy.context.active_operator

op.location = (0.0, 0.0, 0.0)
op.view_align = False
op.rotation = (0.0, 0.0, 0.0)
op.lattice = 'FCT'
op.updating = False
op.a1 = (0.0, 0.5, 0.4000000059604645)
op.a2 = (0.5, 0.0, 0.4000000059604645)
op.a3 = (0.5, 0.5, 0.0)
op.b1 = (-1.0, 1.0, 1.25)
op.b2 = (1.0, -1.0, 1.25)
op.b3 = (1.0, 1.0, -1.25)
op.unit_cube_size = (1.0, 1.0, 0.800000011920929)
