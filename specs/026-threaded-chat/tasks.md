# Tasks: Threaded Chat Execution

> **Feature**: 026-threaded-chat
> **Status**: In Progress

## Phase 1: Setup

## Phase 2: Foundational
- [x] T001 Add `async_send_chat_message` method to `MCPClient` in `blender_addon/mcp_client.py` <!-- id: 0 -->
- [x] T002 Implement threading logic in `async_send_chat_message` to run `_send_request` in background <!-- id: 1 -->
- [x] T003 Implement callback scheduling in `async_send_chat_message` using `bpy.app.timers.register` to return result to main thread <!-- id: 2 -->

## Phase 3: User Story 1 - Asynchronous Chat Processing (P1)
**Goal**: Unblock Blender UI during chat requests.
**Independent Test**: Send a long request, verify UI is responsive and Bridge commands execute.
- [x] T004 [US1] Update `WM_OT_MCP_Send_Chat.execute` in `blender_addon/operators.py` to call `async_send_chat_message` instead of `send_chat_message` <!-- id: 3 -->
- [x] T005 [US1] Define callback function in `operators.py` to handle the response (update history, execute commands) <!-- id: 4 -->
- [x] T006 [US1] Update `WM_OT_MCP_Send_Chat` to disable the send button or clear input immediately (visual feedback) <!-- id: 5 -->
- [x] T007 [US1] Update `run_blender_tests.ps1` or `test_addon.py` to wait for async completion if necessary (or rely on existing timeouts) <!-- id: 6 -->

## Phase 4: Polish
- [ ] T008 Add "Thinking..." indicator or log message when async request starts <!-- id: 7 -->
- [ ] T009 Run `run_blender_tests.ps1` to ensure no regressions <!-- id: 8 -->
