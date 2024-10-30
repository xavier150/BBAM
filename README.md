# BleuRaven Blender Addon Manager (BBAM)

BBAM (BleuRaven Blender Addon Manager) is my personal Blender addon manager library.  
Feel free to use it! You can credit me or support my work if you'd like.

## Discord Community
If you need help or want to check out my side projects, join the Discord community!  
👉 [Join the Discord](https://discord.gg/XuYeGCFtxa)

## How to Use
1. Copy the `bbam` folder to the root of your Blender addon directory.
2. Open Blender and run the following script, updating `addon_directories` with the paths to your addons.

### Example Script

```python
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
```

3. You will found a new file "addon_generate_config.json" at the root of your addons. Edit it with you addon config.
4. Run addon the example script to generate and install you addons.
