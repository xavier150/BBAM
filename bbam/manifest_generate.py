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
import toml
from toml.encoder import TomlEncoder

from . import config
from . import utils
from . import blender_utils

class MultiLineTomlEncoder(TomlEncoder):
    """
    Custom TOML encoder that formats lists to display on multiple lines in the output.
    """
    def dump_list(self, v):
        """
        Formats a list to display each item on a new line in the TOML output.

        Parameters:
            v (list): The list to format for multi-line display.

        Returns:
            str: A formatted multi-line string representation of the list.
        """
        output = "[\n"
        for item in v:
            output += f"  {toml.encoder._dump_str(item)},\n"  # Indent each item
        output += "]"
        return output

def generate_new_manifest(addon_generate_config_data, target_build_name):
    """
    Generates a new manifest dictionary for the addon based on the configuration data.

    Parameters:
        addon_generate_config_data (dict): The configuration data for the addon.
        target_build_name (str): The name of the target build.

    Returns:
        dict: A dictionary representing the new manifest for the addon.
    """
    # Check if the target build data exists
    if target_build_name not in addon_generate_config_data["builds"]:
        print(f"Error: Build data for '{target_build_name}' not found!")
        return {}

    data = {}
    manifest_data = addon_generate_config_data["blender_manifest"]
    build_data = addon_generate_config_data["builds"][target_build_name]

    # Populate generic information
    data["schema_version"] = config.manifest_schema_version
    data["id"] = manifest_data["id"]
    data["version"] = utils.get_str_version(manifest_data["version"])
    data["name"] = manifest_data["name"]
    data["maintainer"] = manifest_data["maintainer"]
    data["tagline"] = manifest_data["tagline"]
    data["website"] = manifest_data["website_url"]
    data["type"] = manifest_data["type"]
    data["tags"] = manifest_data["tags"]
    data["permissions"] = manifest_data["permissions"]
    data["blender_version_min"] = utils.get_str_version(build_data["blender_version_min"])
    data["license"] = manifest_data["license"]
    data["copyright"] = manifest_data["copyright"]
    return data

def save_addon_manifest(addon_path, data, show_debug=False):
    """
    Saves the addon manifest as a TOML file using the MultiLineTomlEncoder for custom formatting.

    Parameters:
        addon_path (str): Path to the addon's root folder.
        data (dict): Manifest data to save as a TOML file.
        show_debug (bool): If True, displays debug information about the save process.
    """
    addon_manifest_path = os.path.join(addon_path, config.blender_manifest)

    # Save the manifest as a TOML file with custom encoder for multi-line list formatting
    with open(addon_manifest_path, "w") as file:
        toml.dump(data, file, encoder=MultiLineTomlEncoder())

    if show_debug:
        print(f"Addon manifest saved successfully at: {addon_manifest_path}")
