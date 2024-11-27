import bpy
from bpy.app.handlers import persistent

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

def register():
    bpy.utils.register_class(CUSTOM_OT_CreateRGBNode)
    bpy.types.Material.customParameter_colorScale = bpy.props.StringProperty(
        name="Color Scale",
        description="RGBA values for the custom RGB node",
        default="1 1 1 1"
    )
    bpy.app.handlers.load_post.append(load_post_handler)
    bpy.app.timers.register(check_property_changes)

def unregister():
    bpy.utils.unregister_class(CUSTOM_OT_CreateRGBNode)
    del bpy.types.Material.customParameter_colorScale
    bpy.app.handlers.load_post.remove(load_post_handler)
    bpy.app.timers.unregister(check_property_changes)
