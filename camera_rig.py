# ------------------------------------------------------------------------
#    Camera Rig Functionality
# ------------------------------------------------------------------------

import bpy
import math

from . import constants
defaults = constants.defaults

sin = math.sin
cos = math.cos

rig_name = 'Camera Rig'
camera_prefix = 'Direction'
camera_suffix = '_%d'
target_name = "Target"

def createTarget(location):
    camera_target = bpy.data.objects.new(target_name, None)
    camera_target.empty_display_type = 'PLAIN_AXES'
    camera_target.location = location or defaults['camera_target_position']
    return camera_target

def createCamera(name, location):
    camera = bpy.data.cameras.new(name)
    camera_object = bpy.data.objects.new(name, camera)
    camera_object.location = location
    return camera_object

def makeCameraTrack(camera, target=defaults['camera_target_position']):
    camera.constraints.new(type='TRACK_TO')
    constraint = camera.constraints["Track To"]
    constraint.track_axis   = 'TRACK_NEGATIVE_Z'
    constraint.up_axis      = 'UP_Y'
    constraint.target       = target

def a2r(a): # angle to radian
    return (math.pi/180)*a

def makeRenderView(suffix):
    view = bpy.context.scene.render.views.new(camera_prefix + suffix)
    view.camera_suffix = suffix
    view.file_suffix = suffix

def createCameraRig(radius, height, directions, target, focal, renderWidth, renderHeight):
    cleanupRig()
    cleanupViews()
    
    bpy.context.scene.render.use_multiview = True
    
    collections = bpy.data.collections

    if (rig_name not in collections.keys()):
        rig = bpy.data.collections.new(rig_name)
        bpy.context.scene.collection.children.link(rig)

    camera_target = createTarget(target)
    rig.objects.link(camera_target)
    
    for index in range(directions):
        r       = radius
        suffix  = camera_suffix % index
        name    = camera_prefix + suffix
        theta   = a2r( 90 + (index/directions)*360 )
        x,y,z   = sin(theta)*r, cos(theta)*r, height
        c       = createCamera(name, (x,y,z))
        c.data.lens = focal
        c.data.type = 'ORTHO'
        c.data.ortho_scale = 1.414
        bpy.context.scene.render.resolution_x = renderWidth
        bpy.context.scene.render.resolution_y = renderHeight
        c.name = name # sometimes 0 comes out as 0.001
        makeCameraTrack(c, camera_target)
        makeRenderView(suffix)
        rig.objects.link(c)

def cleanupRig():
    objects = bpy.data.objects
    cameras = bpy.data.cameras
    collections = bpy.data.collections
    for key in objects.keys():
        if (target_name in key):
            o = objects.get(key)
            bpy.data.objects.remove(o)
    for key in cameras.keys():
        if (camera_prefix in key):
            o = cameras.get(key)
            bpy.data.cameras.remove(o)
    for key in collections.keys():
        if rig_name in key:
            c = collections.get(key)
            collections.remove(c)

def cleanupViews():
    views = bpy.context.scene.render.views
    for k in views.keys():
        if camera_prefix in k:
            views.remove(views.get(k))


def update_rig(self, context):
    enabled = self.get('rig_enable')
    if enabled == None:
        enabled = defaults['rig_enable']
    if self.get('rig_enable'):
        r = self.get('rig_radius') or defaults['rig_radius']
        h = self.get('rig_height') or defaults['rig_height']
        d = self.get('rig_directions') or defaults['rig_directions']
        t = defaults['camera_target_position'] # self.get('camera_target_position')
        f = self.get('camera_focal_length') or defaults['camera_focal_length']
        rw = self.get('render_width') or defaults['render_width']
        rh = self.get('render_height') or defaults['render_height']
        createCameraRig(r, h, d, t, f, rw, rh)
    else:
        cleanupViews()
        cleanupRig()

def update_render_config(self, context):
    render_dir = bpy.path.abspath(self.get('render_directory') or '//')
    dc6_dir = bpy.path.abspath(self.get('dc6_directory') or '//')
    dc6_filename = bpy.path.abspath(self.get('dc6_filename') or 'output') + '.dc6'
    palette_key = self.get('render_palette') or 'ACT1'
    bpy.context.scene.render.filepath = render_dir

