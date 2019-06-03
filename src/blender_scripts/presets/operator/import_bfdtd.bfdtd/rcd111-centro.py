import bpy
op = bpy.context.active_operator

op.filepath = '~/rsync/WORK.rsync/Desktop/RCD-paper/20042015/RCD111-size=10x10x10-n_defect=2.40.n_crystal=1.00.n_backfill=2.40-defectPos=0.5-sphere/Ez/'
op.files.clear()
item_sub_1 = op.files.add()
item_sub_1.name = ''
item_sub_1.name = ''
op.directory = '~/rsync/WORK.rsync/Desktop/RCD-paper/20042015/RCD111-size=10x10x10-n_defect=2.40.n_crystal=1.00.n_backfill=2.40-defectPos=0.5-sphere/Ez/'
op.use_placeholder = False
op.placeholder_type = 'first_imported_object'
op.restrict_import_volume = True
op.xmin = 5.0
op.xmax = 7.0
op.ymin = 5.0
op.ymax = 7.0
op.zmin = 5.0
op.zmax = 7.0
op.import_cylinders = True
op.import_blocks = True
op.numbered_prefixes = True
op.use_Nmax_objects = False
op.Nmax_objects = 500
