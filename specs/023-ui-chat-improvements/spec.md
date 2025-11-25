# Feature Specification: UI Chat Improvements

**Feature Branch**: `023-ui-chat-improvements`  
**Created**: 2025-11-25  
**Status**: Draft  
**Input**: User description: "Améliorer l'affichage du chat dans le panneau latéral de l'addon Blender. Le texte des messages (surtout ceux de l'IA) doit être automatiquement coupé (word wrap) pour tenir dans la largeur du panneau et ne pas être tronqué. De plus, toutes les parties de l'interface (boutons, champs, labels) doivent avoir des info-bulles (tooltips) claires et descriptives pour guider l'utilisateur."

## User Scenarios & Testing

### User Story 1 - Responsive Chat Display (Priority: P1)

Users need to read the full content of AI responses within the Blender N-Panel without horizontal scrolling or truncation, regardless of the text length.

**Why this priority**: Currently, long messages are cut off, making the assistant unusable for complex explanations or code snippets.

**Independent Test**:
- Generate a long lorem ipsum message (or ask the AI for a long explanation).
- Resize the N-Panel to be narrow.
- Verify that the text wraps to the next line automatically and remains fully visible.

**Acceptance Scenarios**:

1. **Given** a long AI response (> 50 words), **When** displayed in the chat panel, **Then** it is split into multiple lines.
2. **Given** the user resizes the sidebar width, **When** the width changes, **Then** the text re-flows to adapt to the new width (if feasible with Blender's UI API, or uses a fixed wrap width that fits standard sizes).

### User Story 2 - Comprehensive Tooltips (Priority: P2)

Users need to understand the function of every UI element (buttons, inputs, status indicators) by hovering over them.

**Why this priority**: Improves usability and discoverability of features like "LLM Mode" or connection status.

**Independent Test**:
- Hover over the "Connect" button, the "Mode" selector, and the chat input.
- Verify that a clear description appears for each.

**Acceptance Scenarios**:

1. **Given** the "LLM Mode" dropdown, **When** hovered, **Then** a tooltip explains the difference between "Contextual" and "Script Generation".
2. **Given** the "Connect" button, **When** hovered, **Then** a tooltip explains it connects to the local MCP server.

## Requirements

### Functional Requirements

- **FR-001**: The chat interface MUST implement a word-wrapping mechanism for message history items.
- **FR-002**: Long text messages MUST be split into multiple `layout.label()` calls or equivalent to simulate wrapping, as `layout.label` does not wrap natively.
- **FR-003**: All interactive UI elements (Operators, Properties) MUST have a `description` parameter defined in their registration or UI definition.
- **FR-004**: The wrapping logic should respect a reasonable character limit per line (e.g., based on approximate panel width) or use a dynamic UI technique if available.

### Key Entities

- **UI Helper Functions**: New utility function `draw_multiline_label(layout, text, width)` in `blender_addon/ui.py`.

## Success Criteria

### Measurable Outcomes

- **SC-001**: 100% of AI messages under 500 characters are fully visible in a standard N-Panel width (300px).
- **SC-002**: All buttons and properties in the `MCP_PT_Panel` have a non-empty tooltip.