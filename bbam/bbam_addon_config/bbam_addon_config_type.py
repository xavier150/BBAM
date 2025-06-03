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

from enum import Enum
from typing import List, Dict, Tuple, Union, Any

class BBAM_AddonType(Enum):
    ADDON = "addon"
    THEME = "theme"

    def get_friendly_name(self) -> str:
        if self == BBAM_AddonType.ADDON:
            return "Add-on"
        elif self == BBAM_AddonType.THEME:
            return "Theme"
        else:
            raise ValueError(f"Unknown addon type: {self}")

    def get_as_string(self) -> str:
        if self == BBAM_AddonType.ADDON:
            return "add-on"
        elif self == BBAM_AddonType.THEME:
            return "theme"
        else:
            raise ValueError(f"Unknown addon type: {self}")
        
    def set_from_string(self, value: str) -> 'BBAM_AddonType':
        if value == "add-on":
            return BBAM_AddonType.ADDON
        elif value == "theme":
            return BBAM_AddonType.THEME
        else:
            print(f"Error: Unknown addon type '{value}' in manifest.")
            return BBAM_AddonType.ADDON

class BBAM_AddonManifest:
    # More details:
    # https://docs.blender.org/manual/fr/dev/advanced/extensions/getting_started.html
    def __init__(self) -> None:
        # Addon information
        self.addon_version: List[int] = [0, 0, 0]
        self.addon_id: str = ""
        self.addon_name: str = ""
        self.tagline: str = ""
        self.maintainer: str = ""

        # Links
        self.website_url: str = ""
        self.report_issue_url: str = ""
        self.documentation_url: str = ""

        # For older versions of Blender
        self.support: str = "COMMUNITY"

        # Additional information
        self.type: BBAM_AddonType = BBAM_AddonType.ADDON
        self.tags: List[str] = []
        self.category: str = ""

        # License conforming to https://spdx.org/licenses/ (use "SPDX: prefix)
        # https://docs.blender.org/manual/en/dev/advanced/extensions/licenses.htm
        self.license: List[str] = []

        # Optional: required by some licenses.
        self.copyright: List[str] = []

        # Optional: add-ons can list which resources they will require:
        # * files (for access of any filesystem operations)
        # * network (for internet access)
        # * clipboard (to read and/or write the system clipboard)
        # * camera (to capture photos and videos)
        # * microphone (to capture audio)
        #
        # If using network, remember to also check `bpy.app.online_access`
        # https://docs.blender.org/manual/en/dev/advanced/extensions/addons.html#internet-access
        #
        # For each permission it is important to also specify the reason why it is required.
        # Keep this a single short sentence without a period (.) at the end.
        # For longer explanations use the documentation or detail page.
        self.permissions: List[Dict[str, str]] = []

    def set_config_from_dict(self, data: Dict[str, Any]) -> bool:
        # Check
        required_keys = ["version", "id", "name"]
        for key in required_keys:
            if key not in data:
                print(f"Error: '{key}' key not found in the provided data.")
                return False

        # Update required fields
        self.addon_version = data["version"]
        self.addon_id = data["id"]
        self.addon_name = data["name"]

        # Optional fields
        self.tagline = data.get("tagline", "")
        self.maintainer = data.get("maintainer", "")
        
        self.website_url = data.get("website_url", "")
        self.report_issue_url = data.get("report_issue_url", "")
        self.documentation_url = data.get("documentation_url", "")
        self.support = data.get("support", "COMMUNITY")
        
        self.type.set_from_string(data.get("type", "add-on"))
        self.tags = data.get("tags", [])
        self.category = data.get("category", "")
        self.license = data.get("license", [])
        
        self.copyright = data.get("copyright", [])
        self.permissions = data.get("permissions", [])
    
        return True
    
    def get_version_as_string(self) -> str:
        """
        Returns the addon version as a string in the format "X.Y.Z".
        """
        return f"{self.addon_version[0]}.{self.addon_version[1]}.{self.addon_version[2]}"

