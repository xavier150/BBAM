# BleuRaven Blender Addon Manager (BBAM)

BBAM (BleuRaven Blender Addon Manager) is my personal Blender addon manager library.  
Feel free to use it! You can credit me or support my work if you'd like.


### How to Use
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

# Features
- With BBAM no need to create a blender_manifest.toml or a bl_info = {} in the __init__.py file.
  You set all the addon config in "addon_generate_config.json"

- BBAM can generate several addon builds, depending the use. See the addon addon_generate_config.json Exemple

### Example addon_generate_config.json
This is the file use in my addon [Blender For UnrealEngine]https://github.com/xavier150/Blender-For-UnrealEngine-Addons

```json
{
    "schema_version": [1,0,0],
    "blender_manifest": {
        "id": "unrealengine_assets_exporter",
        "version": [4,3,8],
        "name": "Unreal Engine Assets Exporter",
        "tagline": "Allows to batch export and import in Unreal Engine",
        "maintainer": "Loux Xavier (BleuRaven) xavierloux.loux@gmail.com",

        "website_url": "https://github.com/xavier150/Blender-For-UnrealEngine-Addons/",
        "report_issue_url": "https://github.com/xavier150/Blender-For-UnrealEngine-Addons/issues",
        "support": "COMMUNITY",

        "type": "add-on",
        "tags": ["Import-Export"],
        "category": "Import-Export",
        "license": ["SPDX:GPL-3.0-or-later"],
        
        "copyright": [
        "2024 Xavier Loux",
        "2013 Blender Foundation",
        "2006-2012 assimp team",
        "2013 Campbell Barton",
        "2014 Bastien Montagne"
        ],
                
        "permissions": {
            "files": "Import/export FBX from/to disk",
            "clipboard": "Copy generated script paths"
        }
    },

    "builds": {
        "unrealengine_assets_exporter_4.2": {   
            "generate_method": "EXTENTION_COMMAND",
            "auto_install_range": [[4,2,0], [4,3,0]],
            "use_extension_build_command": true,
            "naming": "{Name}-{Version}.zip",
            "module": "blender-for-unrealengine", 
            "pkg_id": "unrealengine_assets_exporter", 
            "directory": "P:\\GitHubBlenderAddon\\Blender-For-UnrealEngine-Addons",
            "exclude_paths": [
                "fbxio/generator/",
                "fbxio/run_generator.py",
                "fbxio/io_scene_fbx_2_83/", 
                "fbxio/io_scene_fbx_2_93/", 
                "fbxio/io_scene_fbx_3_1/", 
                "fbxio/io_scene_fbx_3_2/", 
                "fbxio/io_scene_fbx_3_3/", 
                "fbxio/io_scene_fbx_3_4/", 
                "fbxio/io_scene_fbx_3_5/", 
                "fbxio/io_scene_fbx_3_6/"
            ],
            "blender_version_min": [4,2,0]
        },
        "unrealengine_assets_exporter_2.8": {
            "generate_method": "SIMPLE_ZIP",
            "auto_install_range": [[2,80,0], [4,1,0]],
            "use_extension_build_command": false,
            "naming": "{Name}-{Version}-blender2.8-4.1.zip",
            "module": "blender-for-unrealengine", 
            "pkg_id": "unrealengine_assets_exporter", 
            "directory": "P:\\GitHubBlenderAddon\\Blender-For-UnrealEngine-Addons",
            "exclude_paths": [
                "fbxio/generator/",
                "fbxio/run_generator.py",
                "fbxio/io_scene_fbx_4_0/", 
                "fbxio/io_scene_fbx_4_1/", 
                "fbxio/io_scene_fbx_4_2/", 
                "fbxio/io_scene_fbx_4_3/"
            ],
            "blender_version_min": [2,80,0]
        }
    }
}
```

I will add more detail in the wiki later is people use it and need help.

## Discord Community
If you need help or want to check out my side projects, join the Discord community!  
👉 [Join the Discord](https://discord.gg/XuYeGCFtxa)
