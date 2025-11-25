# Data Model: MCP Migration

## 1. Core Entities

### 1.1 MCP Tool Mapping
Existing "Capabilities" (Action Plan tools) are mapped to MCP Tools.

| Concept | Old | New (MCP) |
| :--- | :--- | :--- |
| **Identity** | `InternalTool` (Pydantic) | `mcp.types.Tool` |
| **Input** | `ActionPlan` (JSON) | `mcp.types.CallToolRequest.arguments` |
| **Output** | `ExecutionResult` | `mcp.types.CallToolResult` |

### 1.2 Bridge Protocol (Controller <-> Addon)
Data structures used for the internal long-polling bridge.

#### BridgeCommand
Sent from Controller to Addon.

```json
{
  "id": "uuid-v4",
  "type": "execute_script" | "get_state",
  "payload": {
    "script": "bpy.ops.mesh.primitive_cube_add()",
    "context": {}
  }
}
```

#### BridgeResult
Sent from Addon to Controller.

```json
{
  "command_id": "uuid-v4",
  "status": "success" | "error",
  "data": {
    "output": "Created Cube",
    "scene_state": { ... } // Optional, for get_state
  },
  "error_message": "..."
}
```

### 1.3 Resources

#### `blender://scene/objects`
JSON representation of the scene graph.

```json
[
  {
    "name": "Cube",
    "type": "MESH",
    "location": [0, 0, 0],
    "rotation": [0, 0, 0],
    "scale": [1, 1, 1],
    "visible": true
  }
]
```

## 2. State Management

### 2.1 Pending Command Queue
In-Memory Queue in Controller.
- **Push**: When MCP `call_tool` is invoked.
- **Pop**: When Addon `POST /internal/get_command` connects.

### 2.2 Pending Result Map
In-Memory Map in Controller (`dict[command_id, Future]`).
- **Set**: When command is pushed to queue (create a Future).
- **Resolve**: When Addon `POST /internal/post_result` arrives.
