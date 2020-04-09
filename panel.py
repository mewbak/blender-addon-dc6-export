import bpy
from bpy.types import Panel

def register():
    bpy.utils.register_class(DC6Panel)

def unregister():
    bpy.utils.unregister_class(DC6Panel)

# ------------------------------------------------------------------------
#    Panel in Object Mode
# ------------------------------------------------------------------------

class DC6Panel(Panel):
    bl_label = "DC6 Add-on"
    bl_idname = "OBJECT_PT_DC6Panel"
    bl_space_type = "VIEW_3D"   
    bl_region_type = "UI"
    bl_category = "Tools"

    @classmethod
    def poll(self,context):
        return context.object is not None

    def draw(self, context):
        layout = self.layout
        scene = context.scene
        DC6Plugin = scene.DC6Plugin

        layout.prop(DC6Plugin, "rig_enable")
        row = layout.row()
        row.prop(DC6Plugin, "rig_directions")
        #layout.prop(DC6Plugin, "rig_radius")
        #layout.prop(DC6Plugin, "rig_height")
        #layout.prop(DC6Plugin, "camera_focal_length")
        #layout.prop(DC6Plugin, "camera_target_position")
        row.prop(DC6Plugin, "render_width")
        row.prop(DC6Plugin, "render_height")
        layout.prop(DC6Plugin, "render_directory")
        layout.prop(DC6Plugin, "dc6_directory")
        layout.prop(DC6Plugin, "dc6_filename")
        layout.prop(DC6Plugin, "render_palette", text="Target palette")
        row = layout.row()
        row.operator("dc6_plugin.render_animation", text='Export animation to DC6')
        row.operator("dc6_plugin.render_frame", text='Export frame to DC6')
        layout.separator()

