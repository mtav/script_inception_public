import bpy
op = bpy.context.active_operator

op.origin = (1.0, 2.0, 3.0)
op.direction_specification_style = 'vector'
op.e3_vec3 = (4.0, 5.0, 6.0)
op.e1_vec3 = (7.0, 8.0, 9.0)
op.norm_specification_style = 'normalized'
op.e1_norm = 10.0
op.e2_norm = 11.0
op.e3_norm = 12.0
op.bool_inverse = False
