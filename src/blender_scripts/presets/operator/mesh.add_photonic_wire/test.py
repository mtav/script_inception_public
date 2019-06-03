import bpy
op = bpy.context.active_operator

op.view_align = False
op.location = (0.0, 0.0, 0.0)
op.rotation = (0.0, 0.0, 0.0)
op.length = 100.0
op.height = 30.0
op.bend_radius = 30.0
op.wire_diametre = 5.0
op.cone_diametre = 10.0
op.show_design = True
op.show_gwl = False
op.cross_section_delta_sync = False
op.cross_section_r0 = 0.05000000074505806
op.cross_section_delta_r = 0.10000000149011612
op.cross_section_delta_theta = 0.10000000149011612
op.longitudinal_delta_sync = False
op.bend_delta = 0.10000000149011612
op.cone_delta = 0.10000000149011612
op.wire_delta = 0.10000000149011612
