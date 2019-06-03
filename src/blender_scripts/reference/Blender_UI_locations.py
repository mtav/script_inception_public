import bpy


#bl_region_type
#The region where the panel is going to be used in

#Type :	enum in [‘WINDOW’, ‘HEADER’, ‘CHANNELS’, ‘TEMPORARY’, ‘UI’, ‘TOOLS’, ‘TOOL_PROPS’, ‘PREVIEW’], default ‘WINDOW’
#bl_space_type
#The space where the panel is going to be used in

#Type :	enum in [‘EMPTY’, ‘VIEW_3D’, ‘TIMELINE’, ‘GRAPH_EDITOR’, ‘DOPESHEET_EDITOR’, ‘NLA_EDITOR’, ‘IMAGE_EDITOR’, ‘SEQUENCE_EDITOR’, ‘CLIP_EDITOR’, ‘TEXT_EDITOR’, ‘NODE_EDITOR’, 
#‘LOGIC_EDITOR’, ‘PROPERTIES’, ‘OUTLINER’, ‘USER_PREFERENCES’, ‘INFO’, ‘FILE_BROWSER’, ‘CONSOLE’], default ‘EMPTY’

class HelloWorldPanel(bpy.types.Panel):
    """Creates a Panel in the Object properties window"""
    bl_idname = "OBJECT_PT_hello"

    bl_label = "Panel location"
    
    #bl_context = "object"

    #bl_region_type = 'WINDOW'
    #bl_region_type = 'HEADER'
    #bl_region_type = 'CHANNELS'
    #bl_region_type = 'TEMPORARY'
    bl_region_type = 'UI' # For bl_space_type = 'VIEW_3D': in view->properties
    #bl_region_type = 'TOOLS' # For bl_space_type = 'VIEW_3D': in view->tool shelf top part
    #bl_region_type = 'TOOL_PROPS' # For bl_space_type = 'VIEW_3D': in view->tool shelf bottom part
    #bl_region_type = 'PREVIEW'

    bl_space_type = 'VIEW_3D'
    #bl_space_type = 'PROPERTIES'

    #bl_label = "Hello World Panel"
    #bl_idname = "OBJECT_PT_hello"
    #bl_space_type = 'PROPERTIES'
    #bl_region_type = 'WINDOW'
    #bl_context = "object"


    def draw(self, context):
        layout = self.layout
        row = layout.row()
        row.label(text= 'bl_context = ' + self.bl_context)
        row = layout.row()
        row.label(text= 'bl_region_type = ' + self.bl_region_type)
        row = layout.row()
        row.label(text= 'bl_space_type = ' + self.bl_space_type)

        #obj = context.object

        #row = layout.row()
        #row.label(text="Hello world!", icon='WORLD_DATA')

        #row = layout.row()
        #row.label(text="Active object is: " + obj.name)
        #row = layout.row()
        #row.prop(obj, "name")

        #row = layout.row()
        #row.operator("mesh.primitive_cube_add")

def register():
    bpy.utils.register_class(HelloWorldPanel)


def unregister():
    bpy.utils.unregister_class(HelloWorldPanel)

if __name__ == "__main__":
  print('=== Running main ===')
  register()
  print('=== main done. ===')
