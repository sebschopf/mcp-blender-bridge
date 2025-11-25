# Tasks: Add Inspect Tool & Save Recipe

**Phase**: Implementation | **Feature**: 019-add-inspect-tool

## Phase 1: Setup & Dependencies
*Update data models and project structure.*

- [x] T001 Update `BridgeCommand` in `controller/app/bridge_models.py` to include "get_rna_info" in the `type` literal
- [x] T002 Create `blender_addon/introspection.py` skeleton
- [x] T003 Define `SaveRecipeRequest` in `controller/app/models.py` (or reuse `Recipe` model if appropriate)

## Phase 2: Foundational - Blender Introspection
*Implement the logic to extract RNA properties in Blender.*

- [x] T004 Implement `get_operator_rna` in `blender_addon/introspection.py` (mapping tool name to RNA)
- [x] T005 Implement `extract_properties` in `blender_addon/introspection.py` to return JSON-serializable prop details
- [x] T006 [P] Update `blender_addon/mcp_client.py` (BridgeClient) to handle `get_rna_info` command type and call introspection logic
- [ ] T007 Create a test script `blender_addon/tests/test_introspection.py` to verify property extraction for a known operator (e.g., `primitive_cube_add`)

## Phase 3: User Story 1 - Tool Introspection
*Implement the inspect_tool MCP capability.*

- [x] T008 [US1] Implement `inspect_tool` in `controller/app/mcp_server.py`
- [x] T009 [US1] Update `inspect_tool` to format the JSON response into a readable string for the AI
- [x] T010 [US1] Register `inspect_tool` in `register_tools` function in `controller/app/mcp_server.py`
- [x] T011 [US1] Add unit test for `inspect_tool` in `controller/tests/test_mcp_server.py` (mocking the bridge response)

## Phase 4: User Story 2 - Save Action Plan as Recipe
*Implement the save_recipe MCP capability.*

- [x] T012 [US2] Update `controller/app/knowledge_engine.py` to add `register_recipe(recipe_obj)` method
- [x] T013 [US2] Implement `save_recipe` in `controller/app/mcp_server.py` using `SaveRecipeRequest` validation
- [x] T014 [US2] Update `save_recipe` to save YAML file to `controller/knowledge_base/internal/` and call `register_recipe`
- [x] T015 [US2] Register `save_recipe` in `register_tools` function in `controller/app/mcp_server.py`
- [x] T016 [US2] Add unit test for `save_recipe` in `controller/tests/test_mcp_server.py` (mocking filesystem write)

## Phase 5: Polish
*Documentation and final checks.*

- [x] T017 Update `controller/app/gemini_client.py` system prompt to mention `inspect_tool` and `save_recipe` capabilities
- [x] T018 Update `README.md` to document the new introspection and recipe saving features
- [x] T019 Run full suite of tests including new introspection tests

## Dependencies

- Phase 2 (Blender Introspection) MUST complete before Phase 3 (inspect_tool implementation).
- `save_recipe` implementation depends on `KnowledgeEngine` updates.

## Implementation Strategy

1.  **Backend First**: Implement the Blender side introspection logic first (T004-T007).
2.  **MCP Integration**: Implement the `inspect_tool` on the controller side (T008-T011).
3.  **Recipe Saving**: Implement the recipe saving logic (T012-T016).
4.  **Prompt Update**: Finally, tell the AI about these new powers.
