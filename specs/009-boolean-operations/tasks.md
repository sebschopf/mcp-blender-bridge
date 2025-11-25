# Implementation Tasks: Boolean Operations

**Feature Branch**: `009-boolean-operations`
**Feature Spec**: `specs/009-boolean-operations/spec.md`
**Implementation Plan**: `specs/009-boolean-operations/plan.md`
**Created**: 2025-11-16

## Phase 1: Setup & Configuration

- [X] T001 Add the `object.select_by_name` tool to the `scene` category in `controller/config/capabilities.yaml`.
- [X] T002 Add the `object.apply_boolean` tool to the `modifiers` category in `controller/config/capabilities.yaml`.
- [X] T003 Update `controller/config/schema.py` to make the `modifiers` category non-optional if it isn't already.

## Phase 2: User Story 1 & 2 - Boolean Operations (P1)

**Goal**: An artist can engrave or weld objects using natural language.
**Independent Test**: The AI can generate and execute `ActionPlans` that perform `UNION` and `DIFFERENCE` boolean operations.

- [X] T004 [US1] In `controller/app/bpy_utils.py`, add new script snippets for `object.select_by_name` and `object.apply_boolean` to the dictionary returned by the helper function.
- [X] T005 [US1] Update the command generation logic in `controller/app/main.py` to ensure it correctly formats the new boolean and selection script snippets with their parameters.
- [X] T006 [US1] Add a unit test to `controller/tests/test_main.py` to verify that an `ActionPlan` with `object.apply_boolean` generates the correct, multi-line `bpy` script.
- [X] T009 [US3] Add a unit test to `controller/tests/test_main.py` to verify that an `ActionPlan` with `object.apply_boolean` and the `INTERSECT` operation generates the correct `bpy` script.

## Phase 3: Polish & Cross-Cutting Concerns

- [X] T007 Update the `quickstart.md` file with a clear example of a multi-step boolean operation.
- [X] T008 Manually test the end-to-end flow with a prompt like "create a cube, then carve a sphere out of it."

## Dependencies

- Phase 1 must be completed before Phase 2.
- The core logic is in Phase 2.
- Phase 3 is for documentation and final validation.

## Parallel Execution Examples

- T001 and T002 can be done in parallel.

## Implementation Strategy

1.  **MVP**: Complete Phase 1 and 2 to enable the core functionality of boolean operations.
2.  **Finalization**: Complete Phase 3 to ensure the feature is well-documented and robustly tested.
