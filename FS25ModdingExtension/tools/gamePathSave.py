""" bl_info = {
    "name": "Game Path Saver",
    "author": "Lazy E Modding",
    "version": (1, 0, 1, 0),
    "blender": (2, 83, 0),
    "location": "Shader Editor > Add Menu",
    "description": "Creates a RGB Node in the shader menu that updates automatically when connected to visualize a color with a material in Blender similar to what it will appear like in Giants Editor.",
    "category": "Node",
    "doc_url": "https://github.com/Lazy-E-Modding/i3DColorNodeAddon/wiki/Info",
    "tracker_url": "https://github.com/Lazy-E-Modding/i3DColorNodeAddon/issues",
    "support": "COMMUNITY",
} """

import bpy
from bpy.app.handlers import persistent
from bpy.props import StringProperty
from os.path import join

class CustomAddonPreferences(bpy.types.AddonPreferences):
    """FS25 Game Directory"""
    bl_idname = __name__

    file_path: StringProperty(
        name="File Path",
        description="Path to a file",
        default="",
        subtype='FILE_PATH',
    )

    def draw(self, context):
        layout = self.layout
        layout.label(text="FS25 Game Directory")
        layout.prop(self, "file_path")

@persistent
def assign_file_path(scene=None):
    """Assign the saved file path to the custom scene properties."""
    addon_prefs = bpy.context.preferences.addons.get(__name__)
    if not addon_prefs:
        return
    file_path = addon_prefs.preferences.file_path

    scene = bpy.data.scenes.get("Scene") or bpy.context.scene
    if hasattr(scene, "I3D_UIexportSettings"):
        ui_export_settings = scene.I3D_UIexportSettings

        if hasattr(ui_export_settings, "i3D_gameLocationDisplay"):
            ui_export_settings.i3D_gameLocationDisplay = file_path
            print(f"Assigned gameLocationDisplay: {file_path}")
        
        if hasattr(ui_export_settings, "i3D_shaderFolderLocation"):
            shader_folder_path = join(file_path, "data", "shaders")
            ui_export_settings.i3D_shaderFolderLocation = shader_folder_path
            print(f"Assigned shaderFolderLocation: {shader_folder_path}")
    else:
        print("I3D_UIexportSettings not found. Property assignment skipped.")

def register():
    bpy.utils.register_class(CustomAddonPreferences)
    
    bpy.app.handlers.load_post.append(assign_file_path)

def unregister():
    bpy.utils.unregister_class(CustomAddonPreferences)

    bpy.app.handlers.load_post.remove(assign_file_path)

