# Implementation Tasks: Extend Base Modeling Tools (with Token Optimization)

**Feature Branch**: `011-extend-base-tools`
**Feature Spec**: `specs/011-extend-base-tools/spec.md`
**Implementation Plan**: `specs/011-extend-base-tools/plan.md`
**Created**: 2025-11-17

## Phase 1: Foundational - Token Optimization

**Goal**: Implement the two-step tool discovery mechanism to reduce token usage.
**Independent Test**: The API can serve categories and filtered tools, and tests pass.

- [X] T001 In `controller/app/knowledge_engine.py`, add a new method `get_tool_categories()` that returns a list of all top-level category names.
- [X] T002 In `controller/app/knowledge_engine.py`, modify the `get_tool_palette()` method to accept an optional `category` string to filter the returned tools.
- [X] T003 In `controller/app/main.py`, add the new `/discover_categories` endpoint that calls the `get_tool_categories()` method.
- [X] T004 In `controller/app/main.py`, modify the `/discover_capabilities` endpoint to accept the optional `category` query parameter and pass it to the `get_tool_palette()` method.
- [X] T005 In `controller/tests/test_main.py`, add a test for the `/discover_categories` endpoint to ensure it returns the correct list of categories.
- [X] T006 In `controller/tests/test_main.py`, add tests for the `/discover_capabilities` endpoint: one without a filter, one with a valid category, and one with an invalid category (expecting an empty list).
- [X] T007 Run validation tests using `run_tests.bat`.

## Phase 2: User Story 1 - Comprehensive Mesh Editing

**Goal**: The AI can perform complex mesh modeling operations.
**Independent Test**: The AI can generate and execute a plan to create a stylized archway.

- [X] T008 [US1] Create the new capability file `controller/capabilities/mesh/editing.yaml`.
- [X] T009 [P] [US1] In `editing.yaml`, add the `mesh.extrude` tool definition.
- [X] T010 [P] [US1] In `editing.yaml`, add the `mesh.inset` tool definition.
- [X] T011 [P] [US1] In `editing.yaml`, add the `mesh.bevel` tool definition.
- [X] T012 [P] [US1] In `editing.yaml`, add the `mesh.loop_cut` tool definition.
- [X] T013 [P] [US1] In `editing.yaml`, add the `mesh.subdivide` tool definition.
- [X] T014 [US1] In `controller/app/bpy_utils.py`, add the corresponding Python script snippets for all new tools in `editing.yaml`.
- [X] T015 [US1] Create a new test file `controller/tests/test_new_tools.py`.
- [X] T016 [US1] In `controller/tests/test_new_tools.py`, add a test to verify that an Action Plan using `mesh.extrude` and `mesh.bevel` generates the correct `BpyCommand`.
- [X] T017 [US1] Run validation tests using `run_tests.bat`.

## Phase 3: User Story 2 - Advanced Organic Modeling

**Goal**: The AI can create and refine organic shapes using sculpting and retopology.
**Independent Test**: The AI can execute a plan to sculpt a simple head shape and then retopologize it.

- [X] T018 [US2] Create the new capability file `controller/capabilities/sculpt/brushes.yaml`.
- [X] T019 [US2] In `brushes.yaml`, add the generic `sculpt.apply_brush` tool definition.
- [X] T020 [US2] Create a new capability file `controller/capabilities/mesh/retopology.yaml`.
- [X] T021 [US2] In `retopology.yaml`, add the `mesh.retopology.create_quads` tool definition.
- [X] T022 [US2] In `controller/app/bpy_utils.py`, implement the complex Python script for the `sculpt.apply_brush` helper tool.
- [X] T023 [US2] In `controller/app/bpy_utils.py`, add the script snippet for `mesh.retopology.create_quads`.
- [X] T024 [US2] In `controller/tests/test_new_tools.py`, add a test for `sculpt.apply_brush`.
- [X] T025 [US2] Run validation tests using `run_tests.bat`.

## Phase 4: User Story 3 - Full Modifier Stack Access

**Goal**: The AI can use the full range of Blender's modifiers.
**Independent Test**: The AI can create a chain link using `Array` and `Curve` modifiers.

- [X] T026 [US3] Create the new capability file `controller/capabilities/modifiers/generate.yaml`.
- [X] T027 [US3] Create the new capability file `controller/capabilities/modifiers/deform.yaml`.
- [X] T028 [P] [US3] In `generate.yaml`, add tool definitions for `Array`, `Bevel`, `Boolean`, and `Solidify` modifiers.
- [X] T029 [P] [US3] In `deform.yaml`, add tool definitions for `Curve`, `Wave`, and `SimpleDeform` modifiers.
- [X] T030 [US3] In `controller/app/bpy_utils.py`, add the Python helper scripts for the new modifiers.
- [X] T031 [US3] In `controller/tests/test_new_tools.py`, add an integration test for a complex modifier chain.
- [X] T032 [US3] Run validation tests using `run_tests.bat`.

## Phase 5: Polish & Cross-Cutting Concerns

- [X] T033 Review all new tool `description` fields for clarity, conciseness, and accuracy.
- [X] T034 Update `CONTRIBUTING.md` with guidelines for adding new modeling tools and the token optimization strategy.
- [X] T035 Update the AI's core prompt/instructions to use the new two-step discovery process.
- [X] T036 Run a final, full validation using `run_tests.bat` to ensure all tests pass and performance goals are met.

## Dependencies

- Phase 1 must be completed before all other phases.
- Phase 2, 3, and 4 are largely independent and can be worked on in parallel after Phase 1 is complete.
- Phase 5 should be completed last.

## Implementation Strategy

1.  **MVP**: Complete Phase 1. This delivers the core token optimization feature, which is a prerequisite for sustainably adding more tools.
2.  **Expansion**: Complete Phases 2, 3, and 4 to add the new modeling capabilities.
3.  **Finalization**: Complete Phase 5 to ensure documentation and AI instructions are up-to-date.