# ------------------------------------------------------------------------
#    Handlers
# ------------------------------------------------------------------------
import bpy
import os
import shutil

from . import d2_palettes
palettes = d2_palettes.palettes

from . import batch_encode

def render_started(directions, frames):
    multi_view_render['to_complete'] = directions*frames
    multi_view_render['completed'] = 0

def remove_dir_contents(dirpath):
    folder = dirpath
    for filename in os.listdir(folder):
        file_path = os.path.join(folder, filename)
        try:
            if os.path.isfile(file_path) or os.path.islink(file_path):
                os.unlink(file_path)
            elif os.path.isdir(file_path):
                shutil.rmtree(file_path)
        except Exception as e:
            print('Failed to delete %s. Reason: %s' % (file_path, e))

def prefix_frames(dirpath):
    folder = dirpath
    for src_filename in os.listdir(folder):
        if 'png' not in src_filename:
            continue
        src_file_path = os.path.join(folder, src_filename)
        parts = src_filename.split('_')
        if parts[0] == '':
            parts[0] = '0000'
        dst_filename = '_'.join([str(part) for part in parts])
        dst_file_path = os.path.join(folder, dst_filename)
        if os.path.isfile(src_file_path) or os.path.islink(src_file_path):
            shutil.move(src_file_path, dst_file_path)

def pre_render_frame(scene):
    # remove existing renders from image dir
    plugin = scene.DC6Plugin
    render_dir = bpy.path.abspath(plugin.render_directory)
    remove_dir_contents(render_dir)
    bpy.app.handlers.render_init.remove(pre_render_frame)

def pre_render_animation(scene):
    # remove existing renders from image dir
    plugin = scene.DC6Plugin
    render_dir = bpy.path.abspath(plugin.render_directory)
    bpy.app.handlers.render_init.remove(pre_render_animation)

def post_render(scene, single=False, do_prefix=False):
    plugin = scene.DC6Plugin
    render_dir = bpy.path.abspath(plugin.render_directory)
    dc6_dir = bpy.path.abspath(plugin.dc6_directory)
    dc6_name = plugin.dc6_filename
    palette_key = plugin.render_palette or 'ACT1'
    palette = palettes[palette_key]
    if do_prefix:
        prefix_frames(render_dir)
    if single:
        start         = scene.frame_current
        end           = scene.frame_current
        batch_encode.start(scene, start, end, render_dir, dc6_dir, dc6_name, palette)
    else:
        start         = scene.frame_start
        end           = scene.frame_end
        batch_encode.start(scene, start, end, render_dir, dc6_dir, dc6_name, palette)
    
def post_render_frame(scene):
    post_render(scene, single=True, do_prefix=True)
    bpy.app.handlers.render_complete.remove(post_render_frame)

def post_render_animation(scene):
    post_render(scene, single=False, do_prefix=False)
    bpy.app.handlers.render_complete.remove(post_render_animation)


