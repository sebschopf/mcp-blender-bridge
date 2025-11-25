# Tasks: Injection contrôlée BPY via MCP (001-inject-bpy-mcp)

**Input**: `spec.md`, `plan.md` from `specs/001-inject-bpy-mcp/`

## Phase 1: Setup (Shared Infrastructure)

 - [x] T001 Create prompt templates in `controller/resources/llm_prompts/contextual.md` and `controller/resources/llm_prompts/format-to-bpy.md`
 - [x] T002 [P] Add `controller/resources/llm_prompts/__init__.py` and small loader `controller/resources/llm_prompts/loader.py` to read prompt templates at runtime
 - [x] T003 [P] Add docs entry `specs/001-inject-bpy-mcp/quickstart.md` describing manual test scenario and sandbox expectations

---

## Phase 2: Foundational (Blocking Prerequisites)

 - [x] T004 Implement validator module skeleton `controller/validators/bpy_validator.py` with functions: `validate_syntax`, `detect_forbidden_imports`, `find_bpy_operators`, `verify_operators_with_inspect`
 - [x] T005 Implement script extraction utility `controller/validators/script_extractor.py` with `extract_script_from_response(text_or_attachment)`
 - [x] T006 Add MCP endpoint skeleton `inject_bpy_script` in `controller/mcp_server.py` (accept `{mode, script_or_text}`, persist `InjectScriptRequest` record)
 - [x] T007 [P] Add audit/logging helper `controller/logging/bpy_audit.py` and wire it into `mcp_server` request handling (persist request, validation result, sandbox result)
 - [x] T008 Configure minimal unit-test harness `controller/tests/test_bpy_validator.py` and add to repo test runner

---

## Phase 3: User Story 1 - Génération et exécution d'un script BPY (Priority: P1) 🎯 MVP

**Goal**: Receive LLM output, extract BPY script, validate, run in sandbox, present preview and `Apply to live` button.

**Independent Test**: Submit example request using `format-to-bpy` and verify flow: extraction → validation → sandbox run → preview results shown.

 - [x] T009 [US1] Implement end-to-end handler in `controller/mcp_server.py` to call `script_extractor`, `bpy_validator`, and `sandbox_runner` (depends on T004, T005, T011)
 - [x] T010 [US1] Implement sandbox runner skeleton `controller/bridge_runner/sandbox_runner.py` which accepts `{request_id, script}` and returns `{success, stdout, stderr, artifacts}`
 - [x] T011 [US1] Implement basic sandbox execution job using Docker image placeholder and a local simulation mode if Docker/Blender not available `controller/bridge_runner/docker_runner.py`
 - [ ] T012 [P] [US1] Create UI preview endpoint `controller/ui/preview_bpy.py` (or minimal API handler in `mcp_server`) to return extracted script + validation + sandbox results
 - [ ] T013 [US1] Add unit test `controller/tests/test_end_to_end_flow.py` that asserts validated script runs in simulated sandbox and response schema matches `BPYExecutionRecord`
 - [x] T012 [P] [US1] Create UI preview endpoint `controller/ui/preview_bpy.py` (or minimal API handler in `mcp_server`) to return extracted script + validation + sandbox results
 - [x] T013 [US1] Add unit test `controller/tests/test_end_to_end_flow.py` that asserts validated script runs in simulated sandbox and response schema matches `BPYExecutionRecord`
 - [x] T014 [US1] Add logging of `InjectScriptRequest`, `ValidationResult`, and `BPYExecutionRecord` to `controller/logs/` using `bpy_audit` helper

---

## Phase 4: User Story 2 - LLM s'appuie sur l'inspection outil (Priority: P2)

**Goal**: Ensure operator parameters used by LLM are verified by `inspect_tool` before accepting script.

**Independent Test**: Call `inspect_tool` for an operator and verify `verify_operators_with_inspect` flags mismatches.

 - [x] T015 [US2] Implement `verify_operators_with_inspect` wiring in `controller/validators/bpy_validator.py` calling MCP `inspect_tool` (depends on T004 and T006)
 - [x] T016 [US2] Extend `gemini_client` usage to include per-request `system_instruction` template (update call-site in `controller/mcp_server.py` handler)
 - [x] T017 [US2] Add integration test `controller/tests/test_inspect_integration.py` that stubs `inspect_tool` responses and verifies validator behavior

---

## Phase 5: Polish & Cross-Cutting Concerns

- [x] T018 [P] Add CI job that runs `controller/tests/` unit tests and lints changed files (add to existing CI or `ci/` folder)
 - [x] T019 Update documentation `docs/inject-bpy-workflow.md` and `specs/001-inject-bpy-mcp/quickstart.md` to include sandbox requirements and manual test steps
- [ ] T020 Security hardening: Add rejection rules in `bpy_validator` for imports and filesystem/network access and add test vectors in `controller/tests/test_validator_rejections.py`
- [ ] T021 [P] Run manual E2E scenario and capture logs/artifacts in `build/` (demo-ready)

---

## Dependencies & Execution Order

- Foundation (T004..T008) BLOCKS user stories (T009..T017)
- Sandbox implementation (T010/T011) required before completing T009
- `inspect_tool` verification tasks (T015) depend on MCP endpoint skeleton (T006)

## Summary Report

- Total tasks: 21
- Tasks per story:
  - Setup: 3
  - Foundational: 5
  - User Story 1 (P1): 6
  - User Story 2 (P2): 3
  - Polish: 4
- Parallel opportunities identified: T002, T003, T005, T017, T018, T021
- Suggested MVP scope: Complete Phases 1+2 and User Story 1 (T001..T014)

**File generated by**: `.gemini/commands/speckit.tasks.toml` process
