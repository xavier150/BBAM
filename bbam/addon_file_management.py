# ====================== BEGIN GPL LICENSE BLOCK ============================
#
#  This program is free software: you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation, either version 3 of the License, or
#  (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.	 See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program.	 If not, see <http://www.gnu.org/licenses/>.
#  All rights reserved.
#
# ======================= END GPL LICENSE BLOCK =============================

# ----------------------------------------------
#  BBAM -> BleuRaven Blender Addon Manager
#  https://github.com/xavier150/BBAM
#  BleuRaven.fr
#  XavierLoux.com
# ----------------------------------------------

import shutil
import tempfile
import sys
import os
from typing import Optional, List, Set
from . import manifest_generate
from . import bl_info_generate
from . import config
from . import blender_exec
from .bbam_addon_config.bbam_addon_config_type import BBAM_AddonConfig, BBAM_AddonBuild, BBAM_GenerateMethod


def copy_addon_folder(
    src: str,
    dst: str,
    exclude_paths: list[str] = [],
    include_paths: list[str] = []
):
    """
    Copies the addon folder from 'src' to 'dst' while excluding specified files and folders.
    """

    exclude_folders = ["__pycache__", ".git", ".svn", ".vscode", ".idea", "node_modules"]
    exclude_files = [".blend1", ".blend2", ".blend3", ".blend4", ".blend5", ".blend6", ".blend7", ".blend8", ".blend9"]

    # Normalize paths for comparison
    exclude_paths = [os.path.normpath(path) for path in exclude_paths]
    include_paths = [os.path.normpath(path) for path in include_paths]

    # Ignore function to exclude specific files/folders during the copy
    def ignore_files(dir: str, files: List[str]) -> Set[str]:
        ignore_list: Set[str] = set()
        for file in files:
            file_path = os.path.join(dir, file)
            relative_path = os.path.normpath(os.path.relpath(file_path, src))

            # Exclure les dossiers par nom
            if file in exclude_folders and os.path.isdir(file_path):
                continue

            # Exclure les fichiers par extension
            if any(file.endswith(ext) for ext in exclude_files) and os.path.isfile(file_path):
                continue

            # Skip directories if only files should be ignored
            if os.path.isdir(file_path):
                continue

            # Check if the file path should be included
            if any(relative_path.startswith(os.path.normpath(path)) for path in include_paths):
                continue  # Skip excluding this file or folder

            # Check if the file path should be excluded
            if any(relative_path.startswith(os.path.normpath(path)) for path in exclude_paths):
                ignore_list.add(file)
        return ignore_list

    shutil.copytree(src, dst, ignore=ignore_files)


def create_temp_addon_folder(
    addon_path: str, 
    build_config: BBAM_AddonBuild,
) -> str:
    """
    Creates a temporary folder for the addon, copies relevant files, and generates the manifest.
    """
    

    # Step 1: Create a temporary directory for the addon
    temp_dir = tempfile.mkdtemp(prefix="blender_addon_")
    temp_addon_path = os.path.join(temp_dir, os.path.basename(addon_path))

    # Step 2: Copy addon folder to temporary directory, excluding specified paths
    exclude_paths = build_config.exclude_paths
    include_paths = build_config.include_paths
    exclude_paths.append("bbam/")  # Exclude addon manager from the final build
    copy_addon_folder(addon_path, temp_addon_path, exclude_paths, include_paths)
    print(f"Copied build '{build_config.build_id}' to temporary location")
    print(f"Path: {temp_addon_path}")
    return temp_addon_path

def generate_addon_files(
    addon_path: str, 
    addon_config: BBAM_AddonConfig,
    build_config: BBAM_AddonBuild,
    show_debug: bool = True
) -> None:
    generate_method = build_config.generate_method
    if generate_method == BBAM_GenerateMethod.EXTENTION_COMMAND:
        new_manifest = manifest_generate.generate_new_manifest(addon_config, build_config)
        manifest_generate.save_addon_manifest(addon_path, new_manifest, show_debug)
    elif generate_method == BBAM_GenerateMethod.SIMPLE_ZIP:
        new_manifest = bl_info_generate.generate_new_bl_info(addon_config, build_config)
        bl_info_generate.update_file_bl_info(addon_path, new_manifest, show_debug)
    

