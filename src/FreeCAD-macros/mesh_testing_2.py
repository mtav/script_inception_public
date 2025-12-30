import FreeCAD, Mesh
#import Mesh
#mesh = Mesh.Mesh()

############## Create a cube.
cube = Mesh.createBox(1,2,3)
Mesh.show(cube)

# count segments
print(cube.countSegments( ))

# 
vmin = -1.5
vmax = vmin
for dir in range(3):
#dir = 0

	A = 0
	
	#print(len(cube.Facets))
	
	for f in cube.Facets:
		#print(f)
		if all([vmin <= v[dir] <= vmax for v in f.Points]):
			A+=f.Area
	
	print(f'dir={dir}, A = {A}')
