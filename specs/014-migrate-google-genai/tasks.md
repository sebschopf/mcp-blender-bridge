# Tasks: 014-migrate-google-genai

## Phase 1: Setup
Goal: Prepare the environment for migration by updating dependencies.

- [x] T001 Update `controller/requirements.txt` to replace `google-generativeai` with `google-genai`
- [x] T002 Update `uv.lock` and install new dependencies using `uv pip install -r controller/requirements.txt --python controller/.venv/Scripts/python.exe`

## Phase 2: Foundational
Goal: Ensure the new SDK client can be initialized.

- [x] T003 [US1] Create `GeminiClient` with `google.genai.Client` in `controller/app/gemini_client.py` using Dependency Injection for `api_key` and `model_name`
- [x] T004 [US1] Implement `list_available_models` in `controller/app/gemini_client.py` using `client.models.list()`

## Phase 3: User Story 1 (Developer)
Goal: Full migration to `google-genai` library.

- [x] T005 [US1] Implement `run_dynamic_conversation` in `controller/app/gemini_client.py` using `client.chats.create`
- [x] T006 [US1] Implement chat history conversion to `types.Content` in `run_dynamic_conversation`
- [x] T007 [US1] Implement tool configuration in `client.chats.create` call
- [x] T008 [US1] Implement response parsing and function calling loop using new SDK structure in `run_dynamic_conversation`

## Phase 4: User Story 2 (Maintainer)
Goal: Ensure SOLID compliance and Testability.

- [x] T009 [US2] Update `controller/tests/test_main.py` to mock `google.genai.Client` instead of `genai.GenerativeModel`
- [x] T010 [US2] Update `controller/tests/test_new_tools.py` to match new client structure
- [x] T011 [US2] Run full test suite `pytest controller/` and fix any remaining issues

## Phase 5: Polish
Goal: Verify and cleanup.

- [x] T012 Verify application startup and connection with `run_tests.bat` (Addon Integration Test)
- [x] T013 Verify no legacy `google.generativeai` imports remain in the codebase

## Dependencies

1. Setup (T001-T002) must be done first.
2. T003 is required for all subsequent `GeminiClient` tasks.
3. T009-T010 (Tests) depend on T005-T008 implementation details.

## Implementation Strategy
- **MVP**: Complete Phases 1, 2, and 3 to restore functionality.
- **Verification**: Run tests immediately after Phase 4.
