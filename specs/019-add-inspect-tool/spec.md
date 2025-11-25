# Feature Specification: Add Inspect Tool & Save Recipe

**Feature Branch**: `019-add-inspect-tool`  
**Created**: 2025-11-23  
**Status**: Draft  
**Input**: Add `inspect_tool` meta-tool and `save_recipe` tool.

## User Scenarios & Testing

### User Story 1 - Tool Introspection (Priority: P1)

The AI uses the `inspect_tool` to query Blender for the exact parameters of a specific tool before executing it. This closes the loop in the Search -> Inspect -> Execute workflow.

**Why this priority**: P1. Essential for using tools that have complex or dynamic parameters not fully captured in the static index.

**Independent Test**: 
1. Mock a `BridgeCommand` response from the addon that returns parameter details for `bpy.ops.mesh.primitive_cube_add`.
2. Call the `inspect_tool` MCP tool with `tool_name="bpy.ops.mesh.primitive_cube_add"`.
3. Verify the returned string contains the parameter names and types (e.g., "size: FLOAT").

**Acceptance Scenarios**:

1. **Given** the AI knows the tool name `bpy.ops.mesh.primitive_cube_add` but not its parameters, **When** it calls `inspect_tool("bpy.ops.mesh.primitive_cube_add")`, **Then** it receives a text description of the tool's RNA properties (name, type, description).
2. **Given** an invalid tool name, **When** `inspect_tool` is called, **Then** it returns a clear error message.

---

### User Story 2 - Save Action Plan as Recipe (Priority: P2)

The AI can save a successful sequence of actions (a "recipe") to the internal knowledge base for future use.

**Why this priority**: P2. Allows the system to learn and build a library of complex operations (e.g., "make a chair") composed of simpler tools.

**Independent Test**:
1. Call the `save_recipe` MCP tool with valid recipe JSON data.
2. Verify a new YAML file is created in `controller/knowledge_base/internal/`.
3. Verify `KnowledgeEngine` reloads or updates its registry to include the new recipe.

**Acceptance Scenarios**:

1. **Given** a successful execution of multiple steps to create an object, **When** the AI calls `save_recipe` with a name ("Simple Chair") and the steps, **Then** a `Simple Chair.yaml` file is created in the knowledge base.
2. **Given** the recipe is saved, **When** the AI searches for "chair" later, **Then** this new recipe appears in the search results.

## Requirements

### Functional Requirements

- **FR-001**: Implement `inspect_tool(tool_name: str)` in `mcp_server.py`.
- **FR-002**: `inspect_tool` MUST send a `get_rna_info` command (or similar) to the Blender Addon via the Bridge.
- **FR-003**: The Blender Addon MUST implement a handler for `get_rna_info` that inspects the operator's `bl_rna` properties and returns them as JSON.
- **FR-004**: Implement `save_recipe(name: str, description: str, steps: List[Dict])` in `mcp_server.py`.
- **FR-005**: `save_recipe` MUST save the recipe to `controller/knowledge_base/internal/` (creating the directory if needed) using the standard Recipe YAML format.
- **FR-006**: The `KnowledgeEngine` MUST be able to reload or register the new recipe immediately after saving.
 - **FR-007**: `inspect_tool` MUST return a structured JSON array of parameter descriptors. Each parameter descriptor MUST include at minimum: `name` (string), `type` (string), `description` (string), `default` (nullable), and `enum` (nullable list) to allow programmatic validation and UI form generation.

### Key Entities

- **ToolInspectionResult**: Data structure returned by the Bridge containing parameter info.
- **Recipe**: Existing entity, but now creatable via API.

**ToolInspectionResult (structured)**: The `ToolInspectionResult` returned by the addon MUST be a JSON object containing a `tool_name` string and a `parameters` array. Each entry in `parameters` MUST be an object with the following fields:

- `name` (string): parameter identifier as used by the operator.
- `type` (string): simple type name (e.g., `FLOAT`, `INT`, `BOOLEAN`, `ENUM`, `STRING`).
- `description` (string): human-friendly description of the parameter.
- `default` (any|null): the default value if present, otherwise null.
- `enum` (array|null): list of allowed values for enum-like parameters, otherwise null.

This structured format enables automatic validation, form generation in UI, and conversion to MCP tool schemas.

## Success Criteria

### Measurable Outcomes

- **SC-001**: `inspect_tool` returns accurate parameter lists for standard mesh operators (e.g., `primitive_cube_add`) within 200ms (excluding network latency).
- **SC-002**: Saved recipes are immediately discoverable via `search_tools` without restarting the server.
- **SC-003**: The Blender Addon does not crash if `inspect_tool` queries a non-existent operator.

## Assumptions

- The Blender Python API allows runtime introspection of `bpy.types.Operator` properties via `bl_rna`.
- We are using the standard `Recipe` model defined in `controller/app/models.py`.

## Clarifications

### Session 2025-11-24

- Q: Quel format la sortie de `inspect_tool` doit-elle utiliser? → A: Option B (JSON structuré: `name`, `type`, `description`, `default`, `enum`).

Applied: Added `FR-007` requiring a structured JSON array of parameter descriptors and expanded the `ToolInspectionResult` entity to define the exact fields. This enables programmatic validation and UI form generation from inspection results.