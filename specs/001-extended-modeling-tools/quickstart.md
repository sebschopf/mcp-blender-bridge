# Quickstart: Extended Modeling Tools

This feature adds a suite of powerful tools for more advanced and organized modeling.

## 1. New Capabilities

### Object Management
-   `object.rename(new_name: str)`: Renames the active object.
-   `object.select_multiple(object_names: list)`: Selects a list of objects by name.
-   `object.join()`: Joins all selected objects into one.

### Modifiers
-   `object.apply_bevel(width: float, segments: int)`: Rounds the edges of the active object.
-   `object.apply_subsurf(levels: int)`: Smoothes the geometry of the active object.

## 2. Example Prompts & Workflows

### Renaming for Clarity
-   **"Create a sphere and rename it to 'planet_core'."**
    -   *Expected ActionPlan*:
        1.  `bpy.ops.mesh.primitive_uv_sphere_add()`
        2.  `object.rename(new_name='planet_core')`

### Creating a Smooth, Beveled Shape
-   **"Make a cube, smooth it out, and then bevel the edges."**
    -   *Expected ActionPlan*:
        1.  `bpy.ops.mesh.primitive_cube_add()`
        2.  `object.apply_subsurf(levels=2)`
        3.  `object.apply_bevel(width=0.05, segments=2)`

### Joining Multiple Objects
-   **"Create a cube named 'body' and a sphere named 'head'. Place the head on top of the body, then join them."**
    -   *Expected ActionPlan*:
        1.  `bpy.ops.mesh.primitive_cube_add()`
        2.  `object.rename(new_name='body')`
        3.  `bpy.ops.mesh.primitive_uv_sphere_add(location=(0, 0, 1.5))`
        4.  `object.rename(new_name='head')`
        5.  `object.select_multiple(object_names=['body', 'head'])`
        6.  `object.join()`
