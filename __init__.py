# ##### BEGIN GPL LICENSE BLOCK #####
#
#  This program is free software; you can redistribute it and/or
#  modify it under the terms of the GNU General Public License
#  as published by the Free Software Foundation; either version 2
#  of the License, or (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software Foundation,
#  Inc., 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301, USA.
#
# ##### END GPL LICENSE BLOCK #####

import bpy
from bpy.app.handlers import persistent

bl_info = {
    "name": "RGB Node for Giants Exporter Tool",
    "author": "Lazy E Modding",
    "version": (1, 0, 0, 0),
    "blender": (2, 83, 0),
    "location": "Shader Editor > Add Menu",
    "description": "Creates a RGB Node in the shader menu that updates automatically when connect to be able to visualize a color with a material in blender that will be similar to what it will appear like in Giants Editor.",
    "category": "Node",
    "doc_url": "https://github.com/Lazy-E-Modding/i3DColorNodeAddon/wiki/Info",
    "tracker_url": "https://github.com/Lazy-E-Modding/i3DColorNodeAddon/issues",
    "support": "COMMUNITY",
}

last_property_values = {}

def update_rgb_node(material):
    """Updates or creates the RGB node for the given material."""
    if not material or 'customParameter_colorScale' not in material.keys():
        return

    custom_value = material['customParameter_colorScale']

    try:
        r, g, b, alpha = map(float, custom_value.split())
    except ValueError:
        print(f"Invalid 'customParameter_colorScale' format for material: {material.name}")
        return

    if not material.use_nodes:
        material.use_nodes = True

    nodes = material.node_tree.nodes
    rgb_node = None

    for node in nodes:
        if node.label == "i3D RGB Node":
            rgb_node = node
            break

    if rgb_node is None:
        rgb_node = nodes.new(type='ShaderNodeRGB')
        rgb_node.location = (200, 200)
        rgb_node.label = "i3D RGB Node"
        print(f"Created new RGB node for material: {material.name}")

    rgb_node.outputs['Color'].default_value = (r, g, b, alpha)
    print(f"RGB node updated successfully for material: {material.name}")

def check_property_changes():
    """Checks for changes in the customParameter_colorScale property and updates RGB nodes."""
    global last_property_values

    for material in bpy.data.materials:
        if 'customParameter_colorScale' in material.keys():
            current_value = material['customParameter_colorScale']

            if last_property_values.get(material.name) != current_value:
                update_rgb_node(material)
                last_property_values[material.name] = current_value
        else:
            last_property_values.pop(material.name, None)

    return 1.0

@persistent
def load_post_handler(dummy):
    """Ensures the timer restarts after loading a new Blender file."""
    bpy.app.timers.register(check_property_changes)

class CUSTOM_OT_CreateRGBNode(bpy.types.Operator):
    """Create an RGB Node from 'customParameter_colorScale'"""
    bl_idname = "node.create_rgb_node"
    bl_label = "Create i3D RGB Node"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        obj = context.object
        if not obj or not obj.active_material:
            self.report({'ERROR'}, "No active material on the selected object")
            return {'CANCELLED'}

        material = obj.active_material
        update_rgb_node(material)
        self.report({'INFO'}, "RGB Node updated successfully")
        return {'FINISHED'}

class CUSTOM_PT_MaterialPanel(bpy.types.Panel):
    """Panel to display the custom property"""
    bl_label = "Custom RGB Node Panel"
    bl_idname = "CUSTOM_PT_material_panel"
    bl_space_type = 'PROPERTIES'
    bl_region_type = 'WINDOW'
    bl_context = "material"

    def draw(self, context):
        layout = self.layout
        obj = context.object

        if not obj or not obj.active_material:
            layout.label(text="No active material on the selected object")
            return

        material = obj.active_material
        layout.prop(material, "customParameter_colorScale")

def menu_func(self, context):
    self.layout.operator(CUSTOM_OT_CreateRGBNode.bl_idname)

def register():
    bpy.utils.register_class(CUSTOM_OT_CreateRGBNode)
    bpy.utils.register_class(CUSTOM_PT_MaterialPanel)
    bpy.types.NODE_MT_add.append(menu_func)

    bpy.types.Material.customParameter_colorScale = bpy.props.StringProperty(
        name="Color Scale",
        description="RGBA values for the custom RGB node",
        default="1 1 1 1"
    )

    bpy.app.handlers.load_post.append(load_post_handler)
    bpy.app.timers.register(check_property_changes)

def unregister():
    bpy.utils.unregister_class(CUSTOM_OT_CreateRGBNode)
    bpy.utils.unregister_class(CUSTOM_PT_MaterialPanel)
    bpy.types.NODE_MT_add.remove(menu_func)

    del bpy.types.Material.customParameter_colorScale

    bpy.app.handlers.load_post.remove(load_post_handler)
    bpy.app.timers.unregister(check_property_changes)

if __name__ == "__main__":
    register()
