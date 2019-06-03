#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# To make Blender happy:
bl_info = {"name":"add_mesh_pipe_248", "category": "User"}

"""
Name: 'Pipe_247'
Blender: 244
Group: 'AddMesh'
"""
__author__ = ["Luis Sergio S. Moura Jr."]
__version__ = '0.3'
__url__ = ["liquidblue.com.br"]
__bpydoc__ = """

Usage:

Pipe Mesh

This script lets the user create a new primitive. A pipe. Receives as input the 
inner radius, outer radius and the number of divisions. It consists in a hollow cone.

This script was inspired in opendimension.org's tutorial

0.3 - 2007-07-25 by Luis Sergio<br />
- removed leftover debug instructions
- added radial divisions

0.2 - 2007-07-25 by Luis Sergio<br />
- added height divisions as requested on blenderartists forum thread http://blenderartists.org/forum/showthread.php?t=101571
- normals are corrected

0.1 - 2007-07-24 by Luis Sergio<br />
- initial version

"""

# *** BEGIN LICENSE BLOCK ***
# Creative Commons 3.0 by-sa
#
# Full license: http://creativecommons.org/licenses/by-sa/3.0/
# Legal code: http://creativecommons.org/licenses/by-sa/3.0/legalcode
#
# You are free:
# * to Share  to copy, distribute and transmit the work
# * to Remix  to adapt the work
#
# Under the following conditions:
# * Attribution. You must attribute the work in the manner specified by the author or licensor (but not in any way that suggests that they endorse you or your use of the work).
# * Share Alike. If you alter, transform, or build upon this work, you may distribute the resulting work only under the same, similar or a compatible license.
#
# * For any reuse or distribution, you must make clear to others the license terms of this work. The best way to do this is with a link to this web page.
# * Any of the above conditions can be waived if you get permission from the copyright holder.
# * Nothing in this license impairs or restricts the author's moral rights.
# *** END LICENSE BLOCK ***

# Importing modules
import BPyAddMesh
import Blender
import math


# The actual function that generates the vectors and faces for the pipe
# PARAMETERS:
#	V_DIVISIONS	Vertical divisions
#	H_DIVISIONS	Height divisions
#	R_DIVISIONS	Radial divisions
#	INNER_RADIUS	Inner radius
#	OUTER_RADIUS	Outer radius
#	HEIGHT		Pipe height
def add_pipe(V_DIVISIONS, H_DIVISIONS, R_DIVISIONS, INNER_RADIUS, OUTER_RADIUS, HEIGHT):
	verts = []
	faces = []
	# Number of vertices in each division
	divvcount = (H_DIVISIONS + 1) * 2 + (R_DIVISIONS - 1) * 2
	# Total number of vertices
	vcount = divvcount * V_DIVISIONS

	# Create Vertices
	for hdiv in range(V_DIVISIONS):
		degree = hdiv * 2 * math.pi / V_DIVISIONS
		mulx = math.sin(degree)
		muly = math.cos(degree)
		# step between height divisions
		step = HEIGHT / H_DIVISIONS

		# step between section divisions
		sstep = (OUTER_RADIUS - INNER_RADIUS) / R_DIVISIONS

		for vdiv in range(H_DIVISIONS + 1):
			verts.append([mulx * OUTER_RADIUS, muly * OUTER_RADIUS, -HEIGHT/2 + step * vdiv]);
			verts.append([mulx * INNER_RADIUS, muly * INNER_RADIUS, -HEIGHT/2 + step * vdiv]);

		# section division vertices
		for sdiv in range(R_DIVISIONS):
			if (sdiv > 0):
				verts.append([mulx * (OUTER_RADIUS - sstep * sdiv), muly * (OUTER_RADIUS - sstep * sdiv), -HEIGHT/2]);
				verts.append([mulx * (OUTER_RADIUS - sstep * sdiv), muly * (OUTER_RADIUS - sstep * sdiv), HEIGHT/2]);
	
	# Create Faces
	for hdiv in range(V_DIVISIONS):
		start = hdiv * divvcount
		nextstart = start + divvcount
		if (nextstart >= vcount):
			nextstart = 0

		for vdiv in range(H_DIVISIONS * 2):
			# We have to draw the sequence differently because of our normals. They must point outside of the pipe.
			if ((vdiv % 2) == 0):
				# OUTER FACES
				faces.append([start + vdiv, start + vdiv + 2, nextstart + vdiv + 2, nextstart + vdiv]);
			else:
				# INNER FACES
				faces.append([start + vdiv + 2, start + vdiv, nextstart + vdiv, nextstart + vdiv + 2]);


		if (R_DIVISIONS == 1):
			# Bottom faces
			faces.append([start+1 , start, nextstart, nextstart+1])
			# Top faces
			faces.append([start + divvcount - 2, start + divvcount - 1, nextstart + divvcount - 1, nextstart + divvcount - 2]);
		else:
			# number of vertices on the sides (excluding the ones created between the inner radius and outer radius)
			sidevcount = (H_DIVISIONS + 1) * 2
			for inf in range(R_DIVISIONS):
				if (inf == 0):
					# First faces
					faces.append([start + sidevcount, start, nextstart, nextstart + sidevcount])
					faces.append([start + sidevcount - 2, start + sidevcount + 1, nextstart + sidevcount + 1, nextstart + sidevcount - 2])
				else:
					if (inf == (R_DIVISIONS - 1)):
						# Last faces
						faces.append([start + 1, start + divvcount - 2, nextstart + divvcount - 2, nextstart + 1])
						faces.append([start + divvcount - 1, start + sidevcount - 1, nextstart + sidevcount - 1, nextstart + divvcount - 1])
					else:
						xx = (inf - 1) * 2
						# Middle faces
						faces.append([start + sidevcount + xx + 2, start + sidevcount + xx, nextstart + sidevcount + xx, nextstart + sidevcount + xx + 2])
						faces.append([start + sidevcount + xx + 1, start + sidevcount + xx + 3, nextstart + sidevcount + xx + 3, nextstart + sidevcount + xx + 1])
	
	return verts,faces

# main function (window handle and input variables)
def main():
	pipeInnerInput = Blender.Draw.Create(48)
	pipeOuterInput = Blender.Draw.Create(50)
	pipeDivInput = Blender.Draw.Create(64)
	pipeHDivInput = Blender.Draw.Create(1)
	pipeRDivInput = Blender.Draw.Create(1)
	pipeHeightInput = Blender.Draw.Create(1.0)
	
	block = []
	block.append(("Inner radius:", pipeInnerInput, 0.01, 100, "the inner radius"))
	block.append(("Outer radius:", pipeOuterInput, 0.01, 100, "the outer radius"))
	block.append(("Divisions:", pipeDivInput, 4, 100, "number of divisions"))
	block.append(("Height:", pipeHeightInput, 1.00, 100, "the height of the pipe"))
	block.append(("Height divisions:", pipeHDivInput, 1, 100, "number of height divisions"))
	block.append(("Radial divisions:", pipeRDivInput, 1, 100, "number of radial divisions"))
	
	if not Blender.Draw.PupBlock("Lay pipe", block):
		return
	
#	Generates the mesh
	verts, faces = add_pipe(pipeDivInput.val, pipeHDivInput.val, pipeRDivInput.val, pipeInnerInput.val, pipeOuterInput.val, pipeHeightInput.val)

#	Adds the mesh to the scene
	BPyAddMesh.add_mesh_simple('Pipe', verts, [], faces)

if __name__ == '__main__':
  # call our main function	
  main()
