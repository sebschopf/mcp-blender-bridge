# Implementation Tasks: Basic Material Capabilities

**Feature Branch**: `007-basic-materials`
**Feature Spec**: `specs/007-basic-materials/spec.md`
**Implementation Plan**: `specs/007-basic-materials/plan.md`
**Created**: 2025-11-16

## Phase 1: Setup

- [X] T001 Update the `controller/config/capabilities.yaml` file to include the new tools under the `materials` category as defined in `data-model.md`
- [X] T002 Create a new file `controller/app/bpy_utils.py` to store helper functions that generate `bpy` script snippets

## Phase 2: User Story 1 - AI Can Apply Simple Materials (P1)

**Goal**: An artist can describe the appearance of an object in natural language and see it updated in Blender.
**Independent Test**: The AI can generate and execute an `ActionPlan` that modifies material properties.

- [X] T003 [US1] In `controller/app/bpy_utils.py`, create a helper function `get_material_script_snippets()` that returns a dictionary of the complex, multi-line `bpy` scripts for each material operation (create/assign, set color, etc.) based on the research.
- [X] T004 [US1] Refactor the command generation logic in `controller/app/main.py` to handle the new material "helper" tools. When it encounters an operation like `materials.set_base_color`, it must look up the corresponding script snippet from `bpy_utils.py` and format it with the parameters from the `ActionStep`.
- [X] T005 [US1] Update the `validate_action_plan` function in `controller/app/main.py` to correctly validate the parameters for the new material tools.
- [X] T006 [US1] Add a unit test to `controller/tests/` to verify that the command generation logic correctly creates the full `bpy` script for a material `ActionStep`.

## Phase 3: Polish & Cross-Cutting Concerns

- [X] T007 Update `quickstart.md` with examples of the new material prompts.
- [X] T008 Manually test the end-to-end flow with a prompt like "create a red metallic sphere" to ensure the AI, Controller, and Blender addon work together correctly.

## Dependencies

- Phase 1 must be completed before Phase 2.
- The core logic is in Phase 2.
- Phase 3 is for documentation and final validation.

## Parallel Execution Examples

- T003 (creating script snippets) and T004 (refactoring the main logic) can be worked on in parallel by different developers, as long as the interface between them (the dictionary of snippets) is agreed upon first.

## Implementation Strategy

1.  **MVP**: Complete Phase 1 and 2 to enable the core functionality of applying basic materials via natural language.
2.  **Finalization**: Complete Phase 3 to ensure the feature is well-documented and robustly tested.
