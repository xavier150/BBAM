import os
import sys
import importlib.util

# get bbam __init__.py file
bbam_path = os.path.abspath(os.path.join(__file__, '..', '..', '__init__.py'))
module_name = "bbam"

# Load and run bbam
spec = importlib.util.spec_from_file_location(module_name, bbam_path)
module = importlib.util.module_from_spec(spec)
sys.modules[module_name] = module
spec.loader.exec_module(module)
module.install_from_blender()


# Instructions for running this script from Blender
'''
# Run this script in Blender to generate and install the addon build.
# Ensure the paths in `addon_directories` point to the correct addon directories.
# For more details, visit the GitHub repository: https://github.com/xavier150/BBAM

import os
import importlib.util

# List of addon paths using BBAM
addon_directories = [
    # Uncomment and adjust paths as needed
    r"P:/GitHubBlenderAddon/Blender-For-UnrealEngine-Addons/blender-for-unrealengine",
    # r"M:/MMVS_ProjectFiles/Other/BlenderForMMVS",
    # r"P:/GitHubBlenderAddon/Modular-Auto-Rig/modular-auto-rig",
]

for dir in addon_directories:
    # Install or reinstall the addon
    script_path = os.path.join(dir, "bbam/exec/install_from_blender.py")
    spec = importlib.util.spec_from_file_location("install_from_blender", script_path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
'''