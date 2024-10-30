import os
import re
from . import config



def generate_new_bl_info(addon_generate_config_data, target_build_name):

    # Vars
    if target_build_name not in addon_generate_config_data["builds"]:
        print(f"Error: Build data for '{target_build_name}' not found!")
    
    data = {}
    manifest_data = addon_generate_config_data["blender_manifest"]
    build_data = addon_generate_config_data["builds"][target_build_name]

    # Add generic infos
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
        'category': manifest_data["category"]}

    return data

def update_file_bl_info(addon_path, data, show_debug=False):
    addon_init_file_path = os.path.join(addon_path, "__init__.py")

    # Format the new `bl_info` dictionary with line breaks and indentation
    new_bl_info_lines = ["bl_info = {\n"]
    for key, value in data.items():
        new_bl_info_lines.append(f"    '{key}': {repr(value)},\n")
    new_bl_info_lines.append("}\n\n")  # Close `bl_info` and add an extra line break for readability

    with open(addon_init_file_path, 'r') as file:
        lines = file.readlines()

    with open(addon_init_file_path, "w") as file:
        in_bl_info = False
        for line in lines:
            # Detect the start of `bl_info`
            if line.strip().startswith("bl_info = {") and not in_bl_info:
                in_bl_info = True
                file.writelines(new_bl_info_lines)  # Write the new `bl_info` dictionary
            elif in_bl_info and line.strip() == "}":
                in_bl_info = False  # End of `bl_info`, but keep writing subsequent lines
            elif not in_bl_info or line.strip() != "}":
                file.write(line)  # Write all other lines unchanged
    
    if show_debug:
        print(f"Addon bl_info successfully updated at: {addon_init_file_path}")


