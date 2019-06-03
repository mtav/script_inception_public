#!BPY

# To make Blender happy:
bl_info = {"name":"Cube wireframe", "category": "User"}

"""
Name: 'Cube wireframe'
Blender: 246
Group: 'Mesh'
Tooltip: 'Make a solid wireframe conecting cube nodes'
"""

__author__ = "Alejandro Sierra"
__url__ = ("www.atzibala.com/blender/cube_wire/")
__version__ = "1.0"

__bpydoc__ = """\
This script makes a solid object from selected edges. It's like Ideasman's
solid wire but simpler: cube nodes are created in all selected vertex, then 
connected by extruding the corresponging faces.
"""

# --------------------------------------------------------------------------
# Copyright (C) 2008 Alejandro Sierra (AKA naturalpainter or atzibala)
# --------------------------------------------------------------------------
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
# --------------------------------------------------------------------------


from Blender import Scene, Mesh, Window, sys, Draw
from Blender.Mathutils import *
import BPyMessages
import bpy


def create_cube(me, v, d):
	x = v.co.x
	y = v.co.y
	z = v.co.z
	coords=[ [x-d,y-d,z-d], [x+d,y-d,z-d], [x+d,y+d,z-d], [x-d,y+d,z-d],
		 [x-d,y-d,z+d], [x+d,y-d,z+d], [x+d,y+d,z+d], [x-d,y+d,z+d] ]
	me.verts.extend(coords)


def find_intersected_face(v, face_used=-1):
	normals=[ [0,0,1], [0,0,-1], [0,1,0], [0,-1,0], [-1,0,0], [1,0,0] ]
	
	dotmax = 0
	index = 0
	vn = v.normalize()
	for i in range(6):
		n = normals[i]
		a = Vector(n[0], n[1], n[2])
		d = -a*vn
		if d > dotmax and face_used!=i:
			dotmax=d
			index = i

	return index, dotmax


def fill_cube_face(me, index, f):
	faces= [ [3,2,1,0], [4,5,6,7], [0,1,5,4],
		 [7,6,2,3], [1,2,6,5], [4,7,3,0] ]

	me.faces.extend([ index+faces[f][0], 
			  index+faces[f][1],
			  index+faces[f][2],
			  index+faces[f][3]])

def skin_edges(me, i1, i2, f1, f2):
	faces= [ [3,2,1,0], [4,5,6,7], [0,1,5,4],
		 [7,6,2,3], [1,2,6,5], [4,7,3,0] ]

	me.faces.extend([ i1+faces[f1][0], 
			  i2+faces[f2][3],
			  i2+faces[f2][2],
			  i1+faces[f1][1]])

	me.faces.extend([ i1+faces[f1][1], 
			  i2+faces[f2][2],
			  i2+faces[f2][1],
			  i1+faces[f1][2]])

	me.faces.extend([ i1+faces[f1][2], 
			  i2+faces[f2][1],
			  i2+faces[f2][0],
			  i1+faces[f1][3]])

	me.faces.extend([ i1+faces[f1][3], 
			  i2+faces[f2][0],
			  i2+faces[f2][3],
			  i1+faces[f1][0]])


def create_wired_mesh(me, thick):
	node = {}

	# Create node list
	for e in me.edges:
		if e.sel:
			i0 = e.key[0]
			i1 = e.key[1]
			if not node.has_key(i0):
				node[i0] = []
			if not node.has_key(i1):
				node[i1] = []
			f1, d = find_intersected_face(me.verts[i1].co-me.verts[i0].co)
	
			if (f1 % 2 == 0):
				f2 = f1 + 1
			else:
				f2 = f1 - 1

			# adjust faces in case they are repeated
			for i in range(len(node[i0])):
				if node[i0][i][1] == f1:
					d2 = node[i0][i][3]
					if d < d2:						
						f1, d = find_intersected_face(me.verts[i1].co-me.verts[i0].co, f1)
					else:
						i2 = node[i0][i][0]
						f3, d3= find_intersected_face(me.verts[i2].co-me.verts[i0].co, f1)
						node[i0][i][2] = f3
						node[i0][i][3] = d3

			for i in range(len(node[i1])):
				if node[i1][i][1] == f2:
					d2 = node[i1][i][3]
					if d < d2:						
						f2, d = find_intersected_face(me.verts[i0].co-me.verts[i1].co, f2)
					else:
						i2 = node[i1][i][0]
						f3, d3= find_intersected_face(me.verts[i2].co-me.verts[i1].co, f2)
						node[i1][i][2] = f3
						node[i1][i][3] = d3
				
			node[i0].append([i1, f1, f2, d])
			node[i1].append([i0, f2, f1, d])	

	me2 = bpy.data.meshes.new(me.name)

	# Create the geometry
	n_idx = {}   
	for k in node:
		v = me.verts[k]
		index = len(me2.verts)
		# We need to associate each node with the new geometry
		n_idx[k] = index   
		# Geometry for the nodes, each one a cube
		create_cube(me2, v, thick)
		
		
	# Skin using the new geometry	
	for k in node:
		# Compute the face list
		f = [-1,-1,-1,-1,-1,-1] 
		n = node[k]
		
		for i in range(len(n)):
			f1 = n[i][1]
			f[f1] = i


		# Skin the nodes				
		for i in range(6):
			if f[i] == -1:
				fill_cube_face(me2, n_idx[k], i)	
			else:
				k2 = n[f[i]][0]
				f1 = n[f[i]][1]
				f2 = n[f[i]][2]
				skin_edges(me2, n_idx[k], n_idx[k2], f1, f2)

	print 'vert count', len(me2.verts)
        print 'edge count', len(me2.edges)
        print 'face count', len(me2.faces)

	scn = bpy.data.scenes.active
	ob = scn.objects.new(me2, me2.name)



def main():
	THICK = Draw.Create(0.02)

	if not Draw.PupBlock('Cube wireframe', [\
        ('Thick:', THICK, 0.0001, 10, 'Thickness of the skinned edges'),\

        ]):
                return

	# Gets the current scene, there can be many scenes in 1 blend file.
	sce = bpy.data.scenes.active
	
	# Get the active object, there can only ever be 1
	# and the active object is always the editmode object.
	ob_act = sce.objects.active
	
	if not ob_act or ob_act.type != 'Mesh':
		BPyMessages.Error_NoMeshActive()
		return 
	
	
	# Saves the editmode state and go's out of 
	# editmode if its enabled, we cant make
	# changes to the mesh data while in editmode.
	is_editmode = Window.EditMode()
	if is_editmode: Window.EditMode(0)
	
	Window.WaitCursor(1)
	me = ob_act.getData(mesh=1) # old NMesh api is default
	t = sys.time()
	
	# Run the mesh editing function
	create_wired_mesh(me, THICK.val/2.0)

	ob_act.select(False)
	
	# Restore editmode if it was enabled
	if is_editmode: Window.EditMode(1)

	# Timing the script is a good way to be aware on any speed hits when scripting
	print 'My Script finished in %.2f seconds' % (sys.time()-t)
	Window.WaitCursor(0)
	
	
# This lets you import the script without running it
if __name__ == '__main__':
	main()
