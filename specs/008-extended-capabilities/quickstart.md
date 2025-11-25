# Quickstart: Extended Capabilities

This feature massively expands the MCP's vocabulary, giving the AI a wide range of new tools to work with.

## 1. New Capabilities Overview

The AI can now perform actions in several new categories:

### Modeling
-   Create **Cylinders**, **Planes**, and **Toruses (donuts)**.

### Transformation
-   **Rotate** objects around a specific axis (X, Y, or Z).
-   **Resize** (scale) objects along different axes.

### Scene Management
-   **Select** or **Deselect** all objects.
-   **Duplicate** existing objects.
-   **Delete** selected objects.

### Modifiers
-   Add **Modifiers** to objects, such as `SUBSURF` (to smooth) or `BEVEL` (to round edges). Note that this only adds the modifier with its default settings for now.

### Staging
-   Add **Lights** (`POINT`, `SUN`, `SPOT`) to the scene.
-   Add **Cameras** to the scene.

## 2. Example Prompts

You can now chain these commands for much more complex requests:

-   **"Create a flat plane for the floor, then add a cylinder on top of it. Rotate the cylinder 45 degrees on the X axis."**
    -   *Expected ActionPlan*:
        1.  `bpy.ops.mesh.primitive_plane_add(size=5)`
        2.  `bpy.ops.mesh.primitive_cylinder_add(location=(0, 0, 1))`
        3.  `bpy.ops.transform.rotate(value=0.785, orient_axis='X')`

-   **"Create a cube, duplicate it, and move the new one to the right."**
    -   *Expected ActionPlan*:
        1.  `bpy.ops.mesh.primitive_cube_add()`
        2.  `bpy.ops.object.duplicate()`
        3.  `bpy.ops.transform.translate(value=(2, 0, 0))`

-   **"Add a light above the default cube."**
    -   *Expected ActionPlan*:
        1.  `bpy.ops.object.light_add(type='POINT', location=(0, 0, 5))`

## 3. How to Use

Simply describe what you want to achieve. The AI will now have a much richer set of tools to choose from to build an `ActionPlan` that matches your request.
