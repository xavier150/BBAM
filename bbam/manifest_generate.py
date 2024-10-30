import os
import toml
from toml.encoder import TomlEncoder

from . import config
from . import utils

class MultiLineTomlEncoder(TomlEncoder):
    def dump_list(self, v):
        """Formats lists to display on multiple lines in the TOML output."""
        output = "[\n"
        for item in v:
            output += f"  {toml.encoder._dump_str(item)},\n"  # Indents each item
        output += "]"
        return output

def generate_new_manifest(addon_generate_config_data, target_build_name):

    # Vars
    if target_build_name not in addon_generate_config_data["builds"]:
        print(f"Error: Build data for '{target_build_name}' not found!")
    
    data = {}
    manifest_data = addon_generate_config_data["blender_manifest"]
    build_data = addon_generate_config_data["builds"][target_build_name]

    # Add generic infos
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
    data["blender_version_min"] = get_str_version(build_data["blender_version_min"])

    data["license"] = manifest_data["license"]
    data["copyright"] = manifest_data["copyright"]

    # Add build focused data
    build_data = addon_generate_config_data["builds"][target_build_name]
    data["build"] = {}
    data["build"]["paths_exclude_pattern"] = build_data["exclude_paths"]

    return data

def save_addon_manifest(addon_path, data, show_debug = False):
    addon_manifest_path = os.path.join(addon_path, config.blender_manifest)
    with open(addon_manifest_path, "w") as file:
        toml.dump(data, file, encoder=MultiLineTomlEncoder())
    
        if show_debug:
            print(f"Addon manifest saved successfully at: {addon_manifest_path}")

