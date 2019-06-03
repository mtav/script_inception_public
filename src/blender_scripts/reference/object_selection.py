# based on code from: http://blenderartists.org/forum/showthread.php?200311-Creating-a-Object-Selection-Box-in-Panel-UI-of-Blender-2-5

import bpy

bpy.types.Object.mychosenObject = bpy.props.StringProperty()
bpy.types.Object.mychosenObject1 = bpy.props.StringProperty()
bpy.types.Object.mychosenObject2 = bpy.props.StringProperty()

## class where the custom properties for the Collection will be nested
## (each entry of the collection will derive its Properties from this Class
## and can hold own values for each property)

class MyPropertyGroup(bpy.types.PropertyGroup):
    ## create Properties for the collection entries:
    mystring = bpy.props.StringProperty()
    mybool = bpy.props.BoolProperty(default = False)
    #name = bpy.props.StringProperty(name="Test Prop", default="Unknown")
    #value = bpy.props.IntProperty(name="Test Prop", default=22)
    pass

bpy.utils.register_class(MyPropertyGroup)

## create CollectionProperty and link it to the property class
bpy.types.Object.myCollection = bpy.props.CollectionProperty(type = MyPropertyGroup)
bpy.types.Object.myCollection_index = bpy.props.IntProperty(min = -1, default = -1)

## create operator to add or remove entries to/from  the Collection
class OBJECT_OT_add_remove_Collection_Items(bpy.types.Operator):
    bl_label = "Add or Remove"
    bl_idname = "collection.add_remove"
    
    addvar = bpy.props.BoolProperty(default = True)
    
    def invoke(self, context, event):
        addvar = self.addvar
        obj = context.object
        collection = obj.myCollection
        if addvar:
            # "myCollection.add()" then the default value for "name" will be "". but you can directly assign a name to it with "myCollection.add().name = "bla".
            ret = collection.add()
        else:
            index = obj.myCollection_index
            ret = collection.remove(index)
        #print('addvar = ', addvar)
        #print('ret = ', ret)
        return {'FINISHED'}
        #return(ret)

class OBJECT_PT_ObjectSelecting2(bpy.types.Panel):
    
    bl_label = "Object Selecting 2"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'TOOL_PROPS'
    #bl_context = "object"
    
    def draw(self, context):
        obj = context.object
        layout = self.layout
        
        ##show collection in Panel:
        row = layout.row()
        #row.template_list(listtype_name=obj, list_id="myCollection", dataptr=obj, propname="myCollection_index")
        #row.template_list("UIList", "", obj, "myCollection", obj,"myCollection_index")
        row.template_list("UI_UL_list", "custom_list_id", obj, "myCollection", obj,"myCollection_index")
        ##show add/remove Operator
        col = row.column(align=True)
        col.operator("collection.add_remove", icon="ZOOMIN", text="")
        col.operator("collection.add_remove", icon="ZOOMOUT", text="").addvar = False
        
        ##change name of Entry:
        if obj.myCollection and obj.myCollection_index<len(obj.myCollection):
            #print('len(obj.myCollection) = ', len(obj.myCollection))
            #print('obj.myCollection_index = ', obj.myCollection_index)
            entry = obj.myCollection[obj.myCollection_index]
            layout.prop(entry, "name")
            
            ##show self created properties of myCollection
            layout.prop(entry, "mystring")
            layout.prop(entry, "mybool")
        
        ### search prop to search in myCollection:
        layout.prop_search(obj, "mychosenObject1",  obj, "myCollection")
        layout.prop_search(obj, "mychosenObject2",  obj, "myCollection")

class OBJECT_PT_ObjectSelecting(bpy.types.Panel):
    
    bl_label = "Object Selecting"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'TOOL_PROPS'
    #bl_context = "object"
    
    def draw(self, context):
        obj = context.object
        layout = self.layout
        layout.label(text=" Simple Row:")
        layout.prop_search(obj, "mychosenObject1",  context.scene, "objects")
        layout.prop_search(obj, "mychosenObject2",  context.scene, "objects")


class LayoutDemoPanel(bpy.types.Panel):
    """Creates a Panel in the scene context of the properties editor"""
    bl_label = "Layout Demo"
    bl_idname = "SCENE_PT_layout"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'TOOL_PROPS'
    #bl_context = "scene"

    def draw(self, context):
        layout = self.layout

        scene = context.scene

        # Create a simple row.
        layout.label(text=" Simple Row:")

        row = layout.row()
        row.prop(scene, "frame_start")
        row.prop(scene, "frame_end")

        # Create an row where the buttons are aligned to each other.
        layout.label(text=" Aligned Row:")

        row = layout.row(align=True)
        row.prop(scene, "frame_start")
        row.prop(scene, "frame_end")

        # Create two columns, by using a split layout.
        split = layout.split()

        # First column
        col = split.column()
        col.label(text="Column One:")
        col.prop(scene, "frame_end")
        col.prop(scene, "frame_start")

        # Second column, aligned
        col = split.column(align=True)
        col.label(text="Column Two:")
        col.prop(scene, "frame_start")
        col.prop(scene, "frame_end")
        
        # Big render button
        layout.label(text="Big Button:")
        row = layout.row()
        row.scale_y = 3.0
        row.operator("render.render")
        
        # Different sizes in a row
        layout.label(text="Different button sizes:")
        row = layout.row(align=True)
        row.operator("render.render")
        
        sub = row.row()
        sub.scale_x = 2.0
        sub.operator("render.render")
        
        row.operator("render.render")


def register():
    bpy.utils.register_class(LayoutDemoPanel)
    bpy.utils.register_class(OBJECT_PT_ObjectSelecting)
    bpy.utils.register_class(OBJECT_OT_add_remove_Collection_Items)
    bpy.utils.register_class(OBJECT_PT_ObjectSelecting2)

def unregister():
    bpy.utils.unregister_class(LayoutDemoPanel)
    bpy.utils.unregister_class(OBJECT_PT_ObjectSelecting)
    bpy.utils.unregister_class(OBJECT_OT_add_remove_Collection_Items)
    bpy.utils.unregister_class(OBJECT_PT_ObjectSelecting2)

if __name__ == "__main__":
    print('=== start ===')
    register()
    print('=== end ===')
