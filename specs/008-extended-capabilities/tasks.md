# Implementation Tasks: Extended Capabilities

**Feature Branch**: `008-extended-capabilities`
**Feature Spec**: `specs/008-extended-capabilities/spec.md`
**Implementation Plan**: `specs/008-extended-capabilities/plan.md`
**Created**: 2025-11-16

## Phase 1: Setup & Configuration

- [X] T001 Update `controller/config/schema.py` to include the new categories: `scene`, `modifiers`, and `staging`.
- [X] T002 [P] [US1] Add the new modeling tools (cylinder, plane, torus) to the `modeling` category in `controller/config/capabilities.yaml`.
- [X] T003 [P] [US2] Add the new transformation tools (rotate, resize) to the `transform` category in `controller/config/capabilities.yaml`.
- [X] T004 [P] [US3] Add the new `scene` category and its tools (select_all, duplicate, delete) to `controller/config/capabilities.yaml`.
- [X] T005 [P] [US4] Add the new `modifiers` category and its tool (modifier_add) to `controller/config/capabilities.yaml`.
- [X] T006 [P] [US5] Add the new `staging` category and its tools (light_add, camera_add) to `controller/config/capabilities.yaml`.

## Phase 2: Testing & Documentation

- [X] T007 Add a unit test to `controller/tests/test_config.py` to ensure the loader correctly parses the newly added categories and tools.
- [X] T008 Update the `quickstart.md` file with examples for each new category of tools.
- [X] T009 Manually test the end-to-end flow with a complex prompt that combines tools from at least three different new categories (e.g., "Create a plane, add a cylinder on top, rotate the cylinder, and add a light.").

## Dependencies

- T001 must be completed before the other tasks in Phase 1.
- The tasks T002 through T006 are parallelizable as they involve editing different, independent sections of the same configuration file.
- Phase 1 must be completed before Phase 2.

## Parallel Execution Examples

- All tasks in Phase 1 (T002-T006) can be executed in parallel after T001 is complete.

## Implementation Strategy

1.  **MVP**: Complete all tasks in Phase 1 to make the full range of new capabilities available to the AI.
2.  **Finalization**: Complete Phase 2 to ensure the new capabilities are tested, documented, and validated.
