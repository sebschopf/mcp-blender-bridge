# Tasks: Enhanced Debug Logging

> **Feature**: 025-enhanced-logging
> **Status**: In Progress

## Phase 1: Setup
- [x] T001 Create `controller/app/logging_utils.py` with `PerformanceLogger` class <!-- id: 0 -->

## Phase 2: Foundational
- [x] T002 Update `controller/app/main.py` to configure logging with detailed formatting <!-- id: 1 -->
- [x] T003 Instrument `ChatService.process_message` in `controller/app/services.py` with `PerformanceLogger` for request start/end and intent classification <!-- id: 2 -->
- [x] T004 Instrument `ChatService.classify_intent` in `controller/app/services.py` with `PerformanceLogger` <!-- id: 3 -->
- [x] T005 Instrument `GeminiClient.run_dynamic_conversation` in `controller/app/gemini_client.py` with `PerformanceLogger` <!-- id: 4 -->
- [x] T006 Instrument tool execution calls in `GeminiClient.run_dynamic_conversation` with `PerformanceLogger` <!-- id: 5 -->

## Phase 3: User Story 1 - End-to-End Performance Tracing (P1)
**Goal**: Developers trace request lifecycle with timestamps.
**Independent Test**: Send request, check `mcp_server_log.txt` for structured entries.
- [x] T007 [US1] Manually verify server logs show tags `[REQ_START]`, `[LLM_CALL_START]`, etc. <!-- id: 6 -->

## Phase 4: User Story 2 - Client-Side Timeout Configuration (P2)
**Goal**: Users can configure connection timeout.
**Independent Test**: Change timeout preference, verify client waits longer.
- [x] T008 [US2] Add `request_timeout` IntProperty to `MCPAddonPreferences` in `blender_addon/preferences.py` <!-- id: 7 -->
- [x] T009 [US2] Add timeout slider to `MCPAddonPreferences.draw` in `blender_addon/preferences.py` <!-- id: 8 -->
- [x] T010 [US2] Update `MCPClient._send_request` in `blender_addon/mcp_client.py` to read `request_timeout` from preferences <!-- id: 9 -->
- [x] T011 [US2] Update `run_blender_tests.ps1` or test file to verify timeout handling (optional, or manual test) <!-- id: 10 -->

## Phase 5: Polish
- [x] T012 Run `run_tests.bat` to ensure logging changes don't break existing tests <!-- id: 11 -->
