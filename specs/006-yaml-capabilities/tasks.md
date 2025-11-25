# Implementation Tasks: YAML Capabilities Management

**Feature Branch**: `006-yaml-capabilities`
**Feature Spec**: `specs/006-yaml-capabilities/spec.md`
**Implementation Plan**: `specs/006-yaml-capabilities/plan.md`
**Created**: 2025-11-16

## Phase 1: Setup & Project Initialization

- [X] T001 Add `PyYAML` to the `controller/requirements.txt` file
- [X] T002 Create a new directory `controller/config`
- [X] T003 Create a new file `controller/config/capabilities.yaml` with the example structure from the data model
- [X] T004 Create a new file `controller/config/schema.py` to hold the Pydantic validation models
- [X] T005 Create a new file `controller/config/loader.py` to handle loading, parsing, and validating the YAML file

## Phase 2: User Story 1 - Structured Capability Discovery (P1)

**Goal**: A developer can easily extend capabilities by editing a human-readable YAML file.
**Independent Test**: The Controller loads capabilities from YAML, and the API returns the structured data.

- [X] T006 [US1] Implement the Pydantic models for validation in `controller/config/schema.py`
- [X] T007 [US1] Implement the YAML loading and validation logic in `controller/config/loader.py`
- [X] T008 [US1] Refactor `controller/app/tools.py` to remove the hardcoded `CAPABILITY_PALETTE` and instead import the loaded capabilities from the new config loader
- [X] T009 [US1] Update `controller/app/main.py` to use the new, structured `CapabilityPalette` for validation and API responses
- [X] T010 [US1] Add a unit test in `controller/tests/` to verify that the YAML loader correctly parses a valid file
- [X] T011 [US1] Add a unit test in `controller/tests/` to verify that the loader raises an error for an invalid or missing file

## Phase 3: Polish & Cross-Cutting Concerns

- [X] T012 Update `README.md` and `quickstart.md` to document the new YAML-based configuration
- [X] T013 Review and add logging to the new YAML loading process in `controller/config/loader.py`

## Dependencies

- Phase 1 must be completed before Phase 2.
- Phase 2 implements the core functionality.
- Phase 3 can be addressed after the core functionality is stable.

## Parallel Execution Examples

- **After Phase 1**:
    - T006 (Pydantic models) and T007 (YAML loader logic) can be developed in parallel.

## Implementation Strategy

1.  **MVP**: Complete Phase 1 and 2 to fully transition the capability definition from Python code to the new YAML configuration file.
2.  **Finalization**: Complete Phase 3 to ensure the project documentation is up-to-date.
