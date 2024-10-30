import sys
import os
import zipfile
import subprocess
import re
import json
import importlib

from . import config
from . import manifest_generate
from . import bl_info_generate
from . import addon_file_management
from . import utils
from . import blender_exec
from . import blender_utils

if "config" in locals():
    importlib.reload(config)
if "manifest_generate" in locals():
    importlib.reload(manifest_generate)
if "bl_info_generate" in locals():
    importlib.reload(bl_info_generate)
if "addon_file_management" in locals():
    importlib.reload(addon_file_management)
if "utils" in locals():
    importlib.reload(utils)
if "blender_exec" in locals():
    importlib.reload(blender_exec)
if "blender_utils" in locals():
    importlib.reload(blender_utils)

# List of add-on
addon_directorys = [
    #r"P:\GitHubBlenderAddon\Blender-For-UnrealEngine-Addons",
    #r"M:\MMVS_ProjectFiles\Other\BlenderForMMVS",
    r"P:\GitHubBlenderAddon\Modular-Auto-Rig",
]

# List of add-on modules and their directories
addons = [
    #{"module": "modular-auto-rig", "pkg_id": "modular_auto_rig", "directory": r"P:\GitHubBlenderAddon\Modular-Auto-Rig"},
    #{"module": "anim-bleuraven-rig", "pkg_id": "anim_bleuraven_rig", "directory": r"P:\GitHubBlenderAddon\AnimBleuRavenRig"},
    #{"module": "mmvs-addon-skeletal-mesh-generate", "pkg_id": "mmvs_addon_skeletal_mesh_generate", "directory": r"M:\MMVS_ProjectFiles\Other\MMVS_Addon_Skeletal_Mesh_Generate"},
    #{"module": "copy-visual-position", "pkg_id": "copy_visual_position", "directory": r"P:\GitHubBlenderAddon\Copy-Visual-Position"},
    #{"module": "anim-bleuraven-rig", "pkg_id": "anim_bleuraven_rig", "directory": r"P:\GitHubBlenderAddon\AnimBleuRavenRig"},
]



def should_include(file_path, exclude_paths):
    file_path_norm = os.path.normpath(file_path)
    for exclude_path in exclude_paths:
        exclude_path_norm = os.path.normpath(exclude_path)
        if file_path_norm.startswith(exclude_path_norm):
            return False
    return True

