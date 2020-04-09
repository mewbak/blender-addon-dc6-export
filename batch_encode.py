import bpy
import os
from operator import itemgetter

from math import (pi, sqrt, sin, cos)

from PIL import Image

from . import dc6

DC6Encoder = dc6.DC6FileEncoder

# ------------------------------------------------------------------------
#    PNG -> DC6 conversion
# ------------------------------------------------------------------------
def start(scene, frame_start, frame_end, src_dir, dst_dir, dst_name, dst_palette):
    directions_count    = scene.DC6Plugin.rig_directions
    frame_count         = frame_end - frame_start + 1

    # ensure dc6 extension in dst filename
    if dst_name[-4:] != '.dc6':
        dst_name += '.dc6'

    folder = bpy.path.abspath(src_dir)
    # for singledirection, filenames are like `0001.png`
    # for single frame, filenames like `_0.png`
    # for multi direction+frames, filename like `0001_0.png`
    # we just need to get them and sort the array
    ordered_filepaths = []
    for filename in os.listdir(folder):
        filepath = os.path.join(folder, filename)
        if os.path.isfile(filepath) or os.path.islink(filepath):
            if '.png' in filepath:
                ordered_filepaths.append(filepath)
    ordered_filepaths.sort()
    
    print('Generating DC6 using the following:\n', '\n'.join(ordered_filepaths))
    framedatas = []
    for frame_path in ordered_filepaths:
        # remap to target palette
        img = Image.open(frame_path).convert('P')
        img = remap_image_to_target_palette(img, dst_palette)
        w = img.width
        h = img.height
        framedatas.append([b for b in img.getdata()])
    
    dc6file = DC6Encoder(directions_count, frame_count, w, h, framedatas)

    dc6_path = os.path.join(bpy.path.abspath(dst_dir), dst_name)

    print('GENERATING DC6:', dc6_path)
    dc6file.fileinfo()

    outfile = open(dc6_path, "wb")
    outfile.write(dc6file.getbytes())
    outfile.close()

def load_image(filepath):
    img = Image.open(filepath).convert('P')
    return img

def remap_image_to_target_palette(src_img, dst_palette):
    src_palette      = src_img.getpalette()
    len_src          = len(src_palette)
    len_dst          = len(dst_palette)

    # group like [ [r,g,b], ... ]
    src_palette_grp  = [src_palette[i*3:(i+1)*3] for i in range((len_src+2)//3)]
    dst_palette_grp  = [dst_palette[i*3:(i+1)*3][::-1] for i in range((len_dst+2)//3)]

    # make a mapping of closest colors of src to dst palette
    mapping = [get_closest_color_index(c[0],c[1],c[2],dst_palette_grp) for c in src_palette_grp]

    width           = src_img.width
    height          = src_img.height
    src_data        = src_img.getdata()
    dst_data        = [mapping[idx] for idx in src_data]

    src_img.putdata(dst_data)
    src_img.putpalette([b for b in dst_palette])
    return src_img

def file_bytes(filepath):
    return open(filepath, "rb").read()

def get_closest_color_index(r,g,b,p):
    distances = [sqrt((r-c[0])**2 + (g-c[1])**2 + (b-c[2])**2) for c in p]
    closest = min(enumerate(distances), key=itemgetter(1))[0]
    return closest
