import bpy
op = bpy.context.active_operator

op.align = 'WORLD'
op.location = (0.0, 0.0, 0.0)
op.rotation = (0.0, 0.0, 0.0)
op.size = 1.0
op.shift_cell = True
op.shift_origin = False
op.radius = 0.25999999046325684
op.add_unit_cell_BB = True
op.create_array = True
op.array_size_X = 13
op.array_size_Y = 7
op.array_size_Z = 2
op.cell_type = 'RCD111_v2'
op.RCD111_v2_advanced = False
op.RCD111_v2_location = (0.0, 0.0, 0.0)
op.RCD111_v2_size = (0.7071067690849304, 1.2247449159622192, 1.7320507764816284)