def create_zip_with_exclusions(root_folder, directory, output_filepath, exclude_paths):
    with zipfile.ZipFile(output_filepath, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for root, dirs, files in os.walk(directory):
            for file in files:
                full_path = os.path.join(root, file)
                relative_path = os.path.relpath(full_path, directory)
                if should_include(relative_path, exclude_paths):
                    # Need inclide root folder with older blender addons.
                    relative_path = os.path.join(root_folder, relative_path)
                    zipf.write(full_path, relative_path)

def get_addon_version(source_files_addon):
    version = None

    file_path = os.path.join(source_files_addon, "blender_manifest.toml")
    with open(file_path, 'r') as file:
        for line in file:
            if line.startswith("version"):
                version = line.split('=')[1].strip().strip('"')
                return version

def uninstall_addon(pkg_id, module):
    if bpy.app.version >= (4, 2, 0):
        bpy.ops.extensions.package_uninstall(repo_index=1, pkg_id=pkg_id)
        bpy.ops.preferences.addon_remove(module=module)
    else:
        bpy.ops.preferences.addon_remove(module=module)
        
def install_addon(file_naming, directory, pkg_id, module, build_info):
    
    source_files_addon = os.path.join(directory, module)  
    
    exclude_paths = build_info["exclude_paths"]
    use_extension_build_command = build_info["use_extension_build_command"]
    install = build_info["install"]
    
    version = get_addon_version(source_files_addon)
    formated_file_name = file_naming
    formated_file_name = formated_file_name.replace("{Name}", pkg_id)
    formated_file_name = formated_file_name.replace("{Version}", version)
    output_filepath = os.path.join(directory, formated_file_name)
    
    if use_extension_build_command:
        if bpy.app.version >= (4, 2, 0):
            print("Start build with extension command")
            command = [
                blender_executable_path,
                '--command', 'extension', 'build',
                '--source-dir', source_files_addon,
                '--output-filepath', output_filepath,
            ]
            
            result = subprocess.run(command, capture_output=True, text=True)
            
            print(result.stdout)
            print(result.stderr, file=sys.stderr)
            match = re.search(r'created: "([^"]+)"', result.stdout)
            if match:
                created_filename = match.group(1)
                
                print("Start Validate")
                validate_command = [
                    blender_executable_path,
                    '--command', 'extension', 'validate', 
                    created_filename,
                ]
                subprocess.run(validate_command)
                print("End Validate")
                
                if(install):
                    print("Install as extension...", created_filename)
                    bpy.ops.extensions.package_install_files(repo="user_default", filepath=created_filename, enable_on_install=True)
                    print("End")
            else:
                print("Error created file not found!")

    else:    
        print("Start build without extension command")
        source_files_addon = os.path.join(directory, module)
        destination_zip = os.path.join(directory, pkg_id+"-"+version)
        create_zip_with_exclusions(module, source_files_addon, output_filepath, exclude_paths)
        
        if(install):
            print("Install as add-on...", output_filepath)
            bpy.ops.preferences.addon_install(overwrite=True, filepath=output_filepath)
            bpy.ops.preferences.addon_enable(module=module)
        
def install_from_directory(addon_directorys):
    print("")  
    print("")  
    print("")  
    for addon_dir in addon_directorys:
        build_info_file = os.path.join(addon_dir, "generate_builds_info.json")
        with open(build_info_file, 'r', encoding='utf-8') as file:
            data = json.load(file)
            
            for build_info_key in data:
                print("")  
                print(f"### [uninstall {build_info_key} add-on...] ###")
                
                # Uninstall the add-on if it's already installed
                build_info = data[build_info_key]
                pkg_id = build_info["pkg_id"]
                module = build_info["module"]
                uninstall_addon(pkg_id, module)
            
            for build_info_key in data:
                print("")  
                print(f"### [Buils {build_info_key} add-on...] ###")
            
                # Install the add-on or extention from the zip archive and enable it. 
                build_info = data[build_info_key]
                file_naming = build_info["naming"]
                pkg_id = build_info["pkg_id"]
                module = build_info["module"]
                install_addon(file_naming, addon_dir, pkg_id, module, build_info)  

    print("###################################################")

def install_from_blender():
    # search the current addon using lib folder:
    addon_manifest = config.addon_generate_config

    addon_path = os.path.abspath(os.path.join(__file__, '..', '..'))
    search_addon_folder = os.path.abspath(os.path.join(addon_path, addon_manifest))

    if os.path.isfile(search_addon_folder):
        with open(search_addon_folder, 'r', encoding='utf-8') as file:
            data = json.load(file)
            install_from_blender_with_build_data(addon_path, data)
    else:
        print(f"Error: '{addon_manifest}' was not found in '{search_addon_folder}'.")

def install_from_blender_with_build_data(addon_path, addon_manifest_data):
    import bpy
    blender_executable_path = bpy.app.binary_path

    for target_build_name in addon_manifest_data["builds"]:
        temp_addon_path = addon_file_management.create_temp_addon_folder(addon_path, addon_manifest_data, target_build_name)
        zip_file = addon_file_management.zip_addon_folder(temp_addon_path, addon_path, addon_manifest_data, target_build_name, blender_executable_path)
        
        build_data = addon_manifest_data["builds"][target_build_name]
        pkg_id = build_data["pkg_id"]
        module = build_data["module"]
        blender_utils.uninstall_addon_from_blender(bpy, pkg_id, module)

        auto_install_range = utils.get_tuple_range_version(build_data["auto_install_range"])
        should_install = utils.get_version_in_range(bpy.app.version, auto_install_range)
        if(should_install):
            blender_utils.install_zip_addon_from_blender(bpy, zip_file, module)


    return
    for build_info_key in data:
        print("")  
        print(f"### [uninstall {build_info_key} add-on...] ###")
        
        # Uninstall the add-on if it's already installed
        build_info = data[build_info_key]
        pkg_id = build_info["pkg_id"]
        module = build_info["module"]
        uninstall_addon(pkg_id, module)
    
    for build_info_key in data:
        print("")  
        print(f"### [Buils {build_info_key} add-on...] ###")
    
        # Install the add-on or extention from the zip archive and enable it. 
        build_info = data[build_info_key]
        file_naming = build_info["naming"]
        pkg_id = build_info["pkg_id"]
        module = build_info["module"]
        install_addon(file_naming, addon_path, pkg_id, module, build_info)  