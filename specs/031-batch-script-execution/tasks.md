# Tasks: Batch Script Execution (Spec 031)

## Phase 1: Setup
- [x] Create `tests/test_batch_execution.py` skeleton <!-- id: 0 -->
    - [x] Define test cases for `submit_script` <!-- id: 1 -->
    - [x] Mock `bridge_manager` for offline testing <!-- id: 2 -->

## Phase 2: Foundational (Controller)
- [x] Implement `submit_script` in `mcp_server.py` <!-- id: 3 -->
    - [x] Integrate `SecurityValidator` <!-- id: 4 -->
    - [x] Implement BridgeCommand wrapping <!-- id: 5 -->
    - [x] Implement execution and stdout capture <!-- id: 6 -->
- [x] Verify `submit_script` with automated tests <!-- id: 7 -->

## Phase 3: User Story 1 (Context Retention & Prompt Alignment)
- [x] Audit and Update Prompts <!-- id: 8 -->
    - [x] Update `system_prompt.md` (Core Directives & Batch Strategy) <!-- id: 9 -->
    - [x] Update `resources/llm_prompts/contextual.md` (Enforce Batch Mode) <!-- id: 10 -->
    - [x] Review `resources/llm_prompts/router.md` (Ensure intent alignment) <!-- id: 11 -->
    - [x] Check `resources/llm_prompts/format-to-bpy.md` for conflicts <!-- id: 17 -->
    - [x] Prioritize `submit_script` over `execute_command` in all prompts <!-- id: 18 -->
- [ ] Manual Verification <!-- id: 12 -->
    - [ ] Test "Create and Move" scenario <!-- id: 13 -->
    - [ ] Verify context retention (variable usage) <!-- id: 14 -->

## Phase 4: Polish
- [x] Update `GEMINI.md` with new feature <!-- id: 15 -->
- [x] Run full regression suite <!-- id: 16 -->
