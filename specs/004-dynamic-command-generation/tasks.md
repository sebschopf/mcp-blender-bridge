# Implementation Tasks: Dynamic Command Generation

**Feature Branch**: `004-dynamic-command-generation`
**Feature Spec**: `specs/004-dynamic-command-generation/spec.md`
**Implementation Plan**: `specs/004-dynamic-command-generation/plan.md`
**Created**: 2025-11-16

## Phase 1: Foundational Components (Blocking Prerequisites)

- [X] T001 Refactor `controller/app/tools.py` to replace high-level functions with a data structure for the `CapabilityPalette`
- [X] T002 Update Pydantic models in `controller/app/models.py` to include `ActionStep` and `ActionPlan`
- [X] T003 Modify the `CommandRequest` model in `controller/app/models.py` to include an optional `action_plan` field
- [X] T004 Modify the `CommandResponse` model in `controller/app/models.py` to include a `status` field for plan execution

## Phase 2: User Story 1 - Dynamic Capability Discovery (P1)

**Goal**: The AI can discover the MCP's capabilities to build valid command sequences.
**Independent Test**: The AI can successfully query the MCP for its allowed low-level `bpy` operations.

- [X] T005 [US1] Implement the `/api/mcp/capabilities` endpoint in `controller/app/main.py` to return the `CapabilityPalette`
- [X] T006 [US1] Add a unit test for the `/api/mcp/capabilities` endpoint in `controller/tests/test_tools.py`

## Phase 3: User Story 2 - Step-by-Step Complex Task Execution (P1)

**Goal**: A user can issue a complex command and see the object being built step-by-step.
**Independent Test**: A user can type "build a snowman" and see the sequential creation of the object in Blender.

- [X] T007 [US2] Implement the Action Plan validation logic in `controller/app/main.py` within the `/api/chat` endpoint
- [X] T008 [US2] Implement the sequential execution logic for Action Plans in `controller/app/main.py`
- [X] T009 [US2] Modify the `mcp_client.py` in `blender_addon/` to correctly handle sequential commands and report success/failure for each step
- [X] T010 [US2] Update the `command_executor.py` in `blender_addon/` to ensure it can execute the granular `bpy` operations defined in the new palette
- [X] T011 [US2] Add a unit test in `controller/tests/test_main.py` to verify the validation of a correct Action Plan
- [X] T012 [US2] Add a unit test in `controller/tests/test_main.py` to verify the rejection of an incorrect Action Plan

## Phase 4: Polish & Cross-Cutting Concerns

- [X] T013 Update the core AI prompt in `GEMINI.md` with instructions for the new capability discovery and action plan workflow
- [X] T014 Update `README.md` to reflect the new dynamic architecture
- [X] T015 Review and add logging to the new plan execution logic in `controller/app/main.py`

## Dependencies

- Phase 1 must be completed before Phase 2 and Phase 3.
- Phase 2 (Capability Discovery) is a prerequisite for Phase 3 (Plan Execution), as the AI needs to know the tools before creating a plan.
- Phase 4 can be addressed after the core functionality is complete.

## Parallel Execution Examples

- **After Phase 1**:
    - T005 (capabilities endpoint) and T007 (plan validation logic) can be started in parallel as they are distinct pieces of logic within the controller.

## Implementation Strategy

1.  **MVP**: Complete Phase 1, 2, and 3 to deliver the full end-to-end dynamic generation workflow. This is the core value of the feature.
2.  **Finalization**: Complete Phase 4 to ensure documentation and prompts are up-to-date with the new functionality.
