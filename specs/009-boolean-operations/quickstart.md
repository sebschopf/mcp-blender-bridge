# Quickstart: Boolean Operations

This feature adds powerful modeling capabilities, allowing the AI to combine or carve objects using boolean operations.

## 1. New Capabilities

Two key tools have been added:

-   `object.select_by_name(object_name: str)`: Before you can modify an object, you often need to select it. The AI can now select any object by its name.
-   `object.apply_boolean(target_object_name: str, operation: str)`: This is the main tool. It modifies the *active* object using the *target* object.
    -   `operation`: Can be `'DIFFERENCE'` (carving), `'UNION'` (welding), or `'INTERSECT'`.

## 2. Example Prompts & Workflow

Boolean operations require a sequence of steps, which the AI can now formulate in an `ActionPlan`.

-   **"Create a cube named 'MyCube', then create a sphere named 'MySphere'. Move the sphere inside the cube, then use the sphere to carve a hole in the cube."**
    -   *Expected ActionPlan*:
        1.  `bpy.ops.mesh.primitive_cube_add()`
        2.  `bpy.context.active_object.name = 'MyCube'` (Note: A new `object.rename` tool might be useful in the future)
        3.  `bpy.ops.mesh.primitive_uv_sphere_add()`
        4.  `bpy.context.active_object.name = 'MySphere'`
        5.  `object.select_by_name(object_name='MySphere')`
        6.  `bpy.ops.transform.translate(value=(0, 0, 0))` (Assuming cube is also at origin)
        7.  `object.select_by_name(object_name='MyCube')`
        8.  `object.apply_boolean(target_object_name='MySphere', operation='DIFFERENCE')`

This demonstrates how the AI can now reason about multi-step modeling processes involving multiple objects.
