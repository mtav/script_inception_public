import bpy
import bfdtd.RCD

op = bpy.context.active_operator

(preset_vectors , preset_vectors_groups) = bfdtd.RCD.RCD111_waveguide_vector_dictionary()

op.method = 'three_arrays'
op.array_X_positive = True
op.array_X_positive_size = 2
op.array_Y_positive = True
op.array_Y_positive_size = 3
op.array_Z_positive = True
op.array_Z_positive_size = 4
op.array_X_negative = False
op.array_X_negative_size = 2
op.array_Y_negative = False
op.array_Y_negative_size = 3
op.array_Z_negative = False
op.array_Z_negative_size = 4
op.e1_vec3 = preset_vectors['rcd111-down-1']
op.e2_vec3 = preset_vectors['rcd111-down-2']
op.e3_vec3 = preset_vectors['rcd111-down-3']
op.use_scale = False
op.apply_scale = False
