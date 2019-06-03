#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# To make Blender happy:
bl_info = {"name":"Cells v1.2_248", "category": "User"}

"""
Name: 'Cells v1.2_248'
Blender: 243
Group: 'Add'
Tooltip: 'Voxelize mesh-objects'
"""

__author__ = ["Michael Schardt (M.Schardt@web.de)"]
__url__ = ()
__version__ = "1.2.0 - 03.07.2007"

__bpydoc__ = """\
Select 2 objects: the mesh object to be voxelized and a (small) object used as cell.\n\
Order of selection is not important - you'll be asked to specify the correct object.\n\
Caution: Script may take some time to execute! Please be patient!\n\
After completion a new object is created, parented to the cell-object and selected.\n\
'DupliVerts' is automatically activated for the new object.\n\
\n\
Known issues:\n\
	Mesh object to be voxelized must be triangulated.\n\
	For solid voxel model, mesh object must be closed and manifold (each edge shared by exactly 2 faces).\n\
"""

# Id: Cells.py, v1.2 - 03.07.2007
#
# -------------------------------------------------------------------------- 
# Cells v1.2 (C) Michael Schardt
# -------------------------------------------------------------------------- 
#
#
# ***** BEGIN GPL LICENSE BLOCK ***** 
# 
# This program is free software; you can redistribute it and/or 
# modify it under the terms of the GNU General Public License 
# as published by the Free Software Foundation; either version 2 
# of the License, or (at your option) any later version. 
# 
# This program is distributed in the hope that it will be useful, 
# but WITHOUT ANY WARRANTY; without even the implied warranty of 
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the 
# GNU General Public License for more details. 
# 
# You should have received a copy of the GNU General Public License 
# along with this program; if not, write to the Free Software Foundation, 
# Inc., 59 Temple Place - Suite 330, Boston, MA  02111-1307, USA. 
# 
# ***** END GPL LICENCE BLOCK ***** 
#
# -------------------------------------------------------------------------- 

import Blender; from Blender import *

import math

try:
	import psyco; psyco.full()
except:
	pass

# shortcuts
###########

fabs      = math.fabs
Vector    = Mathutils.Vector
Matrix    = Mathutils.Matrix
CrossVecs = Mathutils.CrossVecs

TriangleNormal = Mathutils.TriangleNormal

#####################################################################

def InsideZProjection(point, faces):

	# calculate boundary:
	
	boundary_edges = set()

	for face in faces:
	
		for edge in ((face.v[0], face.v[1]),
						 (face.v[1], face.v[2]),
						 (face.v[2], face.v[0])):

			if (edge[0], edge[1]) in boundary_edges:
				boundary_edges.remove((edge[0], edge[1]))
				continue

			if (edge[1], edge[0]) in boundary_edges:
				boundary_edges.remove((edge[1], edge[0]))
				continue

			boundary_edges.add(edge)

	# point in 2D-polygon test:
	
	inside = False
	
	for edge in boundary_edges:
		
		p0 = edge[0].co
		p1 = edge[1].co
				
		if (p0[1] <= point[1] < p1[1]):
			if TriangleNormal(point, p0, p1)[2] < 0.0: inside = not inside
			continue
			
		if (p1[1] <= point[1] < p0[1]):
			if TriangleNormal(point, p0, p1)[2] > 0.0: inside = not inside
			continue
			
	return inside
	
#####################################################################