class BBAM_GenerateMethod(Enum):
    EXTENTION_COMMAND = "EXTENTION_COMMAND"
    SIMPLE_ZIP = "SIMPLE_ZIP"

    def get_as_string(self) -> str:
        if self == BBAM_GenerateMethod.EXTENTION_COMMAND:
            return "EXTENTION_COMMAND"
        elif self == BBAM_GenerateMethod.SIMPLE_ZIP:
            return "SIMPLE_ZIP"
        else:
            raise ValueError(f"Unknown generate method: {self}")
        
    def set_from_string(self, value: str) -> 'BBAM_GenerateMethod':
        if value == "EXTENTION_COMMAND":
            return BBAM_GenerateMethod.EXTENTION_COMMAND
        elif value == "SIMPLE_ZIP":
            return BBAM_GenerateMethod.SIMPLE_ZIP
        else:
            print(f"Error: Unknown generate method '{value}' in manifest.")
            return BBAM_GenerateMethod.EXTENTION_COMMAND

class BBAM_AddonBuild:

    def __init__(self, build_id: str) -> None:
        self.build_id: str = build_id
        self.generate_method: BBAM_GenerateMethod = BBAM_GenerateMethod.EXTENTION_COMMAND
        
        # Use "LATEST" at tuple[1] to indicate the latest version.
        self.auto_install_range: Tuple[List[int], Union[List[int], str]] = ([0, 0, 0], [0, 0, 0])
        
        self.naming: str = "{Name}-{Version}.zip"
        self.module: str = "my_addon_module"
        self.pkg_id: str = "MyPackage"

        self.exclude_paths: List[str] = []
        self.include_paths: List[str] = []

        # Minimum supported Blender version - use at least version 4.2.0
        self.blender_version_min: List[int] = [4, 2, 0]

    def set_from_dict(self, data: Dict[str, Any]) -> bool:
        # Check
        required_keys = ["generate_method", "auto_install_range", "naming", "module", "pkg_id"]
        for key in required_keys:
            if key not in data:
                print(f"Error: '{key}' key not found in the provided data.")
                return False

        # Update required fields
        self.generate_method.set_from_string(data["generate_method"])
        self.auto_install_range = (data["auto_install_range"][0], data["auto_install_range"][1])
        
        self.naming = data["naming"]
        self.module = data["module"]
        self.pkg_id = data["pkg_id"]

        # Optional fields
        self.exclude_paths = data.get("exclude_paths", [])
        self.include_paths = data.get("include_paths", [])
        self.blender_version_min = data.get("blender_version_min", [4, 2, 0])

        return True

    def get_version_as_string(self) -> str:
        """
        Returns the minimum Blender version as a string in the format "X.Y.Z".
        """
        return f"{self.blender_version_min[0]}.{self.blender_version_min[1]}.{self.blender_version_min[2]}"

class BBAM_AddonConfig:

    def __init__(self) -> None:
        self.addon_manifest: BBAM_AddonManifest = BBAM_AddonManifest()
        self.builds: Dict[str, BBAM_AddonBuild] = {}

    def set_config_from_dict(self, data: Dict[str, Any]) -> bool:
        # Check
        required_keys = ["blender_manifest", "builds"]
        for key in required_keys:
            if key not in data:
                print(f"Error: '{key}' key not found in the provided data.")
                return False

        # Manifest
        result = self.addon_manifest.set_config_from_dict(data["blender_manifest"])
        if not result:
            print("Error: Failed to set addon manifest configuration from the provided data.")
            return False
        
        # Builds
        for build_id, build_data in data["builds"].items():
            build = BBAM_AddonBuild(build_id)
            result = build.set_from_dict(build_data)
            if not result:
                print(f"Error: Failed to set build configuration for '{build_id}' from the provided data.")
                return False
            self.builds[build_id] = build

        return True
