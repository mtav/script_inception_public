# To make Blender happy:
bl_info = {"name":"mesh_adding.ref.py", "category": "User"}

mesh_data = bpy.data.meshes.new('name')
mesh_data.from_pydata([(0,0,0),(1,0,0),(1,1,0),(0,1,0)], [(0,1),(1,2),(2,3),(3,0)], [(0,1,2,3)])
new_object = bpy.data.objects.new('name', mesh_data)
scene = bpy.context.scene
scene.objects.link(new_object)

if __name__ == '__main__':
  pass
