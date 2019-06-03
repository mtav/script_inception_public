import bpy
op = bpy.context.active_operator

op.origin = (0.0, -1.0, 0.0)
op.direction_specification_style = 'endpoint'
op.e3_vec3 = (-0.5, -0.5, -0.5)
op.e1_vec3 = (1.0, 0.0, 0.0)
op.norm_specification_style = 'specific_norm'
op.e1_norm = 0.20000000298023224
op.e2_norm = 0.20000000298023224
op.e3_norm = 0.8660253882408142
