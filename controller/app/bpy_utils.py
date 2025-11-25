# controller/app/bpy_utils.py
"""This module contains helper functions that generate complex, multi-line
bpy script snippets. This abstracts the complexity of Blender's API
from the core command generation logic.
"""

from typing import Dict


def get_bpy_script_snippets() -> Dict[str, str]:
    """Returns a dictionary of script templates for complex operations."""
    return {
        # --- Material Snippets ---
        "materials.create_and_assign": """
import bpy
material_name = "{material_name}"
if material_name in bpy.data.materials:
    mat = bpy.data.materials[material_name]
else:
    mat = bpy.data.materials.new(name=material_name)
    mat.use_nodes = True
obj = bpy.context.active_object
if not obj.material_slots:
    obj.data.materials.append(None)
obj.material_slots[0].material = mat
""",
        "materials.set_base_color": """
import bpy
obj = bpy.context.active_object
mat = obj.material_slots[0].material
if mat and mat.use_nodes:
    p_bsdf = mat.node_tree.nodes.get("Principled BSDF")
    if p_bsdf:
        p_bsdf.inputs["Base Color"].default_value = {color}
""",
        "materials.set_metallic": """
import bpy
obj = bpy.context.active_object
mat = obj.material_slots[0].material
if mat and mat.use_nodes:
    p_bsdf = mat.node_tree.nodes.get("Principled BSDF")
    if p_bsdf:
        p_bsdf.inputs["Metallic"].default_value = {value}
""",
        "materials.set_roughness": """
import bpy
obj = bpy.context.active_object
mat = obj.material_slots[0].material
if mat and mat.use_nodes:
    p_bsdf = mat.node_tree.nodes.get("Principled BSDF")
    if p_bsdf:
        p_bsdf.inputs["Roughness"].default_value = {value}
""",
        # --- Boolean and Selection Snippets ---
        "object.select_by_name": """
import bpy
bpy.ops.object.select_all(action='DESELECT')
obj = bpy.data.objects.get("{object_name}")
if obj:
    obj.select_set(True)
    bpy.context.view_layer.objects.active = obj
""",
        "object.apply_boolean": """
import bpy
target_obj = bpy.data.objects.get("{target_object_name}")
if target_obj and bpy.context.active_object:
    mod = bpy.context.object.modifiers.new(name="Boolean", type='BOOLEAN')
    mod.object = target_obj
    mod.operation = '{operation}'
    bpy.ops.object.modifier_apply(modifier=mod.name)
    bpy.data.objects.remove(target_obj, do_unlink=True)
""",
        "object.rename": """
import bpy
if bpy.context.active_object:
    bpy.context.active_object.name = "{new_name}"
""",
        "object.apply_bevel": """
import bpy
if bpy.context.active_object:
    mod = bpy.context.object.modifiers.new(name="Bevel", type='BEVEL')
    mod.width = {width}
    mod.segments = {segments}
    bpy.ops.object.modifier_apply(modifier=mod.name)
""",
        "object.apply_subsurf": """
import bpy
if bpy.context.active_object:
    mod = bpy.context.object.modifiers.new(name="Subdivision", type='SUBSURF')
    mod.levels = {levels}
    bpy.ops.object.modifier_apply(modifier=mod.name)
""",
        "object.select_multiple": """
import bpy
bpy.ops.object.select_all(action='DESELECT')
for obj_name in {object_names}:
    obj = bpy.data.objects.get(obj_name)
    if obj:
        obj.select_set(True)
        bpy.context.view_layer.objects.active = obj
""",
        "object.join": """
import bpy
if len(bpy.context.selected_objects) > 1:
    bpy.ops.object.join()
""",
        # --- Sculpting Snippets ---
        "sculpt.apply_brush": """
import bpy
from bpy_extras.view3d_utils import region_2d_to_vector_3d, region_2d_to_origin_3d
# Ensure we are in object mode and have an active object
if bpy.context.active_object and bpy.context.active_object.mode != 'OBJECT':
    bpy.ops.object.mode_set(mode='OBJECT')
if bpy.context.active_object and bpy.context.active_object.type == 'MESH':
    # Go into sculpt mode
    bpy.ops.object.mode_set(mode='SCULPT')
    # Set the brush
    bpy.context.tool_settings.sculpt.brush = bpy.data.brushes.get("{brush_name}")
    brush = bpy.context.tool_settings.sculpt.brush
    if brush:
        if {size} is not None:
            brush.size = {size}
        if {strength} is not None:
            brush.strength = {strength}
    
    # This is a simplified stroke. A real implementation is more complex.
    # We simulate a single "dab" at the object's origin for now.
    override = bpy.context.copy()
    override['area'] = next(area for area in bpy.context.screen.areas if area.type == 'VIEW_3D')
    override['region'] = next(region for region in override['area'].regions if region.type == 'WINDOW')
    
    bpy.ops.sculpt.brush_stroke(override, stroke=[{{'name': '', 'pen_flip': False, 'is_start': True, 'location': (0, 0, 0), 'mouse': (override['region'].width // 2, override['region'].height // 2), 'pressure': 1.0, 'size': brush.size, 'time': 0.0}}])
    
    # Return to object mode
    bpy.ops.object.mode_set(mode='OBJECT')
""",
        # --- Retopology Snippets ---
        "mesh.retopology.create_quads": """
import bpy
if bpy.context.active_object:
    mod = bpy.context.object.modifiers.new(name="Remesh", type='REMESH')
    mod.mode = 'VOXEL'
    if {voxel_size} is not None:
        mod.voxel_size = {voxel_size}
    bpy.ops.object.modifier_apply(modifier=mod.name)
""",
        # --- Modifier Snippets ---
        "modifiers.add_array": """
import bpy
if bpy.context.active_object:
    mod = bpy.context.object.modifiers.new(name="Array", type='ARRAY')
    mod.count = {count}
    if {relative_offset} is not None:
        mod.relative_offset_displace = {relative_offset}
""",
        "modifiers.add_bevel": """
import bpy
if bpy.context.active_object:
    mod = bpy.context.object.modifiers.new(name="Bevel", type='BEVEL')
    mod.width = {width}
    mod.segments = {segments}
""",
        "modifiers.add_boolean": """
import bpy
target_obj = bpy.data.objects.get("{target_object_name}")
if target_obj and bpy.context.active_object:
    mod = bpy.context.object.modifiers.new(name="Boolean", type='BOOLEAN')
    mod.object = target_obj
    mod.operation = '{operation}'
""",
        "modifiers.add_solidify": """
import bpy
if bpy.context.active_object:
    mod = bpy.context.object.modifiers.new(name="Solidify", type='SOLIDIFY')
    mod.thickness = {thickness}
""",
        "modifiers.add_curve": """
import bpy
curve_obj = bpy.data.objects.get("{curve_object_name}")
if curve_obj and bpy.context.active_object:
    mod = bpy.context.object.modifiers.new(name="Curve", type='CURVE')
    mod.object = curve_obj
""",
        "modifiers.add_wave": """
import bpy
if bpy.context.active_object:
    mod = bpy.context.object.modifiers.new(name="Wave", type='WAVE')
    mod.height = {height}
    mod.width = {width}
""",
        "modifiers.add_simple_deform": """
import bpy
if bpy.context.active_object:
    mod = bpy.context.object.modifiers.new(name="SimpleDeform", type='SIMPLE_DEFORM')
    mod.deform_method = '{deform_method}'
    mod.angle = {angle} * (3.14159 / 180.0) # Convert to radians
""",
    }
