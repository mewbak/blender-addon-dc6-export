# Blender Add-on Template
# Contributor(s): Aaron Powell (aaron@aaronpowell.me)
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTIBILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU
# General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.

import bpy
from bpy.types import(	Panel,
			Operator
			)

def register():
    bpy.utils.register_class(RenderFrameToDC6)
    bpy.utils.register_class(RenderAnimationToDC6)

def unregister():
    bpy.utils.unregister_class(RenderFrameToDC6)
    bpy.utils.unregister_class(RenderAnimationToDC6)

# ------------------------------------------------------------------------
#    Operators
# ------------------------------------------------------------------------

from . import handlers
pre_render_animation 	= handlers.pre_render_animation
pre_render_frame 	= handlers.pre_render_frame
post_render_animation 	= handlers.post_render_animation
post_render_frame 	= handlers.post_render_frame

class RenderAnimationToDC6(Operator):
    bl_label = "Render animation to DC6"
    bl_idname = "dc6_plugin.render_animation"

    def execute(self, context):
        scene = context.scene
        plugin = scene.DC6Plugin
        
        # bind the frame handlers
        bpy.app.handlers.render_init.append(pre_render_animation)
        bpy.app.handlers.render_complete.append(post_render_animation)
        
        # do the render
        bpy.ops.render.render('INVOKE_DEFAULT', animation=True)
        
        # then do the conversion
#        print("bool state:", mytool.my_bool)
#        print("int value:", mytool.my_int)
#        print("float value:", mytool.my_float)
#        print("string value:", mytool.my_string)
#        print("enum state:", mytool.my_enum)

        return {'FINISHED'}
    
class RenderFrameToDC6(Operator):
    bl_label = "Render frame to DC6"
    bl_idname = "dc6_plugin.render_frame"

    def execute(self, context):
        scene = context.scene
        plugin = scene.DC6Plugin

        # bind the frame handlers
        bpy.app.handlers.render_init.append(pre_render_frame)
        bpy.app.handlers.render_complete.append(post_render_frame)
        
        # do the render
        bpy.ops.render.render(animation=False, write_still=True)
        
        # then do the conversion
#        print("bool state:", mytool.my_bool)
#        print("int value:", mytool.my_int)
#        print("float value:", mytool.my_float)
#        print("string value:", mytool.my_string)
#        print("enum state:", mytool.my_enum)

        return {'FINISHED'}

