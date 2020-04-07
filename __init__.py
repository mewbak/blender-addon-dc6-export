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

bl_info = {
    "name": "Diablo II DC6 Export",
    "description": "Creates DC6 images for use in Diablo II",
    "author": "Gravestench",
    "version": (0, 0, 1),
    "blender": (2, 80, 0),
    "location": "3D View > Tools",
    "warning": "",
    "wiki_url": "",
    "tracker_url": "",
    "category": "Development"
}

import bpy
import subprocess

def attempt_pillow_install():
	# install Pillow image library
	blender_pypath = bpy.app.binary_path_python
	install_pillow = (blender_pypath, "-m", "pip", "install", "Pillow")
	proc = subprocess.Popen(install_pillow)

def register():
	attempt_pillow_install()
	from . import(properties, panel, operators)
	properties.register()
	panel.register()
	operators.register()

def unregister():
	from . import(properties, panel, operators)
	properties.unregister()
	panel.unregister()
	operators.unregister()

if __name__ == '__main__':
    register()
