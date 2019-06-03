import bpy
op = bpy.context.active_operator

op.rotation = (0.0, 0.0, 0.0)
op.location = (0.5, -0.5, 0.5)
op.view_align = False
op.updating = False
op.method = 'e1,e2,e3'
op.e1_vec3 = (1.0, -1.0, 1.0)
op.e2_vec3 = (0.0707106813788414, 0.0707106813788414, 0.0)
op.e3_vec3 = (0.0, 0.0, 0.30000001192092896)
op.size_vec3 = (1.7320507764816284, 0.10000000149011612, 0.30000001192092896)
op.size_from_vectors = True
op.LineNumber_method = 'use_line_number'
op.voxelsize_vec3 = (0.15000000596046448, 0.15000000596046448, 0.44999998807907104)
op.overlap_vec3 = (0.0, 0.0, 0.5)
op.LineNumber_vec3 = (5, 3, 4)
op.connected = True
