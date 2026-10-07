import bpy

def get_or_create_radial_array_node_group():
    """Initialize Radial Array node group, or get it if it already exists."""
    
    if "Radial Array" in bpy.data.node_groups:
        return bpy.data.node_groups["Radial Array"]
        
    radial_array_1 = bpy.data.node_groups.new(type='GeometryNodeTree', name="Radial Array")
    radial_array_1.is_modifier = True

    radial_array_1.interface.new_socket(name="Geometry", in_out='OUTPUT', socket_type='NodeSocketGeometry')
    radial_array_1.interface.new_socket(name="Geometry", in_out='INPUT', socket_type='NodeSocketGeometry')
    
    count_socket = radial_array_1.interface.new_socket(name="Count", in_out='INPUT', socket_type='NodeSocketInt')
    count_socket.default_value = 10
    count_socket.min_value = 1
    
    radius_socket = radial_array_1.interface.new_socket(name="Radius", in_out='INPUT', socket_type='NodeSocketFloat')
    radius_socket.default_value = 1.0
    radius_socket.min_value = 0.0
    
    axis_socket = radial_array_1.interface.new_socket(name="Axis", in_out='INPUT', socket_type='NodeSocketMenu')
    alignment_socket = radial_array_1.interface.new_socket(name="Alignment", in_out='INPUT', socket_type='NodeSocketMenu')
    
    spin_offset_socket = radial_array_1.interface.new_socket(name="Spin Offset", in_out='INPUT', socket_type='NodeSocketFloat')
    spin_offset_socket.default_value = 0.0
    spin_offset_socket.subtype = 'ANGLE'

    group_input = radial_array_1.nodes.new("NodeGroupInput")
    group_input.location = (-596.736328125, 37.035865783691406)

    group_output = radial_array_1.nodes.new("NodeGroupOutput")
    group_output.is_active_output = True
    group_output.location = (946.0616455078125, -90.23860168457031)

    mesh_circle = radial_array_1.nodes.new("GeometryNodeMeshCircle")
    mesh_circle.location = (-254.57606506347656, 2.700758457183838)

    combine_xyz = radial_array_1.nodes.new("ShaderNodeCombineXYZ")
    combine_xyz.location = (-492.1060791015625, -364.81048583984375)

    transform_geometry_001 = radial_array_1.nodes.new("GeometryNodeTransform")
    transform_geometry_001.location = (-63.193885803222656, -228.99835205078125)

    normal = radial_array_1.nodes.new("GeometryNodeInputNormal")
    normal.location = (-202.7311248779297, 98.97842407226562)

    align_rotation_to_vector = radial_array_1.nodes.new("FunctionNodeAlignRotationToVector")
    align_rotation_to_vector.axis = 'X'
    align_rotation_to_vector.location = (3.2636916637420654, 237.03585815429688)

    align_rotation_to_vector_001 = radial_array_1.nodes.new("FunctionNodeAlignRotationToVector")
    align_rotation_to_vector_001.axis = 'Y'
    align_rotation_to_vector_001.location = (18.250743865966797, 10.024630546569824)

    alignment = radial_array_1.nodes.new("GeometryNodeMenuSwitch")
    alignment.active_index = 0
    alignment.data_type = 'ROTATION'
    if hasattr(alignment, "enum_items"):
        alignment.enum_items[0].name = "Outward"
        alignment.enum_items[1].name = "Along path"
    alignment.location = (248.6071014404297, -194.1221160888672)

    instance_on_points = radial_array_1.nodes.new("GeometryNodeInstanceOnPoints")
    instance_on_points.location = (405.3375244140625, 153.6240997314453)

    axis = radial_array_1.nodes.new("GeometryNodeMenuSwitch")
    axis.active_index = 2
    axis.data_type = 'ROTATION'
    if hasattr(axis, "enum_items"):
        axis.enum_items[0].name = "X"
        axis.enum_items[1].name = "Y"
        axis.enum_items.new("Z")
    axis.inputs[1].default_value = (0.0, 1.5707963705062866, 0.0)
    axis.inputs[2].default_value = (1.5707963705062866, 0.0, 0.0)
    axis.inputs[3].default_value = (0.0, 0.0, 0.0)
    axis.location = (6.354264259338379, -502.3935546875)

    transform_geometry = radial_array_1.nodes.new("GeometryNodeTransform")
    transform_geometry.location = (595.480224609375, -179.17892456054688)

    realize_instances = radial_array_1.nodes.new("GeometryNodeRealizeInstances")
    realize_instances.location = (762.6696166992188, -5.562989711761475)


    links = radial_array_1.links
    links.new(group_input.outputs["Geometry"], instance_on_points.inputs["Instance"])
    links.new(group_input.outputs["Count"], mesh_circle.inputs["Vertices"])
    links.new(group_input.outputs["Radius"], mesh_circle.inputs["Radius"])
    links.new(group_input.outputs["Axis"], axis.inputs["Menu"])
    links.new(group_input.outputs["Alignment"], alignment.inputs["Menu"])
    links.new(group_input.outputs["Spin Offset"], combine_xyz.inputs["Z"])

    links.new(mesh_circle.outputs["Mesh"], transform_geometry_001.inputs["Geometry"])
    links.new(combine_xyz.outputs["Vector"], transform_geometry_001.inputs["Rotation"])
    
    links.new(transform_geometry_001.outputs[0], instance_on_points.inputs["Points"])
    
    links.new(normal.outputs["Normal"], align_rotation_to_vector.inputs["Vector"])
    links.new(normal.outputs["Normal"], align_rotation_to_vector_001.inputs["Vector"])
    
    links.new(align_rotation_to_vector.outputs[0], alignment.inputs["Outward"])
    links.new(align_rotation_to_vector_001.outputs[0], alignment.inputs["Along path"])
    links.new(alignment.outputs["Output"], instance_on_points.inputs["Rotation"])
    
    links.new(instance_on_points.outputs["Instances"], transform_geometry.inputs["Geometry"])
    links.new(axis.outputs["Output"], transform_geometry.inputs["Rotation"])
    
    links.new(transform_geometry.outputs[0], realize_instances.inputs["Geometry"])
    links.new(realize_instances.outputs[0], group_output.inputs["Geometry"])
    
    return radial_array_1


