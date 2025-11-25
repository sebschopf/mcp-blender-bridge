# Research: Chat UI Improvements

**Feature**: `013-chat-ui-improvements`
**Date**: vendredi, 21 novembre 2025

## Decisions

### Immediate Chat Visibility
- **Decision**: Change the condition in `ui.py` to display the chat panel when status is `CONNECTING` in addition to `CONNECTED`.
- **Rationale**: This gives immediate visual feedback that the system is responding to the click, preventing "did I click it?" confusion.

### System Messages
- **Decision**: Inject local messages into `mcp_chat_history` CollectionProperty directly from the addon's operators (e.g., `WM_OT_MCP_Connect`).
- **Rationale**: This allows for instant "System: Connected" feedback without waiting for a server roundtrip.
- **Format**: Use a prefix "System: " to distinguish from User/AI messages.

### Placeholder Text
- **Decision**: Use a conditional check in `ui.py` inside the draw method. If `len(scene.mcp_chat_history) == 0`, verify status. If `CONNECTED` or `CONNECTING`, draw a disabled label or box with "Waiting for instructions...".
- **Rationale**: Standard UI pattern for empty states.

### Backend Deadlock Resolution
- **Decision**: Implement a `globals.py` module in the controller to hold the `KnowledgeEngine` singleton.
- **Rationale**: `internal_tools.py` currently calls `localhost:8000/api/discover_capabilities` via `requests`. Since `uvicorn` is single-threaded (async), this call blocks the main loop while `main.py` is waiting for `internal_tools` to finish, causing a deadlock/timeout. Direct access via a shared instance solves this.

## Technical Unknowns Resolved

- **Q**: Can we modify the CollectionProperty from the draw context?
- **A**: No, drawing is read-only. We must modify the collection in the *Operators* (`WM_OT_MCP_Connect`) or *Handlers* (`poll_mcp_controller`).

- **Q**: How to handle circular imports with `main.py` and `internal_tools.py`?
- **A**: Use `globals.py` as a third module that both import. `main.py` initializes it, `internal_tools.py` reads from it.