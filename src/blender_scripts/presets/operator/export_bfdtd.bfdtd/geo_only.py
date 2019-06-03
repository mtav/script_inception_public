import bpy
op = bpy.context.active_operator

op.filepath = '~/untitled'
op.filename = 'untitled'
op.directory = '~/'
op.write_geo = True
op.write_inp = False
op.write_in = False
op.write_sh = False
op.overwrite = True
