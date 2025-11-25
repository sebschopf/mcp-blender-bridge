# Quickstart: Dynamic Command Generation

This guide provides developers with the necessary information to interact with the new dynamic command generation capabilities of the MCP system.

## 1. Discovering Capabilities

Before generating a plan, the AI must understand what operations are available. This is done by querying the `/api/mcp/capabilities` endpoint.

### Request

```bash
curl -X GET http://127.0.0.1:8000/api/mcp/capabilities
```

### Response

The response will be a JSON object (the "Capability Palette") detailing the allowed `bpy` operations and their parameters.

```json
{
  "bpy.ops.mesh.primitive_uv_sphere_add": {
    "radius": { "type": "float", "required": false, "default": 1.0 },
    "location": { "type": "tuple", "required": false, "default": [0, 0, 0] }
  },
  "bpy.ops.transform.translate": {
    "value": { "type": "tuple", "required": true }
  }
}
```

## 2. Executing an Action Plan

Once the AI has formulated a plan based on the available capabilities, it sends it to the `/api/chat` endpoint for execution.

### Request Body

The request is a JSON object containing the user's original prompt and the `action_plan`.

```json
{
  "prompt": "build a snowman",
  "action_plan": [
    {
      "operation": "bpy.ops.mesh.primitive_uv_sphere_add",
      "params": { "radius": 1.0, "location": [0, 0, 1] }
    },
    {
      "operation": "bpy.ops.mesh.primitive_uv_sphere_add",
      "params": { "radius": 0.5, "location": [0, 0, 2.5] }
    }
  ]
}
```

### Request with `curl`

```bash
curl -X POST http://127.0.0.1:8000/api/chat \
-H "Content-Type: application/json" \
-d 
{
  "prompt": "build a snowman",
  "action_plan": [
    {
      "operation": "bpy.ops.mesh.primitive_uv_sphere_add",
      "params": { "radius": 1.0, "location": [0, 0, 1] }
    },
    {
      "operation": "bpy.ops.mesh.primitive_uv_sphere_add",
      "params": { "radius": 0.5, "location": [0, 0, 2.5] }
    }
  ]
}
```

### Response

The controller will respond with status updates as it executes the plan. For example, a final successful response might look like this:

```json
{
  "message": "I have successfully built the snowman for you.",
  "commands": [],
  "status": "COMPLETED"
}
```

