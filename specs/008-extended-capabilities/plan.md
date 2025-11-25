# Implementation Plan: Extended Capabilities

**Feature Branch**: `008-extended-capabilities`
**Feature Spec**: `specs/008-extended-capabilities/spec.md`
**Created**: 2025-11-16

## Phase 0: Outline & Research

### Technical Context

-   **Controller**: All changes will be confined to the `controller/config/capabilities.yaml` file.
-   **Blender `bpy` API**: This feature requires identifying a wide range of `bpy.ops` commands for modeling, transformation, scene management, modifiers, and staging.
-   **No Code Changes**: No Python code changes are anticipated. This feature is purely about expanding the declarative toolset available to the AI. The existing validation and command generation logic is designed to be generic and should support the new tools without modification.

### Constitution Check & Gate Evaluation

-   ✅ **I. Strict MCP Architecture**: Compliant. We are simply adding more tools to the Controller's "allow list".
-   ✅ **II. Conversational Interface**: Compliant. A larger toolset will enable more complex and useful conversations.
-   ✅ **III. Granular & Secure Tools**: Compliant. All new tools will be granular `bpy` operations, maintaining the security model.
-   ✅ **IV. User-Centric Control**: Compliant.
-   ✅ **V. Blender-Native Integration**: Compliant.

**Gate Evaluation**: The feature plan is fully compliant with the project's constitution.

### Research Tasks

-   Identify the most common and useful `bpy.ops` commands for each category:
    -   Modeling (Cylinder, Plane, Torus)
    -   Transformation (Rotate, Resize)
    -   Scene Management (Select, Duplicate, Delete)
    -   Modifiers (Subdivision Surface, Bevel)
    -   Staging (Add Light, Add Camera)
-   For each command, identify its key parameters and their data types to be included in the `capabilities.yaml` file.

## Phase 1: Design & Contracts

### Data Model (`data-model.md`)

-   The `capabilities.yaml` file will be significantly expanded with new categories and tools as identified in the research phase. This file is the primary design artifact for this feature.

### API Contracts (`contracts/openapi.yaml`)

-   No changes are required to the API contract.

### Quickstart Guide (`quickstart.md`)

-   The guide will be updated with a comprehensive list of the new capabilities and example prompts for each category.

### Agent Context Update

-   No changes are required.