def get_zip_output_filename(
    addon_path: str, 
    build_config: BBAM_AddonBuild,
):
    """
    Generates the output filename for the ZIP file based on naming conventions in the manifest.
    """

    # Formatting output filename
    version_str = build_config.get_version_as_string()
    output_folder_path = os.path.abspath(os.path.join(addon_path, '..', config.build_output_folder))
    formatted_file_name = build_config.naming.replace("{Name}", build_config.pkg_id).replace("{Version}", version_str)
    output_filepath = os.path.join(output_folder_path, formatted_file_name)
    return output_filepath

def zip_addon_folder(
    src: str, 
    addon_path: str, 
    build_config: BBAM_AddonBuild,
    blender_executable_path: str
) -> Optional[str]:
    """
    Creates a ZIP archive of the addon folder, either through Blender's extension command
    or by using a simple ZIP method.
    """
    generate_method = build_config.generate_method

    # Define output file path and ensure the output directory exists
    output_filepath = get_zip_output_filename(addon_path, build_config)
    output_dir = os.path.dirname(output_filepath)
    os.makedirs(output_dir, exist_ok=True)

    # Run addon zip process based on the specified generation method
    if generate_method == BBAM_GenerateMethod.EXTENTION_COMMAND:
        print("Start build with extension command")
        result = blender_exec.build_extension(src, output_filepath, blender_executable_path)
        if result.returncode == 0:
            created_filename = blender_exec.get_build_file(result)
            if created_filename:
                print(f"EXTENTION_COMMAND created successfully at {created_filename}")
                return created_filename
            else:
                print("Error: No created filename found in the result of the extension command.")
                return None
        else:  
            print(f"Error: Build failed with return code {result.returncode}.", file=sys.stderr)
            print(result.stdout, file=sys.stderr)
            print(result.stderr, file=sys.stderr)
            return None

    elif generate_method == BBAM_GenerateMethod.SIMPLE_ZIP:
        print("Start creating simple ZIP file with root folder using shutil")

        # Specify the root folder name inside the ZIP file
        root_folder_name = build_config.module

        # Create a temporary directory
        with tempfile.TemporaryDirectory() as temp_dir:
            # Copy the source folder to a temporary root folder
            temp_root = os.path.join(temp_dir, root_folder_name)
            shutil.copytree(src, temp_root)

            # Use shutil to create the ZIP archive from the temporary directory
            base_name = os.path.splitext(output_filepath)[0]  # Path without .zip extension
            shutil.make_archive(base_name, 'zip', temp_dir, root_folder_name)
        
        print(f"SIMPLE_ZIP created successfully at {output_filepath}")
        return output_filepath
    
def validate_zip_file(
    zip_file: str, 
    build_config: BBAM_AddonBuild,
    blender_executable_path: str
) -> bool:
    """
    Validates the generated ZIP file
    """
    generate_method = build_config.generate_method

        # Run addon zip process based on the specified generation method
    if generate_method == BBAM_GenerateMethod.EXTENTION_COMMAND:
        print("Start validate with extension command")
        result = blender_exec.validate_extension(zip_file, blender_executable_path)
        if result.returncode == 0:
            print("Validation successful.")
            return True
        else:
            print(f"Validation failed with return code {result.returncode}.", file=sys.stderr)
            print(result.stdout, file=sys.stderr)
            print(result.stderr, file=sys.stderr)
            return False

    elif generate_method == BBAM_GenerateMethod.SIMPLE_ZIP:
        print("No validation needed for SIMPLE_ZIP method.")
        return True
    
    return False

    
