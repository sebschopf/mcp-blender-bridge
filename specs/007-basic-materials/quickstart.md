# Quickstart: Basic Material Capabilities

This feature extends the MCP's capabilities to allow for the manipulation of basic object materials.

## 1. New Capabilities

The following tools have been added to the `materials` category. You can now use them in your prompts.

-   `materials.create_and_assign(material_name: str)`: Creates a new material and assigns it to the active object.
-   `materials.set_base_color(color: tuple)`: Sets the material's base color (e.g., `[0.8, 0.2, 0.2, 1.0]`).
-   `materials.set_metallic(value: float)`: Sets the metallic property (0.0 to 1.0).
-   `materials.set_roughness(value: float)`: Sets the roughness property (0.0 to 1.0).

## 2. Example Prompts

You can now use natural language to describe the appearance of objects. The AI will translate these prompts into `ActionPlans` using the new tools.

-   **"Create a red metallic sphere"**
    -   *Expected ActionPlan*:
        1.  `bpy.ops.mesh.primitive_uv_sphere_add(...)`
        2.  `materials.create_and_assign(material_name="RedMetallic")`
        3.  `materials.set_base_color(color=[0.8, 0.0, 0.0, 1.0])`
        4.  `materials.set_metallic(value=1.0)`

-   **"Make the selected object look like rough blue plastic"**
    -   *Expected ActionPlan*:
        1.  `materials.create_and_assign(material_name="RoughBluePlastic")`
        2.  `materials.set_base_color(color=[0.1, 0.2, 0.8, 1.0])`
        3.  `materials.set_metallic(value=0.0)`
        4.  `materials.set_roughness(value=0.9)`

## 3. How it Works

These new "tools" are not direct `bpy` commands. They are helper functions defined in the Controller that execute the necessary multi-step logic to interact with Blender's modern, node-based shading system. This keeps the tools granular and secure, consistent with the project's constitution.
