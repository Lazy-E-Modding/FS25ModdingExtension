# ##### BEGIN GPL LICENSE BLOCK #####
# This program is free software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License
# as published by the Free Software Foundation; either version 2
# of the License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <https://www.gnu.org/licenses/>.
# ##### END GPL LICENSE BLOCK #####

bl_info = {
    "name": "FS25 Modding Extension",
    "author": "Lazy E Modding",
    "version": (1, 0, 1, 0),
    "blender": (2, 83, 0),
    "location": "Shader Editor > Add Menu",
    "description": "Adds an RGB Node to the shader menu, visualizing colors similar to Giants Editor.",
    "category": "Node",
    "doc_url": "https://github.com/Lazy-E-Modding/i3DColorNodeAddon/wiki/Info",
    "tracker_url": "https://github.com/Lazy-E-Modding/i3DColorNodeAddon/issues",
    "support": "COMMUNITY",
}

import bpy
from bpy.app.handlers import persistent
from bpy.props import StringProperty
from os.path import join
from .tools import i3DColorNode


class CustomAddonPreferences(bpy.types.AddonPreferences):
    """Preferences for FS25 Modding Extension"""
    bl_idname = __name__

    file_path: StringProperty(
        name="File Path",
        description="Path to the FS25 game directory",
        default="",
        subtype='FILE_PATH',
    )

    def draw(self, context):
        layout = self.layout
        layout.label(text="FS25 Game Directory")
        layout.prop(self, "file_path")


@persistent
def assign_file_path(scene=None):
    """Assigns the saved file path to custom scene properties."""
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
    i3DColorNode.register()
    bpy.utils.register_class(CustomAddonPreferences)
    bpy.app.handlers.load_post.append(assign_file_path)


def unregister():
    i3DColorNode.unregister()
    bpy.utils.unregister_class(CustomAddonPreferences)
    bpy.app.handlers.load_post.remove(assign_file_path)


if __name__ == "__main__":
    register()
