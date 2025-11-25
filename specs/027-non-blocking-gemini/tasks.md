# Tasks: Non-Blocking Gemini API Calls

> **Feature**: 027-non-blocking-gemini
> **Status**: In Progress

## Phase 1: Setup

## Phase 2: Foundational
- [x] T001 Import `asyncio` in `controller/app/gemini_client.py` <!-- id: 0 -->
- [x] T002 Update `GeminiClient.run_dynamic_conversation` in `controller/app/gemini_client.py` to wrap `client.chats.create` and `chat.send_message` in `asyncio.to_thread` <!-- id: 1 -->
- [x] T003 Update `GeminiClient.simple_generate` in `controller/app/gemini_client.py` to be `async` and use `asyncio.to_thread` for `generate_content` <!-- id: 2 -->
- [x] T004 Update `GeminiClient.list_available_models` in `controller/app/gemini_client.py` to be `async` and use `asyncio.to_thread` for `models.list` <!-- id: 3 -->

## Phase 3: User Story 1 - Concurrent Request Handling (P1)
**Goal**: Ensure server is responsive during LLM calls.
**Independent Test**: Run server, start long LLM task, hit `/internal/get_command` and verify immediate response.
- [x] T005 [US1] Update call sites for `simple_generate` in `controller/app/services.py` (ChatService.classify_intent) to use `await` <!-- id: 4 -->
- [x] T006 [US1] Update call sites for `list_available_models` in `controller/app/main.py` (get_models) to use `await` <!-- id: 5 -->
- [x] T007 [US1] Create unit tests mocking the async behavior in `controller/tests/test_gemini_client_async.py` (new test file) <!-- id: 6 -->
- [x] T008 [US1] Update existing tests in `controller/tests/` to reflect async nature of `simple_generate` and `list_available_models` (update mocks) <!-- id: 7 -->
- [x] T009 [US1] Run validation tests using `run_tests.bat` <!-- id: 8 -->

## Phase 4: Polish
- [ ] T010 Manual verification of interleaving logs during a "Create a prop" task (Requires Blender running) <!-- id: 9 -->
