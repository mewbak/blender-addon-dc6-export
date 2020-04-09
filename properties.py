import bpy
from bpy.types import Scene
from bpy.utils import ( register_class,
                        unregister_class
                        )

from bpy.props import (StringProperty,
                       BoolProperty,
                       IntProperty,
                       FloatProperty,
                       FloatVectorProperty,
                       EnumProperty,
                       PointerProperty,
                       )

from bpy.types import (Panel,
                       Menu,
                       Operator,
                       PropertyGroup,
                       )

def register():
    register_class(CameraRigProperties)
    Scene.DC6Plugin = PointerProperty(type=CameraRigProperties)

def unregister():
    unregister_class(CameraRigProperties)
    del Scene.DC6Plugin

from . import constants
defaults = constants.defaults

from . import camera_rig

class CameraRigProperties(PropertyGroup):

    rig_enable: BoolProperty(
        name="Enable Camera Rig",
        description="Sets up the camera rig in the scene",
        default = defaults['rig_enable'],
        update = camera_rig.update_rig
        )

    rig_directions: IntProperty(
        name = "Directions",
        description="The number of directions in the DC6",
        default = defaults['rig_directions'],
        min = 1,
        max = 64,
        update = camera_rig.update_rig
        )

    rig_radius: IntProperty(
        name = "Radius",
        description="The radius of the circle the cameras are positioned upon",
        default = defaults['rig_radius'],
        min = 1,
        max = 64,
        update = camera_rig.update_rig
        )

    rig_height: FloatProperty(
        name = "Rig Height",
        description="The z-position of the camera rig",
        default = defaults['rig_height'],
        min = 1.0,
        max = 64.0,
        update = camera_rig.update_rig
        )
        
    camera_focal_length: IntProperty(
        name = "Focal Length",
        description="The focal length of the cameras",
        default = defaults['camera_focal_length'],
        min = 1,
        max = 1000,
        update = camera_rig.update_rig
        )

#    camera_target_position: FloatVectorProperty(
#        name = "Camera target position",
#        description="Where the cameras are pointing",
#        default=(0.0, 0.0, 1.0), 
#        min= 0.0, # float
#        max = 100
#    ) 
        
    render_width: IntProperty(
        name = "Outut Width",
        description="The width of the output image",
        default = defaults['render_width'],
        min = 1,
        max = 256,
        update = camera_rig.update_rig
        )
        
    render_height: IntProperty(
        name = "Output Height",
        description="The height of the output image",
        default = defaults['render_height'],
        min = 1,
        max = 256,
        update = camera_rig.update_rig
        )

    render_directory: StringProperty(
        name = "Render Directory",
        description="The raw output dir (not dc6)",
        default="",
        maxlen=1024,
        subtype='DIR_PATH',
        update = camera_rig.update_render_config
        )

    dc6_directory: StringProperty(
        name = "DC6 Directory",
        description="DC6 output dir",
        default="",
        maxlen=1024,
        subtype='DIR_PATH',
        update = camera_rig.update_render_config
        )

    dc6_filename: StringProperty(
        name="DC6 Filename",
        description="DC6 Filename (without extension)",
        default="output",
        maxlen=1024,
        update= camera_rig.update_render_config
        )

    render_palette: EnumProperty(
        name="DC6 Palette",
        description="The palette to use during the DC6 conversion",
        items=[ ('ACT1', "Act 1", 'ACT1'),
                ('ACT2', "Act 2", 'ACT2'),
                ('ACT3', "Act 3", 'ACT3'),
                ('ACT4', "Act 4", 'ACT4'),
                ('ACT5', "Act 5", 'ACT5'),
                ('ENDGAME', "Endgame", 'ENDGAME'),
                ('MENU0', "Menu 0", 'MENU0'),
                ('MENU1', "Menu 1", 'MENU1'),
                ('MENU2', "Menu 2", 'MENU2'),
                ('MENU3', "Menu 3", 'MENU3'),
                ('MENU4', "Menu 4", 'MENU4'),
                ('STATIC', "Static", 'STATIC'),
                ('Sky', "Sky", 'SKY'),
                ('TRADEMARK', "Trademark", 'TRADEMARK'),
                ('UNITS', "Units", 'UNITS'),
                ('FECHAR', "Fechar", 'FECHAR'),
                ('LOADING', "Loading", 'LOADING')
                ],
                update = camera_rig.update_render_config
        )

