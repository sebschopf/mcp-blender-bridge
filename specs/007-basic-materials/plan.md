# Implementation Plan: Basic Material Capabilities

**Feature Branch**: `007-basic-materials`
**Feature Spec**: `specs/007-basic-materials/spec.md`
**Created**: 2025-11-16

## Phase 0: Outline & Research

### Technical Context

-   **Controller**: The changes will be focused on extending the `controller/config/capabilities.yaml` file.
-   **Blender `bpy` API**: The core of this feature involves identifying the correct `bpy` commands to manipulate Blender's node-based material system (Cycles/Eevee). Direct property access like `material.diffuse_color` is legacy and will not work. We must interact with the node tree of the material.
-   **Capabilities**: We will add new tools under the `materials` category in the YAML file. These tools will likely be custom helper functions rather than direct `bpy.ops` calls, as material manipulation is too complex for single-line commands.
-   **NEEDS CLARIFICATION**: What are the precise, idempotent `bpy` commands to:
    1.  Create a new material if it doesn't exist, or get the existing one?
    2.  Assign a material to the active object's first material slot?
    3.  Set the 'Base Color' of the Principled BSDF shader node?
    4.  Set the 'Metallic' value of the Principled BSDF shader node?
    5.  Set the 'Roughness' value of the Principled BSDF shader node?

### Constitution Check & Gate Evaluation

-   ✅ **I. Strict MCP Architecture**: Compliant. The Controller will expose new granular tools, but the validation and execution flow remains the same.
-   ✅ **II. Conversational Interface**: Compliant. This feature directly enables more descriptive, creative conversations.
-   ✅ **III. Granular & Secure Tools**: Compliant. The new tools will be specific and validated (e.g., "set_base_color", not a generic "run_material_script").
-   ✅ **IV. User-Centric Control**: Compliant.
-   ✅ **V. Blender-Native Integration**: Compliant. All operations will use the standard `bpy` API for node-based shading.

**Gate Evaluation**: The feature plan is fully compliant with the project's constitution.

### Research Tasks

-   Research the modern `bpy` API for manipulating Principled BSDF shader nodes in Blender materials.
-   Determine the best practice for creating and assigning materials idempotently (i.e., avoiding duplicates).
-   Design a small set of helper functions that can be exposed as granular tools in the `capabilities.yaml`.

## Phase 1: Design & Contracts

### Data Model (`data-model.md`)

-   The `capabilities.yaml` data model will be extended. The `materials` category will be populated with the new tools identified during research.

### API Contracts (`contracts/openapi.yaml`)

-   No changes are required to the API contract.

### Quickstart Guide (`quickstart.md`)

-   The guide will be updated to demonstrate how to use the new material capabilities with example prompts.

### Agent Context Update

-   No changes are required.