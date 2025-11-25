# Quickstart: YAML Capabilities Management

This feature refactors how the Controller's capabilities are defined, moving them from a Python dictionary to a structured YAML file for better maintainability and clarity.

## 1. The `capabilities.yaml` File

The source of truth for all available tools is now located at `controller/config/capabilities.yaml`. This file is human-readable and organized by category.

### Example:
```yaml
# controller/config/capabilities.yaml

modeling:
  description: "Tools for creating new primitive geometries."
  tools:
    - name: "bpy.ops.mesh.primitive_cube_add"
      description: "Adds a cube to the scene."
      params:
        size:
          type: "float"
          description: "The size of the cube."
          default: 1.0
```

## 2. Adding a New Tool

To extend the MCP's capabilities, simply edit the `capabilities.yaml` file:

1.  Find the appropriate category (e.g., `modeling`, `transform`) or create a new one.
2.  Add a new entry to the `tools` list for that category.
3.  Define the `name` (the `bpy` operation), a `description`, and any `params` it accepts.
4.  Restart the Controller. The new tool will be automatically loaded, validated, and made available through the `/api/mcp/capabilities` endpoint.

## 3. New Dependency

This feature adds a new dependency to the Controller:
-   `PyYAML`: Used for parsing the YAML file.

Ensure it is installed by running `uv pip install -r controller/requirements.txt`.