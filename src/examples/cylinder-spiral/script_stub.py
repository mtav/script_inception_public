# This stub runs a python script relative to the currently open
# blend file, useful when editing scripts externally.

import bpy
import os

# Use your own script name here:
#filename = "cylinder-example.py"
filename = "cylinder-spiral.py"

filepath = os.path.join(os.path.dirname(bpy.data.filepath), filename)
global_namespace = {"__file__": filepath, "__name__": "__main__"}
with open(filepath, 'rb') as file:
    exec(compile(file.read(), filepath, 'exec'), global_namespace)

from blender_scripts.modules.bfdtd_import import addObjectsByDuplication, BristolFDTDimporter
importer = BristolFDTDimporter()
importer.importBristolFDTD('foo.geo')

from blender_scripts.modules.GWL_import import importGWL
importGWL('foo.gwl')