class OBJECT_OT_add_radial_array(bpy.types.Operator):
    """Add a procedural Radial Array modifier"""
    bl_idname = "object.add_radial_array"
    bl_label = "Add Radial Array"
    bl_options = {'REGISTER', 'UNDO'}

    count: bpy.props.IntProperty(
        name="Count",
        description="Number of objects",
        default=10,
        min=3,
        max=1000
    )
    
    radius: bpy.props.FloatProperty(
        name="Radius",
        description="Distance from the center",
        default=2.0,
        min=0.0
    )

    axis: bpy.props.EnumProperty(
        name="Axis",
        description="Which axis to array around",
        items=[
            ('X', "X", "Rotate around X"),
            ('Y', "Y", "Rotate around Y"),
            ('Z', "Z", "Rotate around Z")
        ],
        default='Z'
    )

    alignment: bpy.props.EnumProperty(
        name="Alignment",
        description="How the objects face",
        items=[
            ('Outward', "Outward", "Objects face away from center"),
            ('Along path', "Along path", "Objects follow the circle direction")
        ],
        default='Along path'
    )

    spin_offset: bpy.props.FloatProperty(
        name="Spin Offset",
        description="Rotate the entire array",
        default=0.0,
        subtype='ANGLE'
    )

    @classmethod
    def poll(cls, context):
        obj = context.active_object
        return obj is not None and obj.select_get() and obj.type == 'MESH'

    def execute(self, context):
        obj = context.active_object
        
        node_tree = get_or_create_radial_array_node_group()
        
        mod = obj.modifiers.new(name="Radial Array", type='NODES')
        mod.node_group = node_tree
        
        axis_index = {'X': 0, 'Y': 1, 'Z': 2}
        alignment_index = {'Outward': 0, 'Along path': 1}
        
        for item in node_tree.interface.items_tree:
            if item.item_type == 'SOCKET':
                if item.name == "Count":
                    mod[item.identifier] = self.count
                elif item.name == "Radius":
                    mod[item.identifier] = self.radius
                elif item.name == "Spin Offset":
                    mod[item.identifier] = self.spin_offset
                elif item.name == "Axis":
                    mod[item.identifier] = axis_index[self.axis]
                elif item.name == "Alignment":
                    mod[item.identifier] = alignment_index[self.alignment]
        
        return {'FINISHED'}


def menu_func(self, context):
    obj = context.active_object
    if obj and obj.select_get() and obj.type == 'MESH':
        self.layout.separator()
        self.layout.operator(OBJECT_OT_add_radial_array.bl_idname, icon='MOD_ARRAY')

def register():
    bpy.utils.register_class(OBJECT_OT_add_radial_array)
    bpy.types.VIEW3D_MT_object_context_menu.append(menu_func)

def unregister():
    bpy.utils.unregister_class(OBJECT_OT_add_radial_array)
    bpy.types.VIEW3D_MT_object_context_menu.remove(menu_func)

if __name__ == "__main__":
    target_menu = bpy.types.VIEW3D_MT_object_context_menu
    draw_funcs = getattr(target_menu.draw, "_draw_funcs", [])
    
    for f in list(draw_funcs):
        module_name = getattr(f, "__module__", "")
        if module_name == "__main__":
            target_menu.remove(f)
    
    if "Radial Array" in bpy.data.node_groups:
        node_tree = bpy.data.node_groups["Radial Array"]
        
        for obj in bpy.data.objects:
            for mod in obj.modifiers:
                if mod.type == 'NODES' and mod.node_group == node_tree:
                    mod.node_group = None
                    obj.modifiers.remove(mod)
        bpy.data.node_groups.remove(node_tree)
    
    try:
        unregister()
    except Exception as e:
        print(f"Nothing to unregister yet: {e}")
        
    register()