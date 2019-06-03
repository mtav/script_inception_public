import bpy
op = bpy.context.active_operator

op.view_align = False
op.location = (0.0, 0.0, 0.0)
op.rotation = (0.0, 0.0, 0.0)
op.length = 30.0
op.height = 10.0
op.bend_radius = 10.0
op.wire_diametre = 5.0
op.cone_diametre = 10.0
op.show_design = True
op.show_gwl = True
op.cross_section_delta_sync = False
op.cross_section_r0 = 0.25
op.cross_section_delta_r = 0.5
op.cross_section_delta_theta = 0.5
op.longitudinal_delta_sync = False
op.bend_delta = 0.5
op.cone_delta = 0.5
op.wire_delta = 0.5
