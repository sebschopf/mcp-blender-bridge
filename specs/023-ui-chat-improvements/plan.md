# Implementation Plan - 023-ui-chat-improvements

**Feature**: UI Chat Improvements
**Status**: DRAFT

## Technical Context

### Architecture Overview

This feature focuses on enhancing the user interface of the Blender Addon (`blender_addon/`). The core goal is to improve the readability of the chat history by implementing word wrapping and to improve usability by adding clear tooltips to all interactive elements.

**Existing Components:**
- `blender_addon/ui.py`: Handles the drawing of the N-Panel. Currently uses simple `layout.label()` which truncates text.
- `blender_addon/operators.py`: Defines the operators (buttons). Some lack `bl_description` (tooltips).
- `blender_addon/__init__.py`: Registers properties. These already have descriptions.

### Libraries & Dependencies

- **Blender Python API (`bpy`)**: Used for UI drawing (`layout`, `operator`) and text processing (`textwrap` module from standard library can be used within Blender Python).

### Project Structure

```text
blender_addon/
  ui.py                # Update: Add wrapping logic
  operators.py         # Update: Add descriptions to operators
```

## Constitution Check

### Privacy & Security
- **Data Handling**: No change in data handling. Purely UI presentation.
- **Safety**: Clearer UI reduces user error (e.g., better understanding of "Disconnect" vs "Connect").

### Technical Constraints
- **Performance**: Wrapping text dynamically in `draw` can be expensive if not optimized. We will use a simple `textwrap.wrap` based on an estimated character width, which is performant enough for UI updates.
- **UI limitations**: Blender's `layout.label` doesn't support wrapping. We must simulate it by creating a `layout.column` and adding multiple labels.

## Phase 0: Research & Decisions

### Design Decisions

1.  **Wrapping Strategy**: Instead of complex pixel-width calculation (which is hard in Blender Python without `blf`), we will use a character-based wrap. A standard N-Panel is roughly 30-40 characters wide. We can default to ~40 chars or make it slightly dynamic if `context.region.width` is available.
2.  **Helper Function**: Create `draw_multiline_label(layout, text, icon)` in `ui.py` to encapsulate the logic.

## Phase 1: Design & Contracts

### API Changes

- No backend changes.
- Blender UI update only.

## Phase 2: Implementation

### Dependencies

- None.

### Strategy

1.  **Operators**: Go through `operators.py` and add `bl_description` to all classes.
2.  **UI Logic**: Implement `draw_multiline_label` in `ui.py` using `textwrap`.
3.  **Integration**: Replace the simple label loop in `MCP_PT_Panel.draw` with calls to `draw_multiline_label`.

## Phase 3: Polish

- Tune the wrapping width constant to look good in the default Blender layout.