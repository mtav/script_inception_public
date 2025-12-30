import FreeCAD, Mesh
#import Mesh
#mesh = Mesh.Mesh()

############## Create a square with 2 triangles.
triangles = [
		# triangle 1
		[-0.5000, -0.5000, 0.0000], [0.5000, 0.5000, 0.0000], [-0.5000, 0.5000, 0.0000],
		#triangle 2
		[-0.5000, -0.5000, 0.0000], [0.5000, -0.5000, 0.0000], [0.5000, 0.5000, 0.0000],
	]

meshObject = Mesh.Mesh(triangles)
Mesh.show(meshObject)

############## Create a torus.
m = Mesh.createTorus(8.0, 2.0, 50)
Mesh.show(m)

############## Create cylinder A.
cylA = Mesh.createCylinder(2.0, 10.0, True, 1.0, 36)
Mesh.show(cylA)

############## Create cylinder B.
cylB = Mesh.createCylinder(1.0, 12.0, True, 1.0, 36)
cylB.Placement.Base = (FreeCAD.Vector(-1, 0, 0)) # move cylB to avoid co-planar faces
Mesh.show(cylB)

############## Create cylinder B - cylinder A.
pipe = cylA
pipe = pipe.difference(cylB)
pipe.flipNormals() # somehow required

doc = FreeCAD.ActiveDocument
obj = doc.addObject("Mesh::Feature", "Pipe")
obj.Mesh = pipe
doc.recompute()

############## Create a cube.
cube = Mesh.createBox(1,2,3)
Mesh.show(cube)

# count segments
print(cube.countSegments( ))

# 
vmin = 0
vmax = 0
dir = 0

A = 0

print(len(cube.Facets))

for f in cube.Facets:
	if all([vmin <= v[dir] <= vmax for v in f.Points]):
		A+=f.Area

print(f'A = {A}')
