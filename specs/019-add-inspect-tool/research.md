# Research: Tool Introspection & Recipe Saving

## 1. Unknowns & Clarifications

### 1.1 Runtime Introspection in Blender
- **Question**: How exactly do we get `bl_rna` properties from an operator name (string) in Python/Blender?
- **Finding**: 
    - We can map `bpy.ops.mesh.primitive_cube_add` -> `MESH_OT_primitive_cube_add`.
    - Then use `getattr(bpy.types, "MESH_OT_primitive_cube_add").bl_rna`.
    - The properties are in `bl_rna.properties`.
    - **Constraint**: Some operators are dynamic or context-sensitive and might not show all props via static RNA inspection. But for `primitive_*` operators, it works well.
- **Decision**: Use `bl_rna` introspection in a dedicated handler in the Blender Addon.

### 1.2 Recipe Saving
- **Question**: Where to save recipes?
- **Decision**: `controller/knowledge_base/internal/`.
- **Format**: Use the existing `Recipe` Pydantic model, serialized to YAML.
- **Reloading**: `KnowledgeEngine` needs a method `reload_recipes()` or `register_recipe(recipe_obj)`. Since `KnowledgeEngine` scans directories on init, we can just write the file and then manually inject the object into `self.recipes` to avoid a full reload.

## 2. Technology Choices

### 2.1 Bridge Protocol Update
- **Command**: New `BridgeCommand` type: `get_rna_info`.
- **Payload**: `{"tool_name": "bpy.ops..."}`.
- **Response**: `{"rna_info": {"name": "...", "description": "...", "params": [...]}}`.

### 2.2 Controller Implementation
- `inspect_tool`:
    1. Receives `tool_name`.
    2. Sends `get_rna_info` command to Bridge.
    3. Awaits result.
    4. Formats result as a readable string for the AI (e.g., "Tool: ... 
Params:
 - size (FLOAT): Size of cube").

## 3. Architecture

### 3.1 Components
1.  **Blender Addon (`command_executor.py` or new `introspection.py`)**: Logic to resolve operator name to RNA and extract props.
2.  **Bridge API**: No change needed, just handles the new command type payload.
3.  **MCP Server**: Add `inspect_tool` and `save_recipe` functions decorated with `@mcp.tool()`.

### 3.2 Security
- **Path Traversal**: `save_recipe` must strictly sanitize the recipe name to prevent writing outside `knowledge_base/internal/`.
- **Introspection**: Read-only operation, low risk.

## 4. Migration Steps
1.  Implement `get_rna_info` logic in Blender Addon.
2.  Update `BridgeCommand` model (if strict enum) or just use string literal.
3.  Implement `inspect_tool` in `mcp_server.py`.
4.  Implement `save_recipe` in `mcp_server.py`.
