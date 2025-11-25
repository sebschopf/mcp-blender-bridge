# Tasks: Intelligent LLM Scenario Routing System

> **Feature**: 022-scenario-router
> **Status**: In Progress

## Phase 1: Setup
- [x] T001 Create scenario definitions directory `controller/resources/llm_prompts/scenarios/`

## Phase 2: Foundational
- [x] T002 Add `simple_generate` method to `GeminiClient` in `controller/app/gemini_client.py` for single-turn text generation
- [x] T003 Create `router.md` in `controller/resources/llm_prompts/` with a prompt for intent classification
- [x] T004 Create `character.md` in `controller/resources/llm_prompts/scenarios/` with instructions for character creation <!-- id: 3 -->
- [x] T005 Create `architecture.md` in `controller/resources/llm_prompts/scenarios/` with instructions for architecture creation <!-- id: 4 -->
- [x] T006 Create `prop.md` in `controller/resources/llm_prompts/scenarios/` with instructions for prop creation <!-- id: 5 -->
- [x] T007 Create `scripting.md` in `controller/resources/llm_prompts/scenarios/` with instructions for direct scripting tasks <!-- id: 6 -->

## Phase 3: User Story 1 - Intent-Based Scenario Selection (P1)
**Goal**: The system intelligently understands user intent and applies a structured scenario.
**Independent Test**: Send prompts, verify correct scenario classification and prompt loading.
- [x] T008 [US1] Implement `classify_intent(user_message)` method in `ChatService` in `controller/app/services.py` to use `simple_generate` with `router.md` <!-- id: 7 -->
- [x] T009 [US1] Update `ChatService.process_message` in `controller/app/services.py` to call `classify_intent` if `mode` is `contextual` and load the corresponding scenario prompt <!-- id: 8 -->
- [x] T010 [US1] Implement logic in `ChatService` to check mandatory scenario conditions (as defined in `spec.md` FR-003) <!-- id: 9 -->
- [x] T011 [US1] Implement logic in `ChatService` to ask clarifying questions if mandatory conditions are missing (FR-004) <!-- id: 10 -->
- [x] T012 [US1] Create unit tests for intent classification and scenario loading in `controller/tests/test_chat_service.py` <!-- id: 11 -->
- [x] T013 [US1] Run validation tests using `run_tests.bat` <!-- id: 12 -->

## Phase 4: Polish
- [x] T014 Tune `router.md` and scenario prompts to improve accuracy and reduce false positives <!-- id: 13 -->
- [x] T015 Run full system verification and ensure no regressions <!-- id: 14 -->