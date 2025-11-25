# Research Log: Basic Material Capabilities

## 1. `bpy` API for Material Manipulation

### Decision

Modern Blender materials (for Eevee and Cycles) are node-based. Direct property access (`material.diffuse_color`) is a legacy feature for the old Blender Internal renderer and should not be used. All material properties, such as color, metallic, and roughness, are inputs on the "Principled BSDF" shader node, which is the default node in a new material.

The correct way to modify these properties is to access the material's node tree, find the "Principled BSDF" node, and set the default value of its inputs.

### Rationale

Using the node-based API is the only way to guarantee compatibility with modern Blender workflows and renderers. It is the standard, officially supported method.

### Key `bpy` Snippets

-   **Get or Create Material**:
    ```python
    import bpy
    def get_or_create_material(name):
        if name in bpy.data.materials:
            return bpy.data.materials[name]
        else:
            return bpy.data.materials.new(name=name)
    ```

-   **Assign Material to Active Object**:
    ```python
    obj = bpy.context.active_object
    if not obj.material_slots:
        obj.data.materials.append(None) # Add a slot if none exist
    obj.material_slots[0].material = material
    ```

-   **Set Principled BSDF Properties**:
    ```python
    material.use_nodes = True
    principled_bsdf = material.node_tree.nodes.get("Principled BSDF")
    if principled_bsdf:
        # Set Base Color (takes a 4-tuple RGBA)
        principled_bsdf.inputs["Base Color"].default_value = (r, g, b, 1.0)
        # Set Metallic (float 0.0 to 1.0)
        principled_bsdf.inputs["Metallic"].default_value = value
        # Set Roughness (float 0.0 to 1.0)
        principled_bsdf.inputs["Roughness"].default_value = value
    ```

## 2. Implementation Strategy

### Decision

Directly exposing these multi-line `bpy` snippets as capabilities is not feasible. Instead, we will create a small set of helper functions within the Controller (e.g., in a new `controller/app/bpy_helpers.py` module). These helper functions will then be exposed as single-line, granular tools in the `capabilities.yaml` file.

For example, we will create a helper `materials.set_base_color(color: tuple)` and expose it in the YAML as a tool named `materials.set_base_color`.

### Rationale

This approach maintains the "Granular & Secure Tools" principle. The AI calls a simple, validated function, and the Controller executes the more complex, multi-line `bpy` logic. This abstracts the complexity of the node system from the AI.
