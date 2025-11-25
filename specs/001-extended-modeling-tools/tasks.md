# Implementation Tasks: Extended Modeling Tools

**Feature Branch**: `001-extended-modeling-tools`
**Feature Spec**: `specs/001-extended-modeling-tools/spec.md`
**Implementation Plan**: `specs/001-extended-modeling-tools/plan.md`
**Created**: 2025-11-17

## Phase 1: Setup & Configuration

- [X] T001 [P] Add the new `object` category with the `object.rename`, `object.select_multiple`, and `object.join` tools to `controller/config/capabilities.yaml`.
- [X] T002 [P] Add the `object.apply_bevel` and `object.apply_subsurf` tools to the `modifiers` category in `controller/config/capabilities.yaml`.
- [X] T003 Update `controller/config/schema.py` to include the new optional `object` category.

## Phase 2: User Story 1 - Rename (P1)

**Goal**: An artist can rename objects for better scene organization.
**Independent Test**: The AI can generate and execute an `ActionPlan` that renames the active object.

- [X] T004 [US1] In `controller/app/bpy_utils.py`, add a new script snippet for `object.rename`.
- [X] T005 [US1] Add a unit test to `controller/tests/test_main.py` to verify that an `ActionPlan` with `object.rename` generates the correct `bpy` script.

## Phase 3: User Story 2 - Bevel (P1)

**Goal**: A modeler can add realism to models by beveling edges.
**Independent Test**: The AI can generate and execute an `ActionPlan` that applies a bevel modifier.

- [X] T006 [US2] In `controller/app/bpy_utils.py`, add a new script snippet for `object.apply_bevel`.
- [X] T007 [US2] Add a unit test to `controller/tests/test_main.py` to verify the script generation for `object.apply_bevel`.

## Phase 4: User Story 3 - Subdivision Surface (P1)

**Goal**: A designer can create smooth, organic shapes from simple primitives.
**Independent Test**: The AI can generate and execute an `ActionPlan` that applies a subdivision surface modifier.

- [X] T008 [US3] In `controller/app/bpy_utils.py`, add a new script snippet for `object.apply_subsurf`.
- [X] T009 [US3] Add a unit test to `controller/tests/test_main.py` to verify the script generation for `object.apply_subsurf`.

## Phase 5: User Story 4 - Join Objects (P2)

**Goal**: An artist can combine multiple objects into a single mesh.
**Independent Test**: The AI can join two or more objects into one.

- [X] T010 [US4] In `controller/app/bpy_utils.py`, add a new script snippet for `object.select_multiple`.
- [X] T011 [US4] In `controller/app/bpy_utils.py`, add a new script snippet for `object.join`.
- [X] T012 [US4] Add unit tests to `controller/tests/test_main.py` to verify the script generation for both `object.select_multiple` and `object.join`.

## Phase 6: Polish & Cross-Cutting Concerns

- [X] T013 Update the `quickstart.md` file in `specs/001-extended-modeling-tools/` with examples for all new tools.
- [X] T014 Manually test the end-to-end flow for each of the four user stories.

## Dependencies

- Phase 1 must be completed before all other phases.
- User Story phases (2, 3, 4, 5) can be implemented in parallel after Phase 1 is complete.
- Phase 6 should be completed last.

## Parallel Execution Examples

- T001 and T002 can be done in parallel.
- The implementation and testing tasks within each user story phase (e.g., T004 and T005) are sequential.
- The user story phases themselves (Phase 2, 3, 4, 5) are independent and can be worked on in parallel.

## Implementation Strategy

1.  **MVP**: Complete Phase 1 and all P1 User Stories (Phases 2, 3, 4) to deliver the core modeling improvements.
2.  **Finalization**: Complete the P2 User Story (Phase 5) and the final polish phase (Phase 6).
