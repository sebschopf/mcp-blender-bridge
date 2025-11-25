import logging

import bpy

logger = logging.getLogger(__name__)


def get_operator_rna(tool_name: str):
    """Maps a tool name (e.g., 'bpy.ops.mesh.primitive_cube_add') to its RNA type.
    """
    try:
        # Expected format: bpy.ops.module.operator_name
        parts = tool_name.split(".")
        if len(parts) < 3 or parts[0] != "bpy" or parts[1] != "ops":
            print(f"DEBUG: Invalid format for {tool_name}")
            return None

        module_name = parts[2]
        op_name = parts[3]

        # Method 1: Try direct access via bpy.ops (works for C-defined ops sometimes)
        try:
            module = getattr(bpy.ops, module_name)
            op_func = getattr(module, op_name)
            if hasattr(op_func, "get_rna_type"):
                print(f"DEBUG: Found get_rna_type on {tool_name}")
                return op_func.get_rna_type()
        except AttributeError:
            pass

        # Method 2: Standard Class Mapping mapping rule: mesh.primitive_cube_add -> MESH_OT_primitive_cube_add
        rna_name = f"{module_name.upper()}_OT_{op_name}"
        print(f"DEBUG: Trying to resolve RNA via class: {rna_name}")

        op_class = getattr(bpy.types, rna_name, None)
        if op_class:
            return op_class.bl_rna

        print(f"DEBUG: Could not find {rna_name} in bpy.types")
        return None
    except Exception as e:
        logger.error(f"Error resolving RNA for {tool_name}: {e}")
        return None


def extract_properties(tool_name: str):
    """Extracts relevant properties for a given tool name.
    Returns a dictionary with name, description, and properties list.
    """
    rna = get_operator_rna(tool_name)
    if not rna:
        return None

    properties = []

    # Properties to ignore
    ignore_props = {
        "rna_type",
        "name",
        "properties",
        "has_reports",
        "layout",
        "options",
        "macros",
        "bl_idname",
        "bl_label",
        "bl_description",
        "bl_translation_context",
        "bl_undo_group",
        "bl_options",
        "bl_cursor_pending",
    }

    for prop in rna.properties:
        if prop.identifier in ignore_props or prop.is_hidden:
            continue

        prop_info = {
            "identifier": prop.identifier,
            "name": prop.name,
            "description": prop.description,
            "type": prop.type,
        }

        # Try to get default value (can be tricky for some types)
        # We skip complex types for now to keep JSON simple

        properties.append(prop_info)

    return {"name": rna.name, "description": rna.description, "properties": properties}
