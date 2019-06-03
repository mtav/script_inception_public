import bpy
op = bpy.context.active_operator

op.view_align = False
op.location = (0.0, 0.0, 0.0)
op.rotation = (0.0, 0.0, 0.0)
op.size = 1.0
op.shift_cell = False
op.shift_origin = False
op.radius = 0.0
op.add_unit_cell_BB = False
op.create_array = False
op.array_size_X = 2
op.array_size_Y = 3
op.array_size_Z = 4
op.cell_type = 'RCD111_v2'
op.RCD111_v2_advanced = True
op.RCD111_v2_location = (0.0, 0.0, 0.0)
op.RCD111_v2_size = (2.0, 2.0, 1.7320507764816284)
