import bpy
op = bpy.context.active_operator

op.source = '4'
op.size = 1.0
op.vTrunc = 1.0
op.eTrunc = 1.0
op.snub = 'None'
op.dual = True
op.keepSize = False
op.preset = 'dr4'
