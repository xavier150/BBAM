from . import utils

def uninstall_addon_from_blender(bpy, pkg_id, module):
    if bpy.app.version >= (4, 2, 0):
        bpy.ops.extensions.package_uninstall(repo_index=1, pkg_id=pkg_id)
        bpy.ops.preferences.addon_remove(module=module)
    else:
        bpy.ops.preferences.addon_remove(module=module)



def install_zip_addon_from_blender(bpy, zip_file, module):
    if bpy.app.version >= (4, 2, 0):
        print("Install as extension...", zip_file)
        bpy.ops.extensions.package_install_files(repo="user_default", filepath=zip_file, enable_on_install=True)
        print("End")
    else:    
        print("Install as add-on...", zip_file)
        bpy.ops.preferences.addon_install(overwrite=True, filepath=zip_file)
        bpy.ops.preferences.addon_enable(module=module)