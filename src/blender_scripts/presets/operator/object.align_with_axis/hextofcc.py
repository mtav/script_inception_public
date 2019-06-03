import bpy
op = bpy.context.active_operator

op.origin = (0.0, 0.0, 0.0)
op.direction_specification_style = 'vector'
op.e3_vec3 = (1.0, 1.0, 1.0)
op.e1_vec3 = (0.0, -1.0, -2.0)
op.norm_specification_style = 'normalized'
op.e1_norm = 1.0
op.e2_norm = 1.0
op.e3_norm = 1.0
op.bool_inverse = True
