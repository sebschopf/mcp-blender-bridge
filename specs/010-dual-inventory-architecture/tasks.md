# Implementation Tasks: Dual Inventory Architecture

**Feature Branch**: `010-dual-inventory-architecture`
**Feature Spec**: `specs/010-dual-inventory-architecture/spec.md`
**Implementation Plan**: `specs/010-dual-inventory-architecture/plan.md`
**Created**: 2025-11-17

## Phase 1: Foundational Architecture & Setup

- [X] T001 Create the new directory structure in `controller/`: `capabilities/`, `knowledge_base/`, and `resources/`.
- [X] T002 Create the main engine file `controller/app/knowledge_engine.py`.
- [X] T003 In `controller/app/models.py`, define the Pydantic models for `Tool`, `ToolCategory`, `Recipe`, and related sub-schemas based on `data-model.md`.
- [X] T004 In `controller/app/knowledge_engine.py`, implement the `KnowledgeEngine` class.
- [X] T005 In `KnowledgeEngine`, implement the file discovery and loading logic to scan YAML files from `capabilities/` and `knowledge_base/`.
- [X] T006 In `KnowledgeEngine`, implement the validation logic that uses the Pydantic models to parse and validate the loaded YAML files.
- [X] T007 Create the test file `controller/tests/test_knowledge_engine.py` with initial setup for mocking the filesystem.

## Phase 2: User Story 1 - Refactor Existing Capabilities

**Goal**: Migrate existing tools to the new architecture to ensure backward compatibility.
**Independent Test**: The AI can execute an Action Plan using a tool like `transform.translate` loaded from the new system.

- [X] T008 [US1] Create `controller/capabilities/object/transforms.yaml` and migrate all transform-related tools from the old `capabilities.yaml` into it.
- [X] T009 [US1] Create `controller/capabilities/mesh/primitives.yaml` and migrate all primitive creation tools.
- [X] T010 [US1] Create `controller/capabilities/object/modifiers.yaml` and migrate all modifier tools.
- [X] T011 [US1] Create `controller/capabilities/object/management.yaml` and migrate remaining object tools (`rename`, `join`, etc.).
- [X] T012 [US1] In `controller/app/main.py`, replace the old capability loading logic with an instance of the new `KnowledgeEngine`.
- [X] T013 [US1] Update the `/discover_capabilities` endpoint to return the tool palette from the `KnowledgeEngine`.
- [X] T014 [US1] Delete the old `controller/config/capabilities.yaml` file.
- [X] T015 [US1] In `controller/tests/test_knowledge_engine.py`, add a test to verify that the engine correctly loads and indexes all the refactored tools from the new YAML files.
- [X] T016 [US1] Run validation tests using `run_tests.bat`.

## Phase 3: User Story 2 - Implement Knowledge Engine Meta-Tools

**Goal**: The AI can interact with the knowledge base to find, use, and save recipes.
**Independent Test**: The AI can generate an Action Plan that successfully uses `knowledge.search_recipes`, `knowledge.execute_recipe`, and `knowledge.save_recipe`.

- [X] T017 [US2] In `controller/app/knowledge_engine.py`, implement the logic for the `knowledge.search_recipes` tool.
- [X] T018 [US2] In `controller/app/knowledge_engine.py`, implement the logic for the `knowledge.execute_recipe` tool, including parameter injection.
- [X] T019 [US2] In `controller/app/knowledge_engine.py`, implement the logic for the `knowledge.save_recipe` tool.
- [X] T020 [US2] Add the new `knowledge` tools to the `capabilities/` inventory, likely in a new file `controller/capabilities/internal/knowledge.yaml`.
- [X] T021 [US2] In `controller/tests/test_knowledge_engine.py`, add unit tests for `search_recipes`, `execute_recipe`, and `save_recipe`.
- [X] T022 [US2] Run validation tests using `run_tests.bat`.

## Phase 4: User Story 3 - Create and Test First Recipe

**Goal**: A developer-defined recipe can be loaded and executed successfully.
**Independent Test**: An Action Plan containing `knowledge.execute_recipe` for a "Simple Table" runs correctly.

- [X] T023 [US3] Create the example recipe file `controller/knowledge_base/furniture/tables/simple_table.yaml` as defined in `quickstart.md`.
- [X] T024 [US3] In `controller/tests/test_knowledge_engine.py`, add a specific integration test that loads and executes the `simple_table.yaml` recipe to validate the end-to-end flow.
- [X] T025 [US3] Run validation tests using `run_tests.bat`.

## Phase 5: Polish & Cross-Cutting Concerns

- [X] T026 Create a `CONTRIBUTING.md` file at the project root and add the guidelines for the extensible classification model.
- [X] T027 Review and update the main `README.md` to reflect the new architecture.
- [X] T028 Run a final, full validation using `run_tests.bat` to ensure no regressions were introduced.

## Dependencies

- Phase 1 must be completed before all other phases.
- Phase 2 must be completed before Phase 3 and 4, as the meta-tools depend on the new tool loading system.
- Phase 3 and 4 can be worked on in parallel.
- Phase 5 should be completed last.

## Parallel Execution Examples

- Within Phase 2, tasks T008, T009, T010, and T011 can be executed in parallel as they involve migrating different sets of tools to different files.
- The implementation of the three meta-tools in Phase 3 (T017, T018, T019) can be done in parallel.

## Implementation Strategy

1.  **MVP**: Complete Phase 1 and Phase 2. This will deliver the core architectural refactoring and ensure the system is stable and backward-compatible.
2.  **Finalization**: Complete Phase 3, 4, and 5 to deliver the full recipe management capabilities and documentation.
