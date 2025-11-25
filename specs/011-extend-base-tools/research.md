# Research: Extend Base Modeling Tools

**Objective**: Resolve the key unknowns identified in the implementation plan to ensure a clear and robust strategy for translating Blender's complex modeling tools into the YAML-based capability format.

## 1. Mapping UI Tools to `bpy.ops`

-   **Unknown**: What is the definitive mapping between Blender's UI-based tools (e.g., "Loop Cut and Slide") and their corresponding `bpy.ops` functions and parameters?
-   **Research Task**: "Investigate methods for discovering `bpy.ops` equivalents for Blender's UI modeling tools."

### Investigation & Findings

-   **Blender's Python Tooltips**: The most reliable method is to enable "Python Tooltips" in Blender's preferences (Interface -> Display). When you hover over any button or tool in the UI, the tooltip will display the exact `bpy.ops` command.
-   **Blender's Info Panel**: The Info panel can be dragged open and set to display reports. It logs all operations as `bpy` commands, providing a live history of actions that can be copied and analyzed.
-   **Blender Manual vs. API Docs**: The user-facing manual (which was provided) describes the *function* of a tool, while the `bpy` API documentation describes the *parameters* of the Python function. Both are needed. The manual provides the "what" and "why", and the API docs provide the "how".

### Decision

-   The primary method for mapping tools will be to use Blender's **Python Tooltips** and **Info Panel** to identify the correct `bpy.ops` function for each desired modeling tool.
-   The `description` field of each tool in the YAML file will be based on the Blender Manual to ensure it's user-friendly for the AI.
-   The `params` for each tool will be derived directly from the `bpy` API documentation for that function.

## 2. Representing Stateful Sculpting Brushes

-   **Unknown**: What is the best practice for representing sculpting brushes, which are stateful tools, within our stateless `Tool` model?
-   **Research Task**: "Determine a pattern for defining and using sculpting brushes as granular, stateless tools."

### Investigation & Findings

-   Sculpting in Blender involves two main steps: (1) entering Sculpt Mode, and (2) using a brush tool. The brush itself is a setting on the active tool.
-   The `bpy.ops.sculpt.brush_stroke` operator is the key function. It can be configured with a `stroke` parameter that defines the path of the brush, but for a simple, single "dab", it can be called with a minimal configuration.
-   The active brush can be set via `bpy.context.tool_settings.sculpt.brush`.

### Decision

-   We will not represent each brush as a separate tool. Instead, we will create a single, more powerful `sculpt.apply_brush` tool.
-   This tool will have parameters for:
    -   `brush_name`: The name of the brush to activate (e.g., 'Draw', 'Clay', 'Grab').
    -   `location`: The 3D coordinate where the brush stroke should be applied.
    -   `size`, `strength`, etc.: Common brush parameters.
-   The underlying script for this tool will be more complex: it will switch to Sculpt Mode, set the active brush and its parameters, perform a single brush stroke at the specified location, and then switch back to Object Mode. This encapsulates the stateful nature of sculpting into a single, stateless, granular tool, fitting our existing model perfectly.

## 3. Handling Complex Modifier Properties

-   **Unknown**: How should complex modifier properties (e.g., curve objects for the Curve modifier) be represented as simple, serializable parameters in YAML?
-   **Research Task**: "Design a YAML-compatible parameter format for modifier properties that reference other scene objects."

### Investigation & Findings

-   Many modifiers (`Curve`, `Boolean`, `Array`) require a reference to another object in the scene (e.g., the curve to deform along, the object to subtract).
-   The `bpy` API assigns these by passing the `Object` reference itself (e.g., `modifier.object = bpy.data.objects['MyCurve']`).
-   Our `Tool` model only supports simple JSON/YAML-serializable types (string, int, float, bool, list, dict). We cannot pass a live Python object reference.

### Decision

-   For any modifier parameter that requires a reference to another object, the parameter type in the YAML file will be defined as `string`.
-   The `description` for this parameter will explicitly state that it expects the **name** of the target object.
-   The underlying helper script that implements the modifier tool (e.g., a new `object.apply_curve_modifier` tool) will be responsible for taking this name and looking up the actual Blender object reference using `bpy.data.objects.get(object_name)`.
-   This approach keeps the YAML definition simple and serializable, while the implementation handles the logic of resolving the object reference at execution time. For example:
    ```yaml
    - name: "object.apply_curve_modifier"
      description: "Deforms the active object along a curve."
      params:
        curve_object_name:
          type: "string"
          description: "The name of the Curve object to use for deformation."
          required: true
    ```
