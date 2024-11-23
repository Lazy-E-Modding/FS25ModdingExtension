# Copyright (c) 2024 Lazy E Modding. All rights reserved.
#
# This script is the exclusive property of Lazy E Modding and is protected under applicable copyright laws and international treaties.
#
# Unauthorized reproduction, modification, distribution, or use of this script or any portion of it, in any form, is strictly prohibited without prior written permission from Lazy E Modding.
#
# Violations may result in civil and/or criminal penalties as provided by law.

bl_info = {
    "name": "Custom RGB Node Creator",
    "author": "Lazy E Modding",
    "version": (1, 0),
    "blender": (4, 2, 2),
    "location": "Shader Editor > Add Menu",
    "description": "Creates an RGB node using the 'customParameter_colorScale' custom property",
    "category": "Node",
}

import bpy

class CUSTOM_OT_CreateRGBNode(bpy.types.Operator):
    """Create an RGB Node from 'customParameter_colorScale'"""
    bl_idname = "node.create_rgb_node"
    bl_label = "Create RGB Node"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        # Get the selected object
        obj = bpy.context.object
        if not obj:
            self.report({'ERROR'}, "No object selected")
            return {'CANCELLED'}

        # Get the active material
        material = obj.active_material
        if not material:
            self.report({'ERROR'}, "The selected object has no active material")
            return {'CANCELLED'}

        # Check for the custom property
        if 'customParameter_colorScale' not in material.keys():
            self.report({'ERROR'}, "'customParameter_colorScale' not found in the material")
            return {'CANCELLED'}

        # Get the value of 'customParameter_colorScale'
        custom_value = material['customParameter_colorScale']

        try:
            # Split the custom value into RGBA components
            r, g, b, alpha = map(float, custom_value.split())
        except ValueError:
            self.report({'ERROR'}, "Invalid 'customParameter_colorScale' format")
            return {'CANCELLED'}

        # Ensure the material has a node tree
        if not material.use_nodes:
            material.use_nodes = True

        # Get the material's node tree
        nodes = material.node_tree.nodes

        # Create an RGB node
        rgb_node = nodes.new(type='ShaderNodeRGB')
        rgb_node.location = (200, 200)

        # Set the RGB values from the custom property
        rgb_node.outputs['Color'].default_value = (r, g, b, alpha)

        self.report({'INFO'}, "RGB Node created successfully")
        return {'FINISHED'}


def menu_func(self, context):
    self.layout.operator(CUSTOM_OT_CreateRGBNode.bl_idname)


def register():
    bpy.utils.register_class(CUSTOM_OT_CreateRGBNode)
    bpy.types.NODE_MT_add.append(menu_func)


def unregister():
    bpy.utils.unregister_class(CUSTOM_OT_CreateRGBNode)
    bpy.types.NODE_MT_add.remove(menu_func)


if __name__ == "__main__":
    register()
