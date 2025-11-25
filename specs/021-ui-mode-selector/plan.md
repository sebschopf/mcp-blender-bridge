# Implementation Plan - 021-ui-mode-selector

**Feature**: UI Mode Selector for LLM Context
**Status**: DRAFT

## Technical Context

### Architecture Overview

The Blender Addon needs to expose a new user preference, "LLM Mode", which dictates how the backend Controller processes the request (Chat vs Script Generation). This involves:
1.  **State Management**: Storing the selection in Blender's runtime state (`bpy.types.Scene`).
2.  **UI Layer**: Adding a dropdown selector to the existing MCP panel in Blender.
3.  **Operator Layer**: Extracting this value when the "Send" button is clicked.
4.  **Network Layer**: Passing this value in the API payload to the Controller.

**Existing Components:**
- `blender_addon/__init__.py`: Registers properties on `bpy.types.Scene`.
- `blender_addon/ui.py`: Draws the UI panel.
- `blender_addon/operators.py`: Handles the send event.
- `blender_addon/mcp_client.py`: Sends the HTTP request.

### Libraries & Dependencies

- **Blender Python API (`bpy`)**: Used for UI properties and interface drawing.
- **Python Standard Library**: `requests` (used in `mcp_client.py`).

### Project Structure

```text
blender_addon/
  __init__.py          # Register EnumProperty
  ui.py                # Add UI selector
  operators.py         # Read property, pass to client
  mcp_client.py        # Update API payload
```

## Constitution Check

### Privacy & Security
- **Data Handling**: The new "mode" parameter is non-sensitive configuration data.
- **Safety**: No direct safety implications, but enabling "Script Generation" mode (backend feature) does involve code execution risks, which are handled by the backend's confirmation flow (out of scope for this UI task, but relevant context).

### Technical Constraints
- **Compatibility**: Must use standard Blender UI widgets (`EnumProperty`).
- **Persistence**: Using `Scene` properties means the setting is saved with the `.blend` file, which is desired behavior for project-specific context.

## Phase 0: Research & Decisions

### Design Decisions

1.  **Property Location**: `bpy.types.Scene` is chosen over `AddonPreferences` because the mode (chat vs script) is likely a per-session or per-project context, not a global plugin setting. It allows easier access in the UI panel.
2.  **UI Widget**: `layout.prop` with `text=""` (no label) or minimal label to save space in the panel.
3.  **Enum Values**:
    - `contextual`: "Contextual (Chat)"
    - `format-to-bpy`: "Script Generation"

## Phase 1: Design & Contracts

### Data Model (`data-model.md`)

- **New Property**: `mcp_llm_mode` (EnumProperty) on `Scene`.

### API Changes (`contracts/`)

- **Client-Side**: `MCPClient.send_chat_message` signature updated to accept `mode: str`.
- **Payload**: `{ ..., "mode": "contextual" | "format-to-bpy" }`.

## Phase 2: Implementation

### Dependencies

- **Backend Support**: The backend Controller must support the `mode` parameter (completed in feature `020`).

### Strategy

1.  **Registry**: Add `mcp_llm_mode` to `__init__.py`.
2.  **Client**: Update `mcp_client.py` to handle the new parameter.
3.  **Operator**: Update `operators.py` to read from scene and call client.
4.  **UI**: Add the control to `ui.py`.

## Phase 3: Polish

- Ensure the UI looks clean and the dropdown doesn't clutter the interface.
- Verify default value is "Contextual".