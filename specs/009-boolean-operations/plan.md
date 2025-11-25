# Implementation Plan: Boolean Operations

**Feature Branch**: `009-boolean-operations`
**Feature Spec**: `specs/009-boolean-operations/spec.md`
**Created**: 2025-11-16

## Phase 0: Outline & Research

### Technical Context

-   **Controller**: The core logic will be implemented in the `controller/app/bpy_utils.py` module. We will add a new helper function to generate the `bpy` script for boolean operations.
-   **Capabilities**: The `controller/config/capabilities.yaml` file will be updated to expose the new boolean tool. A prerequisite tool for selecting objects by name will also be added.
-   **Blender `bpy` API**: Boolean operations are performed by adding a `BOOLEAN` modifier to an object, setting its target object and operation type, and then applying the modifier. This multi-step process is ideal for encapsulation in a helper function.
-   **NEEDS CLARIFICATION**: What is the most robust `bpy` sequence to:
    1.  Select an object by its name?
    2.  Add a boolean modifier to the active object?
    3.  Set the target object for the modifier by name?
    4.  Apply the modifier and then delete the target object?

### Constitution Check & Gate Evaluation

-   ✅ **I. Strict MCP Architecture**: Compliant. The complex logic is encapsulated in the Controller, and only a granular, validated tool is exposed to the AI.
-   ✅ **II. Conversational Interface**: Compliant. Enables more powerful modeling conversations.
-   ✅ **III. Granular & Secure Tools**: Compliant. The new tool is specific and secure.
-   ✅ **IV. User-Centric Control**: Compliant.
-   ✅ **V. Blender-Native Integration**: Compliant. Uses the standard `bpy` modifier system.

**Gate Evaluation**: The feature plan is fully compliant with the project's constitution.

### Research Tasks

-   Research the `bpy` API for selecting objects by name.
-   Research the full, robust sequence for adding, configuring, applying, and cleaning up a `BOOLEAN` modifier via script.

## Phase 1: Design & Contracts

### Data Model (`data-model.md`)

-   The `capabilities.yaml` data model will be extended with two new tools: `object.select_by_name` and `object.apply_boolean`.

### API Contracts (`contracts/openapi.yaml`)

-   No changes are required to the API contract.

### Quickstart Guide (`quickstart.md`)

-   The guide will be updated to explain how the AI can now perform boolean operations, with a clear example prompt like "carve a hole in a cube with a sphere."

### Agent Context Update

-   No changes are required.