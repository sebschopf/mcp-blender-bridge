# Research Log: Boolean Operations

## 1. `bpy` API for Object Selection and Boolean Modifiers

### Decision

The process for applying a boolean operation via script is as follows:
1.  Ensure no objects are selected.
2.  Select the primary object (the one to be modified) by name and make it the active object.
3.  Add a `BOOLEAN` modifier to the active object.
4.  Set the modifier's `object` property to the target object (the "cutter" or "welder").
5.  Set the modifier's `operation` property (`'UNION'`, `'DIFFERENCE'`, `'INTERSECT'`).
6.  Apply the modifier.
7.  (Optional but recommended) Delete the target object.

### Rationale

This sequence is the most robust and mirrors the manual user workflow in Blender, ensuring predictable results. Direct calls to `bpy.ops.object.bool_operation` are less flexible for scripting purposes.

### Key `bpy` Snippets

-   **Select by Name**:
    ```python
    import bpy
    bpy.ops.object.select_all(action='DESELECT')
    obj = bpy.data.objects.get("ObjectName")
    if obj:
        obj.select_set(True)
        bpy.context.view_layer.objects.active = obj
    ```

-   **Apply Boolean Modifier**:
    ```python
    import bpy
    # Assumes primary object is active and selected
    target_obj = bpy.data.objects.get("TargetObjectName")
    if target_obj:
        mod = bpy.context.object.modifiers.new(name="Boolean", type='BOOLEAN')
        mod.object = target_obj
        mod.operation = 'DIFFERENCE' # Or 'UNION', 'INTERSECT'
        bpy.ops.object.modifier_apply(modifier=mod.name)
        # Clean up the target object
        bpy.data.objects.remove(target_obj, do_unlink=True)
    ```

## 2. Implementation Strategy

### Decision

As with the material tools, this complex, multi-step logic will be encapsulated in helper functions in `bpy_utils.py`. We will create a single, powerful helper script template for `object.apply_boolean` that performs the entire sequence. We will also add a simple `object.select_by_name` tool.

### Rationale

This maintains the abstraction layer between the AI and the complexities of the `bpy` API, adhering to the "Granular & Secure Tools" principle. The AI can simply state its intent ("apply boolean"), and the Controller handles the detailed execution.
