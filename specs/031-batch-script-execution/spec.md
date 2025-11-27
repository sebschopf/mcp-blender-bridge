# Feature Specification: Batch Script Execution

**Feature Branch**: `031-batch-script-execution`  
**Created**: 2025-11-27  
**Status**: Draft  
**Input**: User request for batch execution to solve context loss.

## User Scenarios & Testing

### User Story 1 - Batch Execution for Context Retention (Priority: P1)

As a user, I want the AI to generate and execute a single, complete Python script for my request (e.g., "Make a tree and move it") instead of executing one line at a time, so that the AI maintains full context of the variables and objects it creates.

**Why this priority**: Solves the critical "I cannot modify objects" hallucination/failure mode.

**Independent Test**:
- Ask: "Create a cube and move it up 2 units."
- Verify: The system executes ONE bridge command containing both operations.
- Verify: The cube is created AND moved correctly.

**Acceptance Scenarios**:

1. **Given** a multi-step request ("Make a red cube"), **When** the AI processes it, **Then** it generates a single script with creation + material assignment.
2. **Given** a script with multiple dependent steps, **When** executed, **Then** intermediate variables (like `obj = ...`) are preserved and used in subsequent steps.

## Requirements

### Functional Requirements

- **FR-001**: The system MUST provide a `submit_script(script_content: str)` tool to the AI.
- **FR-002**: The AI System Prompt MUST be updated to prioritize `submit_script` over `execute_command` for complex tasks.
- **FR-003**: The `submit_script` tool MUST use the `SecurityValidator` (from Spec 030) to validate the entire script before execution.
- **FR-004**: The `submit_script` tool MUST return the standard output (stdout) of the script execution to the AI.

### Key Entities

- **Script**: A block of valid, safe Python code using `bpy`.
- **BatchCommand**: A new BridgeCommand type (or reuse of `execute_script`) that handles multi-line input.

## Success Criteria

### Measurable Outcomes

- **SC-001**: Complex requests (Create + Modify) succeed in 1 turn instead of failing in 2.
- **SC-002**: Reduction in "I cannot modify" errors.
