# Implementation Tasks: Dynamic Model Discovery

**Feature Branch**: `012-dynamic-model-discovery`
**Feature Spec**: `specs/012-dynamic-model-discovery/spec.md`
**Implementation Plan**: `specs/012-dynamic-model-discovery/plan.md`
**Created**: 2025-11-21

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Project initialization and basic structure

- [x] T001 Create project structure per implementation plan
- [x] T002 [P] Update `specs/012-dynamic-model-discovery/research.md` if needed based on latest findings

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Core infrastructure that MUST be complete before ANY user story can be implemented

**⚠️ CRITICAL**: No user story work can begin until this phase is complete

- [x] T003 [P] Implement `list_available_models` method in `controller/app/gemini_client.py` using `genai.list_models`
- [x] T004 Add `/api/models` endpoint in `controller/app/main.py` that calls `gemini_client.list_available_models`
- [x] T005 [P] Create test for `/api/models` endpoint in `controller/tests/test_main.py`

**Checkpoint**: Foundation ready - user story implementation can now begin in parallel

---

## Phase 3: User Story 1 - Dynamic Model Selection (Priority: P1) 🎯 MVP

**Goal**: Allow users to fetch available models from the API and select one in the Blender addon UI.

**Independent Test**: Open addon preferences, click "Refresh Models", see dropdown populated, select a model, and run a command.

### Implementation for User Story 1

- [x] T006 [US1] Add `AvailableModels` cache and `selected_model` EnumProperty in `blender_addon/preferences.py`
- [x] T007 [US1] Implement `MCP_OT_RefreshModels` operator in `blender_addon/operators.py` to query `/api/models`
- [x] T008 [US1] Add "Refresh Models" button and model dropdown to `MCPAddonPreferences.draw` in `blender_addon/preferences.py`
- [x] T009 [US1] Add `custom_model_name` StringProperty in `blender_addon/preferences.py` visible when "Custom" is selected
- [x] T010 [US1] Update `blender_addon/server_manager.py` to retrieve the selected model from preferences
- [x] T011 [US1] Update `blender_addon/server_manager.py` to pass `GEMINI_MODEL` environment variable to the server process
- [x] T012 [US1] Update `controller/app/gemini_client.py` to initialize `GenerativeModel` using `GEMINI_MODEL` env var (defaulting to `gemini-1.5-flash`)

**Checkpoint**: At this point, User Story 1 should be fully functional and testable independently

---

## Phase 4: User Story 2 - Automatic Environment Variable Fallback (Priority: P2)

**Goal**: Automatically use `GEMINI_API_KEY` from system environment variables if not set in addon preferences.

**Independent Test**: Clear API Key in preferences, set `GEMINI_API_KEY` env var, restart, and verify connection works.

### Implementation for User Story 2

- [x] T013 [US2] Modify `start_server` in `blender_addon/server_manager.py` to check `os.environ.get("GEMINI_API_KEY")` if preference is empty
- [x] T014 [US2] Update `blender_addon/ui.py` to reflect status (e.g., "Using system API Key") if applicable (optional polish)

**Checkpoint**: At this point, User Stories 1 AND 2 should both work independently

---

## Phase 5: Polish & Cross-Cutting Concerns

**Purpose**: Improvements that affect multiple user stories

- [x] T015 [P] Update `README.md` with new configuration options (Model selection, Env var)
- [x] T016 [P] Update `quickstart.md` validation
- [x] T017 Run validation tests using run_tests.bat

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies
- **Foundational (Phase 2)**: Depends on Setup
- **User Story 1 (Phase 3)**: Depends on Foundational (needs API endpoint)
- **User Story 2 (Phase 4)**: Independent of US1, can run in parallel after Foundational (or even before, as it touches different logic)
- **Polish (Phase 5)**: Depends on US1 and US2

### Implementation Strategy

1. Complete Phase 1 & 2 to get the backend ready.
2. Implement User Story 1 (MVP) to get the UI working.
3. Implement User Story 2 for better DevX.
4. Final Polish.