def Cells(object, cell, solid = False):
	
	t0 = sys.time()
	
	Window.WaitCursor(1)

	es = [Vector(1.0, 0.0, 0.0),
			Vector(0.0, 1.0, 0.0),
			Vector(0.0, 0.0, 1.0)]

	# transform object/mesh (to get cell-alignment right)
	######################################################
	
	cm  = Matrix(cell.getMatrix())
	cmi = Matrix(cell.getInverseMatrix())

	om  = Matrix(object.getMatrix())
	omi = Matrix(object.getInverseMatrix())
	
	tm  = om * cmi
	tmi = cm * omi
	
	mesh = object.getData(0, 1)
		
	# transform mesh to align with cell

	mesh.transform(tm, 1)
	
	# calculate cell dimensions
	###########################
		
	cell_gbb_min = cell.getBoundBox()[0]
	cell_lbb_min = Vector(cell_gbb_min[0], cell_gbb_min[1], cell_gbb_min[2], 1.0) * cmi
	cell_gbb_max = cell.getBoundBox()[6]
	cell_lbb_max = Vector(cell_gbb_max[0], cell_gbb_max[1], cell_gbb_max[2], 1.0) * cmi

	cell_dimensions = cell_lbb_max - cell_lbb_min
	cell_dimension_x = cell_dimensions[0]
	cell_dimension_y = cell_dimensions[1]
	cell_dimension_z = cell_dimensions[2]
	
	# bin vertices
	##############
	# everything in object's local coordinates (aligned with cell)
	
	v_cells = {}		
		
	for vert in mesh.verts:
		coords = vert.co
		v_cells[vert] = (int(round(coords[0] / cell_dimension_x)),
							  int(round(coords[1] / cell_dimension_y)),
							  int(round(coords[2] / cell_dimension_z)))

	# bin faces
	###########
	# everything in object's local coordinates (aligned with cell)
	
	f_cells = {}
		
	for face in mesh.faces:
		
		verts = face.v

		fidxs = [v_cells[vert][0] for vert in verts]; fidxs.sort()		
		min_fidx = fidxs[0]; max_fidx = fidxs[-1]		
		fidys = [v_cells[vert][1] for vert in verts]; fidys.sort()
		min_fidy = fidys[0]; max_fidy = fidys[-1]
		fidzs = [v_cells[vert][2] for vert in verts]; fidzs.sort()
		min_fidz = fidzs[0]; max_fidz = fidzs[-1]
				
		# fast path for special cases (especially small faces spanning a single cell only)

		category = 0
		if (max_fidx > min_fidx): category |= 1
		if (max_fidy > min_fidy): category |= 2
		if (max_fidz > min_fidz): category |= 4
		
		if category == 0: # single cell
			f_cells.setdefault((min_fidx, min_fidy, min_fidz), set()).add(face)
			continue
		
		if category == 1: # multiple cells in x-, single cell in y- and z-direction
			for fidx in range(min_fidx, max_fidx + 1):
				f_cells.setdefault((fidx, min_fidy, min_fidz), set()).add(face)
			continue
		
		if category == 2: # multiple cells in y-, single cell in x- and z-direction
			for fidy in range(min_fidy, max_fidy + 1):
				f_cells.setdefault((min_fidx, fidy, min_fidz), set()).add(face)
			continue

		if category == 4: # multiple cells in z-, single cell in x- and y-direction
			for fidz in range(min_fidz, max_fidz + 1):
				f_cells.setdefault((min_fidx, min_fidy, fidz), set()).add(face)
			continue
						
		# long path (face spans multiple cells in more than one direction)

		a0 = face.no

		r0 =  0.5 * (fabs(a0[0]) * cell_dimension_x +
						 fabs(a0[1]) * cell_dimension_y +
						 fabs(a0[2]) * cell_dimension_z)
											
		cc = Vector(0.0, 0.0, 0.0)		
		for fidx in range(min_fidx, max_fidx + 1):
			cc[0] = fidx * cell_dimensions[0]
			for fidy in range(min_fidy, max_fidy + 1):
				cc[1] = fidy * cell_dimensions[1]
				for fidz in range(min_fidz, max_fidz + 1):
					cc[2] = fidz * cell_dimensions[2]
						
					if not solid and (fidx, fidy, fidz) in f_cells: continue # cell already populated -> no further processing needed for hollow model
						
					vs = [vert.co - cc for vert in verts]
															
					if not (-r0 <= a0 * vs[0] <= r0): continue # cell not intersecting face hyperplane

					# check overlap of cell with face (separating axis theorem)
												
					fs = [vs[1] - vs[0],
							vs[2] - vs[1],
							vs[0] - vs[2]]
												
					overlap = True

					for f in fs:
						if not overlap: break

						for e in es:
							if not overlap: break
							
							a = CrossVecs(e, f)
							
							r = 0.5 * (fabs(a[0]) * cell_dimension_x +
										  fabs(a[1]) * cell_dimension_y +
										  fabs(a[2]) * cell_dimension_z)						

							ds = [a * v for v in vs]; ds.sort()
															
							if (ds[0] > r or ds[-1] < -r): overlap = False
													
					if overlap:	f_cells.setdefault((fidx, fidy, fidz), set()).add(face)
	
	# the hollow voxel representation is complete
	
	# fill
	######

	if solid:
		
		# find min, max cells in x, y, z
		
		idxs = [id[0] for id in f_cells]; idxs.sort()		
		min_idx = idxs[0]; max_idx = idxs[-1]		
		idys = [id[1] for id in f_cells]; idys.sort()
		min_idy = idys[0]; max_idy = idys[-1]
		idzs = [id[2] for id in f_cells]; idzs.sort()
		min_idz = idzs[0]; max_idz = idzs[-1]

		testpoint = Vector(0.0, 0.0, 0.0)
		
		# for x,y
		
		for idx in range(min_idx, max_idx + 1):
			testpoint[0] = idx * cell_dimension_x	
			for idy in range(min_idy, max_idy + 1):
				testpoint[1] = idy * cell_dimension_y

				odd_parity = False

				tested_faces = set()

				# walk the z pile and keep track of parity
				
				for idz in range(min_idz, max_idz + 1):
				
					fs = f_cells.get((idx, idy, idz), set()) - tested_faces
					
					# cell contains faces
					
					if fs:

						# categorize faces in this cell by normal
						
						pfaces = []
						nfaces = []
						
						for f in fs:
							fnoz = f.no[2]
							if fnoz >= 0.0: pfaces.append(f)
							if fnoz <= 0.0: nfaces.append(f)						
							tested_faces.add(f)
						
						# check if testpoint inside z projections
														
						if pfaces:																		
							if InsideZProjection(testpoint, pfaces): odd_parity = not odd_parity
								
						if nfaces:
							if InsideZProjection(testpoint, nfaces): odd_parity = not odd_parity

					# cell contains no faces (empty cell)
					
					else:
						if odd_parity:	f_cells[(idx, idy, idz)] = 1 # odd parity -> empty cell inside object
								
	# create new object
	###################
			
	mesh_new = Mesh.New("Cells("+object.name+")")
	mesh_new.verts = None
	mesh_new.verts.extend([Vector(id[0] * cell_dimension_x,
											id[1] * cell_dimension_y,
											id[2] * cell_dimension_z) for id in f_cells])

	scene = Scene.GetCurrent()
				
	object_new = scene.objects.new(mesh_new,"Cells("+object.name+")")

	object_new.layers = object.layers

	# transform objects/meshes back
	###############################

	object_new.setMatrix(om)
	mesh.transform(tmi, 1)
	mesh_new.transform(tmi, 1)

	# parent new object to cell for dupliverts
	###########################################
	
	cell.LocX = object.LocX
	cell.LocY = object.LocY
	cell.LocZ = object.LocZ
	cell.layers = object_new.layers
	scene.update()		
	object_new.makeParent([cell])
	object_new.enableDupVerts = True
	
	# select
	########
	
	object.select(0)
	cell.select(0)
	object_new.select(1)
		
	# done
	######
	
	Window.WaitCursor(0)

	t1 = sys.time()
	
	print((str(len(mesh.faces))+" faces ... "+str(len(f_cells))+" cells: "+str(round(t1-t0, 3))+" s"))

	Window.Redraw()

