# Tasks: Sticky Scenario Routing

> **Feature**: 024-sticky-scenario
> **Status**: In Progress

## Phase 1: Setup

## Phase 2: Foundational
- [x] T001 Update `router.md` in `controller/resources/llm_prompts/` to include `reset` intent and keywords (e.g., "stop", "new task", "cancel") <!-- id: 0 -->
- [x] T002 Update `ChatService.active_sessions` in `controller/app/services.py` to store `history` and `active_scenario` per session <!-- id: 1 -->
- [x] T003 Update `ChatService.handle_connect` in `controller/app/services.py` to initialize new session state `{"history": [], "active_scenario": None}` <!-- id: 2 -->
- [x] T004 Update `ChatService.handle_disconnect` in `controller/app/services.py` to correctly access session data <!-- id: 3 -->

## Phase 3: User Story 1 - Scenario Persistence (P1)
**Goal**: The system remembers the current task context across multiple turns of conversation.
**Independent Test**: Send "Create a prop" -> Verify system enters `prop` scenario. Send "Make it red" -> Verify system STAYS in `prop` scenario. Send "Cancel" -> Verify system resets.
- [x] T005 [US1] Modify `ChatService.process_message` in `controller/app/services.py` to check for `active_scenario` in session state <!-- id: 4 -->
- [x] T006 [US1] Implement logic in `ChatService.process_message` to classify new intent using the router <!-- id: 5 -->
- [x] T007 [US1] Implement logic in `ChatService.process_message` to update `active_scenario` based on new intent (reset, new specific intent, or keep current) <!-- id: 6 -->
- [x] T008 [US1] Ensure `ChatService.process_message` loads the correct system prompt from the `active_scenario` <!-- id: 7 -->
- [x] T009 [US1] Create unit tests in `controller/tests/test_chat_service_sticky.py` for scenario persistence and reset <!-- id: 8 -->
- [x] T010 [US1] Run validation tests using `run_tests.bat` <!-- id: 9 -->

## Phase 4: Polish
- [x] T011 Verify reset/cancellation flow manually in Blender <!-- id: 10 -->
- [x] T012 Run full system verification and ensure no regressions <!-- id: 11 -->
