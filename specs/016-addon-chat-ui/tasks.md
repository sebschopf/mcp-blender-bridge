# Tasks: 016-addon-chat-ui

## Phase 1: Setup
Goal: Prepare the environment for UI updates.

- [x] T001 [US1] Update `blender_addon/ui.py` to import the updated data structures (if needed) or prepare for edits. (Check task is just a placeholder for starting work).

## Phase 2: Foundational (Data Model)
Goal: Update the data model to support chat roles.

- [x] T002 [US1] Update `MCP_ChatHistoryItem` in `blender_addon/ui.py` (or properties file) to include `role` EnumProperty ('USER', 'AI', 'SYSTEM').
- [x] T003 [US1] Update `blender_addon/mcp_client.py` to populate `role='AI'` when receiving messages.
- [x] T004 [US1] Update `blender_addon/operators.py` to populate `role='USER'` (and `SYSTEM`) when adding messages to history.

## Phase 3: User Story 1 (UI Implementation)
Goal: Create the visual chat interface.

- [x] T005 [US1] Refactor `MCP_PT_Panel.draw` in `blender_addon/ui.py` to iterate through `mcp_chat_history` and draw items based on `role`.
- [x] T006 [US1] Implement visual distinction (e.g., icons, alignment) for USER vs AI messages in the panel.
- [x] T007 [US1] Implement a display limit (e.g., last 10 messages) to simulate scrolling in the N-panel.

## Phase 4: User Story 2 (Integration Verification)
Goal: Verify the full stack works with the new UI and backend.

- [x] T008 [US2] Run the addon, connect to the controller, and verify the handshake "System: Connecting..." message appears with correct role/icon.
- [x] T009 [US2] Send a test message "make a cube" and verify it appears as User, and the response appears as AI.
- [x] T010 [US2] Run `run_tests.bat` to ensure no regressions in existing tests.

## Phase 5: Polish
Goal: Cleanup and UX tweaks.

- [x] T011 Ensure the chat input box is always visible/accessible at the bottom of the panel.
- [x] T012 Verify text wrapping or truncation looks acceptable.

## Dependencies

1. T002 (Data Model) must happen before T003, T004, T005.
2. T005-T007 (UI) must happen before T008 (Verification).

## Implementation Strategy
- **MVP**: Steps T002-T006 provide the core value.
- **Refinement**: T007 adds usability for long conversations.
