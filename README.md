# About
A blender-2.80 plugin that manages a camera rig, as well as batch converting the rendered output to DC6 file format.

# Prerequisites
Before installing this addon, you need to install pip with Blender's bundled python.

First, open blender and go to the scripting work area. In the python shell type the following:

```python
import sys
sys.exec_prefix
```

Inside of the directory it prints there will be a `bin` folder. inside of that is where the python binary is.
You need to download the `get_pip.py` script (https://bootstrap.pypa.io/get-pip.py) and run it with blender's python.

# Install
Clone this directory and compress to a `.zip` file. Now, run Blender and go to `Preferences` >> `Add-ons` >> `Install` and select the `.zip` you just made.

# Usage
Currently, the DC6 controls are only available in the main 3D View (you may need to click an object first...).

When you open the panel, click `Enable Rig` to create the camera rig.
The output width/height set the resolution of the render.

The palette you select from the palette list is what rthe endered images will be remapped to.

Exporting animation will render each direction for each animation frame. 16 directions @ 48 frames crashed diablo when i tried.

Exporting single frame will render each direction for the currently selected frame

# Scene Setup
Do the following:
* Remove all existing cameras
* Enable the camera rig
* Go to the `Output` properites and enable `Stereoscopy`, set `Multi-View` and disable the `left` and `right` views
* Go to `World` properties, set the background color to black (rgb 0,0,0)
* In the `Render` properties, set the rendering engine to `Cycles` (you may not need to do this, but I did it...)

# CAVEATS
The add-on is very experimental (buggy), so here are some shortcomings i'm awar of...

* exporting a single frame hasn't been well tested and will likely fail
* changing the camera rig properties will completely destroy the camera rig.
* if you accidentally put objects into the camera rig collection, they will be deleted when you change the rig settings
* Currently, the encoding always considers index 0 as the transparency index during dc6 encoding (i need to add controls in the ui for this)
