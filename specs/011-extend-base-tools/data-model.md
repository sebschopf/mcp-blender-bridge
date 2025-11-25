# Data Model: Extend Base Modeling Tools

This feature does not introduce any new Pydantic models or change the existing data schemas. It focuses on expanding the *content* within the existing `capabilities/` inventory.

The primary entities involved are `Tool` and `ToolCategory`, which are already defined in `controller/app/models.py`.

## New Tool Categories

This feature will introduce the following new tool categories, which will be represented as new subdirectories and/or YAML files within the `controller/capabilities/` directory:

### 1. `mesh/editing`
-   **Description**: Contains tools for detailed mesh manipulation beyond simple primitive creation.
-   **Example Tools**: `mesh.extrude`, `mesh.inset`, `mesh.bevel`, `mesh.loop_cut`, `mesh.subdivide`.

### 2. `sculpt`
-   **Description**: Contains tools for organic modeling and sculpting.
-   **Example Tools**: `sculpt.apply_brush` (a generic tool to apply any brush by name), `sculpt.enter_mode`, `sculpt.exit_mode`.

### 3. `retopology`
-   **Description**: Tools for creating clean, low-polygon geometry over a high-polygon mesh.
-   **Example Tools**: `mesh.retopology.create_quads`.

### 4. `modifiers`
-   **Description**: A new, broad category for adding, configuring, and applying Blender's modifiers. This will likely be a directory containing multiple YAML files, such as:
    -   `modifiers/generate.yaml`: For modifiers that create geometry (e.g., Array, Bevel, Solidify).
    -   `modifiers/deform.yaml`: For modifiers that deform geometry (e.g., Curve, Wave, Simple Deform).
-   **Example Tools**: `object.modifier_add`, `object.modifier_apply`, and specific helper tools like `object.apply_curve_modifier` which handle more complex parameter mapping.

All new tools added under these categories will conform to the existing `Tool` schema.
