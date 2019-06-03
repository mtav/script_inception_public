import bpy
op = bpy.context.active_operator

op.filepath = '/tmp/untitled'
op.filename = 'untitled'
op.directory = '/tmp/'
op.write_geo = True
op.write_inp = True
op.write_in = True
op.write_sh = True
op.overwrite = True
