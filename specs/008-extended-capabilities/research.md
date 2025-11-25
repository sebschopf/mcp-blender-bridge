# Research Log: Extended Capabilities

## 1. `bpy.ops` Command Identification

The following `bpy.ops` commands have been identified as the most suitable for extending the AI's capabilities across the desired domains.

### Modeling Primitives

-   `bpy.ops.mesh.primitive_cylinder_add`: `vertices`, `radius`, `depth`, `location`
-   `bpy.ops.mesh.primitive_plane_add`: `size`, `location`
-   `bpy.ops.mesh.primitive_torus_add`: `major_radius`, `minor_radius`, `location`

### Transformations

-   `bpy.ops.transform.rotate`: `value` (angle in radians), `orient_axis` (e.g., 'Z')
-   `bpy.ops.transform.resize`: `value` (scale factor as a tuple `(x, y, z)`)

### Scene Management

-   `bpy.ops.object.select_all`: `action` ('SELECT', 'DESELECT', 'INVERT', 'TOGGLE')
-   `bpy.ops.object.duplicate()`: No parameters needed for a simple duplicate.
-   `bpy.ops.object.delete()`: `use_global` (boolean)

### Modifiers

Modifiers are complex as they are added and then configured. The best approach is to expose a single tool to add the modifier by type, and then subsequent tools to configure the properties of the *last added* modifier.

-   `bpy.ops.object.modifier_add`: `type` (e.g., 'SUBSURF', 'BEVEL')
-   **Helper Tool Idea**: `modifier.set_property`
    -   This would be a custom helper function.
    -   `params`: `property_name` (e.g., '"levels"'), `value`
    -   This is more advanced and might be deferred. For now, we will stick to direct `bpy.ops` and add modifiers with default settings.

### Staging

-   `bpy.ops.object.light_add`: `type` ('POINT', 'SUN', 'SPOT'), `location`
-   `bpy.ops.object.camera_add`: `location`, `rotation`

## 2. Implementation Strategy

All of these commands can be added directly to the `capabilities.yaml` file. No new helper functions in Python are required for this phase, simplifying the implementation significantly. We will focus on adding the tools with their most important and easy-to-understand parameters.
