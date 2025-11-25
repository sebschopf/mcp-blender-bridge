# Feature Specification: Basic Material Capabilities

**Feature Branch**: `007-basic-materials`
**Created**: 2025-11-16
**Status**: Draft
**Input**: User description: "Étendre les capacités du MCP pour inclure la gestion des matériaux de base. L'IA doit pouvoir créer des matériaux, changer leur couleur, ajuster leurs propriétés (brillance, rugosité) et appliquer des textures simples."

## User Scenarios & Testing *(mandatory)*

### User Story 1 - AI Can Apply Simple Materials (Priority: P1)

An artist wants to describe the appearance of an object in natural language, such as "make the cube metallic and red," and see the object's material properties update accordingly in Blender.

**Why this priority**: This is the core value proposition of this feature, enabling creative control over object appearance beyond just shape and position.

**Independent Test**: The AI can successfully generate and execute an `ActionPlan` that creates a new material, assigns it to an object, and modifies its base color and metallic properties in response to a user prompt.

**Acceptance Scenarios**:

1.  **Given** a user prompt "create a red metallic sphere", **When** the AI processes the request, **Then** a new sphere is created with a new material applied, and that material has its base color set to red and its metallic property set to a high value (e.g., 1.0).
2.  **Given** an existing object is selected, **When** the user prompts "make this object rough and blue", **Then** the object's material is modified to have a blue base color and a high roughness value.

### Edge Cases

-   **Object has no material slots**: The system should gracefully handle cases where an operation attempts to modify a material on an object with no material slots.
-   **Invalid color/value inputs**: The Controller should reject `ActionPlan` steps with invalid parameter values (e.g., a color specified as a string instead of a tuple).

## Requirements *(mandatory)*

### Functional Requirements

-   **FR-001**: The `capabilities.yaml` file MUST be extended with new tools for basic material manipulation.
-   **FR-002**: New capabilities MUST include, at a minimum:
    -   Creating a new material and assigning it to the active object.
    -   Setting the `base_color` of a material.
    -   Setting the `metallic` property of a material.
    -   Setting the `roughness` property of a material.
-   **FR-003**: The Controller's validation logic MUST be updated to recognize and validate these new material capabilities.
-   **FR-004**: The AI's context/prompting SHOULD be aware of these new capabilities to generate relevant `ActionPlans`.

### Key Entities

-   **Material Capabilities**: A new category in the `capabilities.yaml` file containing tools for material manipulation.

## Success Criteria *(mandatory)*

### Measurable Outcomes

-   **SC-001**: The AI can successfully execute at least 3 different material-related prompts (e.g., changing color, metallic, roughness).
-   **SC-002**: The new material capabilities are exposed and correctly structured in the `/api/mcp/capabilities` endpoint response.