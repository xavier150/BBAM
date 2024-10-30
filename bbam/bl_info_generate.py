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

import os
import re
from . import config

def generate_new_bl_info(addon_generate_config_data, target_build_name):
    """
    Generates a new `bl_info` dictionary for the addon based on the configuration data.

    Parameters:
        addon_generate_config_data (dict): Data containing addon configurations.
        target_build_name (str): The name of the target build configuration.

    Returns:
        dict: A dictionary representing the new `bl_info` for the addon.
    """
    # Check if the target build data exists
    if target_build_name not in addon_generate_config_data["builds"]:
        print(f"Error: Build data for '{target_build_name}' not found!")
        return {}

    manifest_data = addon_generate_config_data["blender_manifest"]
    build_data = addon_generate_config_data["builds"][target_build_name]

    # Populate `bl_info` with addon details
    data = {
        'name': manifest_data["name"],
        'author': manifest_data["maintainer"],
        'version': tuple(manifest_data["version"]),
        'blender': tuple(build_data["blender_version_min"]),
        'location': 'View3D > UI > Unreal Engine',
        'description': manifest_data["tagline"],
        'warning': '',
        "wiki_url": manifest_data["website_url"],
        'tracker_url': manifest_data["report_issue_url"],
        'support': manifest_data["support"],
        'category': manifest_data["category"]
    }

    return data

def update_file_bl_info(addon_path, data, show_debug=False):
    """
    Updates the `bl_info` dictionary in the addon's __init__.py file with new data.

    Parameters:
        addon_path (str): Path to the addon's root folder.
        data (dict): New `bl_info` dictionary to update in the file.
        show_debug (bool): If True, displays debug information about the update process.
    """
    addon_init_file_path = os.path.join(addon_path, "__init__.py")

    # Format the new `bl_info` dictionary with line breaks and indentation
    new_bl_info_lines = ["bl_info = {\n"]
    for key, value in data.items():
        new_bl_info_lines.append(f"    '{key}': {repr(value)},\n")
    new_bl_info_lines.append("}\n\n")  # Close `bl_info` and add an extra line break for readability

    # Read the existing lines of the __init__.py file
    with open(addon_init_file_path, 'r') as file:
        lines = file.readlines()

    # Write the updated lines, replacing the old `bl_info` if it exists
    with open(addon_init_file_path, "w") as file:
        in_bl_info = False
        for line in lines:
            # Detect the start of `bl_info`
            if line.strip().startswith("bl_info = {") and not in_bl_info:
                in_bl_info = True
                file.writelines(new_bl_info_lines)  # Write the new `bl_info` dictionary
            elif in_bl_info and line.strip() == "}":
                in_bl_info = False  # End of `bl_info`, but skip this closing brace line
            elif not in_bl_info:
                file.write(line)  # Write all other lines unchanged

    if show_debug:
        print(f"Addon bl_info successfully updated at: {addon_init_file_path}")