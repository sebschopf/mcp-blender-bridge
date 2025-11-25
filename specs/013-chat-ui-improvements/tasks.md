# Implementation Tasks: Chat UI Improvements

**Feature Branch**: `013-chat-ui-improvements`
**Feature Spec**: `specs/013-chat-ui-improvements/spec.md`
**Implementation Plan**: `specs/013-chat-ui-improvements/plan.md`
**Created**: 2025-11-21

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Project initialization and basic structure

- [x] T001 Create project structure per implementation plan (Existing)
- [x] T002 [P] Verify project structure and dependencies

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Core infrastructure that MUST be complete before ANY user story can be implemented

**⚠️ CRITICAL**: No user story work can begin until this phase is complete

- [x] T003 [P] Create `controller/app/globals.py` to hold the `KnowledgeEngine` singleton
- [x] T004 Modify `controller/app/main.py` to initialize `globals.knowledge_engine` on startup
- [x] T005 Modify `controller/app/internal_tools.py` to use `globals.knowledge_engine` instead of HTTP requests (Deadlock fix)
- [x] T006 [P] Define `SYSTEM` message type constant/enum in `blender_addon/mcp_client.py` or `ui.py` if not present
- [x] T007 [P] Update `MCP_ChatHistoryItem` in `blender_addon/ui.py` to support message types/sources if needed

**Checkpoint**: Foundation ready - user story implementation can now begin in parallel

---

## Phase 3: User Story 1 - Always-Visible Chat Interface (Priority: P1) 🎯 MVP

**Goal**: Ensure the chat UI is visible as soon as the user initiates a connection attempt.

**Independent Test**: Click "Connect", verify UI appears immediately while status is "Connecting...".

### Implementation for User Story 1

- [x] T008 [US1] Modify `MCP_PT_Panel.draw` in `blender_addon/ui.py` to show chat panel when status is `CONNECTING` or `CONNECTED`
- [x] T009 [US1] Modify `MCP_PT_Panel.draw` in `blender_addon/ui.py` to ensure input field is enabled/disabled correctly based on status (optional polish)

**Checkpoint**: At this point, User Story 1 should be fully functional and testable independently

---

## Phase 4: User Story 2 - Explicit AI Status Feedback (Priority: P2)

**Goal**: Provide clear system status messages in the chat history.

**Independent Test**: Connect and observe "System: Connecting...", "System: Connected" messages in chat history.

### Implementation for User Story 2

- [x] T010 [US2] Update `WM_OT_MCP_Connect` in `blender_addon/operators.py` to inject "System: Connecting..." message into chat history
- [x] T011 [US2] Update `attempt_connection` in `blender_addon/__init__.py` to inject "System: Connected. Waiting for AI..." upon success
- [x] T012 [US2] Update `attempt_connection` in `blender_addon/__init__.py` to inject "System: Connection Failed" upon failure
- [x] T013 [US2] Modify `MCP_PT_Panel.draw` in `blender_addon/ui.py` to display "Waiting for instructions..." placeholder if chat history is empty

**Checkpoint**: At this point, User Stories 1 AND 2 should both work independently

---

## Phase 5: Polish & Cross-Cutting Concerns

**Purpose**: Improvements that affect multiple user stories

- [x] T014 [P] Update `blender_addon/tests/test_addon.py` to verify UI state changes (checking `mcp_connection_status` transitions)
- [ ] T015 Run validation tests using `run_tests.bat`

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies
- **Foundational (Phase 2)**: Depends on Setup. **Includes deadlock fix which is critical.**
- **User Story 1 (Phase 3)**: Depends on Foundational
- **User Story 2 (Phase 4)**: Depends on Foundational, independent of US1
- **Polish (Phase 5)**: Depends on US1 and US2

### Implementation Strategy

1. Fix the backend deadlock first (T003-T005) to ensure stability.
2. Implement immediate UI visibility (US1) to fix the "did it work?" confusion.
3. Implement system messages (US2) to provide detailed feedback.
4. Verify with tests.