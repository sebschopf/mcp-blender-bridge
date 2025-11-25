# Data Model: Dynamic Command Generation

This document outlines the key data structures used for the dynamic command generation feature.

## 1. Capability Palette

The `CapabilityPalette` is a JSON object returned by the `/api/mcp/capabilities` endpoint. It defines the "palette" of safe, low-level `bpy` operations that the AI is allowed to use in an Action Plan.

-   **Type**: `JSON Object`
-   **Description**: The keys of the object are the string representations of the allowed `bpy` operations. The values are objects that describe the parameters for that operation.

### Example

```json
{
  "bpy.ops.mesh.primitive_uv_sphere_add": {
    "radius": {
      "type": "float",
      "required": false,
      "default": 1.0
    },
    "location": {
      "type": "tuple",
      "required": false,
      "default": [0, 0, 0]
    }
  },
  "bpy.ops.transform.translate": {
    "value": {
      "type": "tuple",
      "required": true
    }
  },
  "object.active.scale": {
      "value": {
          "type": "tuple",
          "required": true
      }
  }
}
```

## 2. Action Plan

The `ActionPlan` is a JSON array sent by the AI to the `/api/chat` endpoint for execution. It represents a sequence of operations to be performed in Blender.

-   **Type**: `JSON Array` of `Action Step` objects.

## 3. Action Step

An `ActionStep` is a single object within the `ActionPlan` array. It defines one operation to be executed.

-   **Type**: `JSON Object`
-   **Properties**:
    -   `operation` (string, required): The name of the operation to execute. This MUST be a key present in the `CapabilityPalette`.
    -   `params` (object, optional): A dictionary of parameters for the operation. The keys and value types must conform to the definition in the `CapabilityPalette`.

### Example `ActionPlan`

```json
[
  {
    "operation": "bpy.ops.mesh.primitive_uv_sphere_add",
    "params": {
      "radius": 1.0,
      "location": [0, 0, 1]
    }
  },
  {
    "operation": "bpy.ops.mesh.primitive_uv_sphere_add",
    "params": {
      "radius": 0.5,
      "location": [0, 0, 2.5]
    }
  },
  {
    "operation": "bpy.ops.transform.translate",
    "params": {
        "value": [0, 0, 1.5]
    }
  }
]
```
