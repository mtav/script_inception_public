import bpy
op = bpy.context.active_operator

op.view_align = False
op.location = (0.0, 0.0, 0.0)
op.rotation = (0.0, 0.0, 0.0)
op.size = 1.0
op.shift_cell = True
op.shift_origin = True
op.radius = 0.05000000074505806
op.add_unit_cell_BB = True
op.create_array = False
op.array_size_X = 2
op.array_size_Y = 3
op.array_size_Z = 4
op.cell_type = 'RCD111_inverse'
