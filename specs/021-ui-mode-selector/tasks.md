# Tasks: UI Mode Selector for LLM Context

> **Feature**: 021-ui-mode-selector
> **Status**: In Progress

## Phase 1: Setup
- [x] T001 Verify and update `blender_addon/tests/test_addon.py` to support mocking scene properties for testing <!-- id: 0 -->

## Phase 2: Foundational
- [x] T002 Modify `blender_addon/mcp_client.py` to accept `mode` parameter in `send_chat_message` <!-- id: 1 -->

## Phase 3: User Story 1 - Select LLM Context Mode (P1)
**Goal**: Allow users to select the LLM mode (Contextual/Script) from the Blender UI and send it with the request.
**Independent Test**: Verify API call includes correct `mode` parameter when switching UI selector.
- [x] T003 [US1] Define `mcp_llm_mode` EnumProperty in `blender_addon/__init__.py` and register it on `bpy.types.Scene` <!-- id: 2 -->
- [x] T004 [US1] Add "Mode" dropdown selector to `MCP_PT_Panel` in `blender_addon/ui.py` <!-- id: 3 -->
- [x] T005 [US1] Update `WM_OT_MCP_Send_Chat` operator in `blender_addon/operators.py` to read `mcp_llm_mode` from scene <!-- id: 4 -->
- [x] T006 [US1] Pass `mode` value to `mcp_client.send_chat_message` in `blender_addon/operators.py` <!-- id: 5 -->
- [x] T007 [US1] Create test case in `blender_addon/tests/test_addon.py` (or new file) to verify property registration and mode switching <!-- id: 6 -->
- [x] T008 [US1] Run addon tests using `run_blender_tests.ps1` (or equivalent) <!-- id: 7 -->

## Phase 4: Polish
- [x] T009 Ensure UI layout is clean and consistent with Blender standards <!-- id: 8 -->
