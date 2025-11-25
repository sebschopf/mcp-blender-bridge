# Implementation Tasks: Activate Dynamic AI Logic

**Feature Branch**: `005-activate-dynamic-ai`
**Feature Spec**: `specs/005-activate-dynamic-ai/spec.md`
**Implementation Plan**: `specs/005-activate-dynamic-ai/plan.md`
**Created**: 2025-11-16

## Phase 1: Foundational Components (Blocking Prerequisites)

- [X] T001 Create a new file `controller/app/internal_tools.py` to define the internal AI tools
- [X] T002 In `controller/app/internal_tools.py`, implement the `discover_capabilities` function that makes a GET request to the local `/api/mcp/capabilities` endpoint
- [X] T003 In `controller/app/internal_tools.py`, implement the `submit_action_plan` function that makes a POST request to the local `/api/chat` endpoint
- [X] T004 Refactor `controller/app/main.py` to import and use the new internal tools instead of the old static tool definitions

## Phase 2: User Story 1 - AI-Driven Capability Discovery (P1)

**Goal**: The AI autonomously queries the MCP's capabilities before building a plan.
**Independent Test**: A user prompt triggers the AI to call the `discover_capabilities` tool.

- [X] T005 [US1] Modify the `/api/chat` endpoint in `controller/app/main.py` to present the `discover_capabilities` tool to Gemini on the first turn of a conversation
- [X] T006 [US1] Update the `gemini_client.py` to handle the tool call for `discover_capabilities` and return the palette to the AI

## Phase 3: User Story 2 - AI-Driven Action Plan Formulation (P1)

**Goal**: The AI uses the discovered capabilities to construct and submit a valid `ActionPlan`.
**Independent Test**: After discovering capabilities, the AI's next action is to submit a valid `ActionPlan`.

- [X] T007 [US2] Modify the conversation logic in `controller/app/main.py` to present the `submit_action_plan` tool to Gemini after capabilities have been discovered
- [X] T008 [US2] Update the `gemini_client.py` to handle the tool call for `submit_action_plan` and forward the plan to the `/api/chat` endpoint for execution
- [X] T009 [US2] Add a unit test in `controller/tests/test_main.py` to simulate the full two-step conversation flow (discover, then plan)

## Phase 4: Polish & Cross-Cutting Concerns

- [X] T010 Update the core AI prompt in `GEMINI.md` to be more explicit about the two-step tool-calling process
- [X] T011 Update `quickstart.md` to explain the new internal conversational flow for developers
- [X] T012 Review and enhance logging in `controller/app/main.py` and `controller/app/internal_tools.py` to trace the multi-step AI conversation

## Dependencies

- Phase 1 must be completed before Phase 2 and Phase 3.
- Phase 2 (Discovery) is a strict prerequisite for Phase 3 (Formulation).
- Phase 4 can be completed after the core functionality is stable.

## Parallel Execution Examples

- This feature is highly sequential. The tasks within each phase are dependent on the previous ones. No significant parallel execution is possible.

## Implementation Strategy

1.  **MVP**: Complete Phase 1, 2, and 3 to implement the full, intelligent, two-step conversational loop.
2.  **Finalization**: Complete Phase 4 to ensure all documentation is updated and the system is observable through logging.
