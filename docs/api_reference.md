# MCP Blender API Reference

This document provides a reference for the schemas and protocols used in the MCP Blender project.

## Controller Endpoints

The Controller exposes a standard MCP interface via SSE (Server-Sent Events) or Stdio, but also provides specific HTTP endpoints for the Blender Addon bridge.

### Bridge Endpoints

*   **`GET /api/bridge/commands`**
    *   **Description**: Long-polling endpoint for the Blender Addon to fetch pending commands.
    *   **Returns**: JSON object containing the command (if any) or a timeout message.
    *   **Response Schema**:
        ```json
        {
          "command": "mesh.create_cube",
          "params": { "size": 2.0 },
          "id": "unique_command_id"
        }
        ```

*   **`POST /api/bridge/feedback`**
    *   **Description**: Endpoint for the Blender Addon to report the result of a command execution.
    *   **Payload**:
        ```json
        {
          "command_id": "unique_command_id",
          "status": "success", // or "error"
          "data": { ... }, // Optional result data
          "error": "Error message" // If status is error
        }
        ```

## Tool Definition Schema

Tools (Capabilities) are defined in YAML files.

### Schema

```yaml
category_name:
  description: string
  tools:
    - name: string
      description: string
      params:
        param_name:
          type: string (string, float, int, bool, list, dict)
          description: string
          required: boolean
          default: any
```

### Example

```yaml
mesh_tools:
  description: "Tools for creating and modifying meshes."
  tools:
    - name: "mesh.create_cube"
      description: "Creates a new cube mesh."
      params:
        size:
          type: "float"
          description: "Length of the cube's sides."
          required: true
          default: 2.0
```

## Recipe Definition Schema

Recipes (Knowledge Base) are defined in YAML files.

### Schema

```yaml
name: string
category: string
version: string
tags: [string]
description: string
parameters:
  - name: string
    type: string
    description: string
    default: any
steps:
  - operation: string (tool name)
    params:
      param_name: value (or "{{ recipe_param }}")
```

### Example

```yaml
name: "Simple Table"
category: "furniture/tables"
version: "1.0"
description: "Creates a simple four-legged table."
parameters:
  - name: "width"
    type: "float"
    description: "Width of the table top."
    default: 2.0
steps:
  - operation: "mesh.create_cube"
    params:
      size: "{{ width }}"
      location: [0, 0, 1]
```
