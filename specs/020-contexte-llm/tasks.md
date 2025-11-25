# Tasks: Contexte LLM pour Blender

> **Feature**: 020-contexte-llm
> **Status**: Completed

## Phase 1: Setup
- [x] T001 Create prompt templates directory `controller/resources/llm_prompts/`

## Phase 2: Foundational
- [x] T002 Modify `GeminiClient.run_dynamic_conversation` in `controller/app/gemini_client.py` to accept `system_instruction`
- [x] T003 Create `controller/app/validation.py` with `validate_bpy_script` function (syntax check using `ast`)
- [x] T004 Create `run_validation_tests.bat` (or add to `run_tests.bat`) to execute `controller/tests/test_validation.py`

## Phase 3: User Story 1 - Generate Executable BPY Script (P1)
**Goal**: The system must provide an executable BPY script when requested, validated for syntax.
**Independent Test**: Send request with `mode='format-to-bpy'`, receive valid Python code.
- [x] T005 [US1] Create `format-to-bpy.md` template in `controller/resources/llm_prompts/` with strict output instructions
- [x] T006 [US1] Update `ChatService.process_message` in `controller/app/services.py` to accept `mode` parameter
- [x] T007 [US1] Implement template loading logic in `ChatService` in `controller/app/services.py`
- [x] T008 [US1] Update `ChatService` to use `GeminiClient` with dynamic `system_instruction` in `controller/app/services.py`
- [x] T009 [US1] Integrate `validate_bpy_script` into `ChatService` workflow for `format-to-bpy` mode in `controller/app/services.py`
- [x] T010 [US1] Create unit tests for BPY generation and validation in `controller/tests/test_chat_service.py`
- [x] T011 [US1] Run validation tests using `run_tests.bat`

## Phase 4: User Story 2 - Contextual Mode (P2)
**Goal**: The LLM is loaded with a prompt specifying the Blender environment and naming conventions.
**Independent Test**: Send request with `mode='contextual'`, check response for Blender terminology.
- [x] T012 [US2] Create `contextual.md` template in `controller/resources/llm_prompts/` with Blender expert persona and rules
- [x] T013 [US2] Update `ChatService` in `controller/app/services.py` to handle `mode='contextual'` specifically (if different from default)
- [x] T014 [US2] Create unit tests for contextual mode prompt injection in `controller/tests/test_chat_service.py`
- [x] T015 [US2] Run validation tests using `run_tests.bat`

## Phase 5: Polish
- [x] T016 Run full system verification and ensure no regressions