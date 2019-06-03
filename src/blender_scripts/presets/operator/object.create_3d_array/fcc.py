import bpy
op = bpy.context.active_operator

op.array_size_X = 3
op.array_size_Y = 3
op.array_size_Z = 4
op.e1_vec3 = (0.0, 0.5, 0.5)
op.e2_vec3 = (0.5, 0.0, 0.5)
op.e3_vec3 = (0.5, 0.5, 0.0)
