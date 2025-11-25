# Feature Specification: UI Mode Selector for LLM Context

**Feature Branch**: `021-ui-mode-selector`  
**Created**: 2025-11-24  
**Status**: Draft  
**Input**: User description: "ajouter un selecteur dans l'addon de Blender pour choisir le mode qu'on souhaite pour le llm."

## User Scenarios & Testing

### User Story 1 - Select LLM Context Mode (Priority: P1)

Users need a way to explicitly choose how the LLM interacts with Blender (Conversational/Contextual vs. Script Generation) directly from the Blender UI.

**Why this priority**: It's the core interface requirement to enable the "Format-to-BPY" feature implemented in the backend (feature 020). Without this UI, users cannot easily access the new capability.

**Independent Test**:
- Open the Blender Addon panel.
- Locate the new "LLM Mode" selector.
- Verify two options exist: "Contextual (Chat)" and "Script Generation (Format-to-BPY)".
- Send a request with each mode selected and verify the backend receives the correct `mode` parameter.

**Acceptance Scenarios**:

1. **Given** the user is in the MCP Chat panel, **When** they look at the UI, **Then** they see a dropdown or radio button set labeled "Mode" with options "Contextual" (default) and "Script Generation".
2. **Given** "Contextual" is selected, **When** the user sends a message "Create a cube", **Then** the request payload to the server includes `"mode": "contextual"`.
3. **Given** "Script Generation" is selected, **When** the user sends a message "Create a cube", **Then** the request payload to the server includes `"mode": "format-to-bpy"`.
4. **Given** the user restarts Blender, **Then** the selected mode persists (or defaults back to Contextual, depending on UX decision - assumed default for safety).

### Edge Cases

- **Server incompatibility**: If the server doesn't support the `mode` parameter (e.g. old version), the request should still succeed (ignoring the parameter) or fail gracefully. (Assumption: Server is updated).
- **Rapid switching**: Switching modes while a request is pending should not affect the *current* pending request, only subsequent ones.

## Requirements

### Functional Requirements

- **FR-001**: The Addon UI MUST display a selection mechanism (EnumProperty presented as dropdown or expanded list) for "LLM Mode".
- **FR-002**: The available modes MUST be "contextual" (Display: "Contextual / Chat") and "format-to-bpy" (Display: "Script Generation").
- **FR-003**: The default mode MUST be "contextual".
- **FR-004**: When sending a chat request to the `/api/chat` endpoint, the client MUST include the selected mode in the JSON payload under the key `mode`.
- **FR-005**: The UI element MUST be accessible in the main chat panel, clearly visible near the message input area.

### Key Entities

- **Blender Preferences/Scene Properties**: Store the current `llm_mode` selection.

## Success Criteria

### Measurable Outcomes

- **SC-001**: 100% of requests sent from the Addon include the `mode` parameter matching the UI selection.
- **SC-002**: Users can switch modes in under 2 clicks.