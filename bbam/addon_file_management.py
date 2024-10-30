import shutil
import tempfile
import sys
import os
from . import manifest_generate
from . import bl_info_generate
from . import config
from . import utils
from . import blender_exec


def copy_addon_folder(src, dst, exclude_paths=[]):
    # Fonction d'ignore pour exclure certains fichiers/dossiers lors de la copie
    def ignore_files(dir, files):
        # Créer une liste de fichiers à ignorer en vérifiant chaque chemin complet par rapport à exclude_paths
        ignore_list = []
        for file in files:
            file_path = os.path.join(dir, file)

            # Comparaison du chemin relatif pour chaque fichier avec les chemins dans exclude_paths
            relative_path = os.path.normpath(os.path.relpath(file_path, src))
            if any(relative_path.startswith(os.path.normpath(path)) for path in exclude_paths):
                ignore_list.append(file)
        return set(ignore_list)

    shutil.copytree(src, dst, ignore=ignore_files)


def create_temp_addon_folder(addon_path, addon_manifest_data, target_build_name, show_debug=True):
    # Variables
    build_data = addon_manifest_data["builds"][target_build_name]
    generate_method = build_data["generate_method"] == "EXTENTION_COMMAND"

    # Step 1: Création du dossier temporaire pour l'add-on
    temp_dir = tempfile.mkdtemp(prefix="blender_addon_")
    temp_addon_path = os.path.join(temp_dir, os.path.basename(addon_path))

    # Step 2: Copie du dossier add-on vers le dossier temporaire en excluant les chemins spécifiés
    exclude_paths = build_data["exclude_paths"]
    exclude_paths.append("bbam/") # exclude addon manager from the final build
    copy_addon_folder(addon_path, temp_addon_path, exclude_paths)
    print(f"Copied build '{target_build_name}' to temporary location: {temp_addon_path}")

    # Step 3: Génération du manifest de l'add-on
    generate_method = build_data["generate_method"]
    if generate_method == "EXTENTION_COMMAND":
        new_manifest = manifest_generate.generate_new_manifest(addon_manifest_data, target_build_name)
        manifest_generate.save_addon_manifest(temp_addon_path, new_manifest, show_debug)
    elif generate_method == "SIMPLE_ZIP":
        new_manifest = bl_info_generate.generate_new_bl_info(addon_manifest_data, target_build_name)
        bl_info_generate.update_file_bl_info(temp_addon_path, new_manifest, show_debug)

    return temp_addon_path

def zip_output_filename(addon_path, addon_manifest_data, target_build_name):
    # Vars
    manifest_data = addon_manifest_data["blender_manifest"]
    build_data = addon_manifest_data["builds"][target_build_name]
    version = utils.get_str_version(manifest_data["version"])

    # Format
    output_folder_path = os.path.abspath(os.path.join(addon_path, '..', config.build_output_folder))
    formated_file_name = build_data["naming"]
    formated_file_name = formated_file_name.replace("{Name}", build_data["pkg_id"])
    formated_file_name = formated_file_name.replace("{Version}", version)
    output_filepath = os.path.join(output_folder_path, formated_file_name)
    return output_filepath

def zip_addon_folder(src, addon_path, addon_manifest_data, target_build_name, blender_executable_path):
    # Variables
    build_data = addon_manifest_data["builds"][target_build_name]
    generate_method = build_data["generate_method"]

    # Get path and create folder
    output_filepath = zip_output_filename(addon_path, addon_manifest_data, target_build_name)
    output_dir = os.path.dirname(output_filepath)
    os.makedirs(output_dir, exist_ok=True)

    # Run addon zip
    if generate_method == "EXTENTION_COMMAND":
        print("Start build with extension command")
        result = blender_exec.build_extension(src, output_filepath, blender_executable_path)
        print(result.stdout)
        print(result.stderr, file=sys.stderr)

        created_filename = blender_exec.get_build_file(result)
        if created_filename:
            print("Start Validate")
            blender_exec.validate_extension(created_filename, blender_executable_path)
            print("End Validate")

        return created_filename
    
    elif generate_method == "SIMPLE_ZIP":
        print("Start creating simple ZIP file with root folder using shutil")

        # Nom du dossier racine à ajouter dans le ZIP
        root_folder_name = "my_addon_root_folder"

        # Créer un dossier temporaire
        with tempfile.TemporaryDirectory() as temp_dir:
            # Créer le dossier racine dans le dossier temporaire
            temp_root = os.path.join(temp_dir, root_folder_name)
            shutil.copytree(src, temp_root)

            # Utiliser shutil.make_archive pour créer le ZIP depuis le dossier temporaire
            base_name = os.path.splitext(output_filepath)[0]  # Chemin sans extension .zip
            shutil.make_archive(base_name, 'zip', temp_dir, root_folder_name)
        
        print(f"SIMPLE_ZIP created successfully at {output_filepath}")
        return output_filepath
    
