# Implementation Plan - Batch Script Execution (Spec 031)

The goal is to enable the AI to generate and execute complete Python scripts in a single request, rather than executing line-by-line. This solves the context loss issue where the AI forgets object references between turns.

## User Review Required
> [!IMPORTANT]
> This changes the primary interaction model. The System Prompt will be updated to encourage `submit_script` over `execute_command` for complex tasks.

## Proposed Changes

### Controller App

#### [MODIFY] [mcp_server.py](file:///c:/Users/sebas/Documents/MCP_Outils/MCP_Blender_02/controller/app/mcp_server.py)
- Implement `submit_script(script: str) -> str` tool.
- This tool must:
    1. Validate the script using `SecurityValidator`.
    2. Wrap the script in a `BridgeCommand`.
    3. Execute it via `bridge_manager`.
    4. Return the stdout/result.

#### [MODIFY] [system_prompt.md](file:///c:/Users/sebas/Documents/MCP_Outils/MCP_Blender_02/controller/app/system_prompt.md)
- Update "Core Directives" to prioritize Batch Execution.
- Add a new section "Batch Execution Strategy".
- Instruct the AI to:
    1. Search & Inspect ALL necessary tools first.
    2. Construct a SINGLE Python script using variables.
    3. Call `submit_script`.

## Verification Plan

### Automated Tests
- Create `tests/test_batch_execution.py`:
    - Mock `bridge_manager`.
    - Call `submit_script` with a valid multi-line script.
    - Verify it passes validation and calls bridge.
    - Call `submit_script` with malicious code.
    - Verify it is blocked.

### Manual Verification
- **Scenario**: "Create a red cube and move it up 2 units."
- **Expected**:
    1. AI searches `cube`, `material`, `translate`.
    2. AI calls `submit_script` with a script containing:
       ```python
       import bpy
       bpy.ops.mesh.primitive_cube_add(...)
       cube = bpy.context.active_object
       bpy.ops.transform.translate(...)
       ```
    3. Blender executes it in one go.