#####################################################################
#####################################################################

def CheckMesh(object):
	
	if object.getType() != "Mesh":
		Draw.PupMenu("object '"+object.name+"' is not a mesh-object - exit")
		return False
	
	return True

# *******************************************************************

def CheckManifold(object):
	
	mesh = object.getData(0, 1)
	
	edgeusers = {}
	
	for face in mesh.faces:
		for edgekey in face.edge_keys:
			edgeusers.setdefault(edgekey, 0)
			edgeusers[edgekey] += 1
	
	for val in list(edgeusers.values()):
		if val != 2: 
			Draw.PupMenu("object '"+object.name+"' is not manifold - exit")
			return False
	
	return True

# *******************************************************************

def CheckTriangles(object):
	
	mesh = object.getData(0, 1)
		
	for face in mesh.faces:
		
		if len(face.v) != 3:
			Draw.PupMenu("object '"+object.name+"' must be triangulated - Ctrl/t in edit mode")
			return False
	
	return True

#####################################################################
#####################################################################


if __name__ == "__main__":
	
	selection = Object.GetSelected()

	ok = True
	
	if len(selection) != 2:
		Draw.PupMenu("please select 2 objects: mesh-object to be voxelized and cell object")
		ok = False

	if ok:
		res1 = Draw.PupMenu("choose object to be voxelized%t|"+selection[0].name+"%x0|"+selection[1].name+"%x1")		
		if res1 == -1:
			ok = False;	print("\nAborted")
		
	if ok:
		ok &= CheckMesh(selection[res1])
		
	if ok:			
		ok &= CheckTriangles(selection[res1])

	if ok:			
		res2 = Draw.PupMenu("create voxel model%t|hollow (from "+selection[res1].name+" surface)%x0| solid   (from "+selection[res1].name+" volume)%x1")
		if res2 == -1:
			ok = False;	print("\nAborted")

	if ok:
		if res2 == 1:
			ok &= CheckManifold(selection[res1])	
	
	if ok:
		if res1 == 0:
			print(("\nCalculating Cells("+selection[0].name+"):\n"))
			Cells(selection[0], selection[1], res2)
		if res1 == 1:
			print(("\nCalculating Cells("+selection[1].name+"):\n"))
			Cells(selection[1], selection[0], res2)

		print("\nDone")
