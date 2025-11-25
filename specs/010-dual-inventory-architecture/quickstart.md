# Quickstart: Dual Inventory Architecture

This guide explains how developers can add new capabilities and recipes to the Controller under the Dual Inventory Architecture.

## 1. Adding a New Granular Tool

To add a new, atomic Blender capability (a "Tool"), follow these steps.

**Goal**: Add a `mesh.subdivide` tool.

1.  **Locate or Create the Right File**:
    -   Navigate to the `controller/capabilities/` directory.
    -   The logical place for a mesh editing tool is `mesh/editing.yaml`. If this file or the `mesh` directory doesn't exist, create it.

2.  **Add the Tool Definition**:
    -   Open `controller/capabilities/mesh/editing.yaml`.
    -   Add the new tool definition to the list of tools under the appropriate category.

    ```yaml
    editing:
      description: "Tools for modifying mesh geometry."
      tools:
        # ... other tools like extrude, inset ...
        - name: "mesh.subdivide"
          description: "Subdivides selected faces of the active object."
          params:
            cuts:
              type: "int"
              description: "The number of subdivisions."
              default: 1
    ```

3.  **Implement the Logic**:
    -   Open `controller/app/bpy_utils.py`.
    -   Add a new entry in the `SCRIPT_PALETTE` dictionary that corresponds to the tool's name (`mesh.subdivide`).
    -   The script should expect a dictionary of parameters (`params`) which will contain the `cuts` value.

    ```python
    # In bpy_utils.py
    SCRIPT_PALETTE = {
        # ... other scripts ...
        "mesh.subdivide": """
    bpy.ops.object.mode_set(mode='EDIT')
    bpy.ops.mesh.subdivide(number_cuts=params.get('cuts', 1))
    bpy.ops.object.mode_set(mode='OBJECT')
    """,
    }
    ```

4.  **Restart the Controller**:
    -   Upon restarting, the Knowledge Engine will automatically discover, load, and validate the new tool, making it immediately available to the AI.

## 2. Adding a New Recipe

To add a new, high-level "Recipe" for creating a complex object, follow these steps.

**Goal**: Add a recipe for a simple table.

1.  **Create the Recipe File**:
    -   Navigate to the `controller/knowledge_base/` directory.
    -   Create a new file in a logical path, for example: `furniture/tables/simple_table.yaml`.

2.  **Define the Recipe**:
    -   Open the new file and define the recipe's metadata, parameters, and steps. The steps are a sequence of calls to the granular tools defined in the `capabilities/` inventory.

    ```yaml
    name: "Simple Wooden Table"
    category: "furniture/tables"
    version: "1.0"
    tags: ["furniture", "table", "wood"]
    description: "Creates a simple four-legged table with a rectangular top."

    parameters:
      - name: "table_width"
        type: "float"
        default: 1.5
      - name: "table_depth"
        type: "float"
        default: 0.8

    steps:
      - operation: "mesh.create_cube"
        params:
          name: "TableTop"
      - operation: "transform.resize"
        params:
          object_name: "TableTop"
          value: ["{{ table_width }}", "{{ table_depth }}", 0.05]
      # ... more steps for the four legs using create_cube, resize, and translate
    ```

3.  **Restart the Controller**:
    -   The Knowledge Engine will discover and validate the new recipe on startup. The AI will now be able to find it using `knowledge.search_recipes` and execute it with `knowledge.execute_recipe`.
