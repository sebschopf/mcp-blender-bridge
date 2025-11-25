# Feature Specification: Boolean Operations

**Feature Branch**: `009-boolean-operations`
**Created**: 2025-11-16
**Status**: Draft
**Input**: User description: "Ajouter la capacité d'effectuer des opérations booléennes (graver, souder) entre les objets."

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Geometric Subtraction (Engraving) (Priority: P1)
An artist wants to carve a shape out of an object, telling the AI, "create a cube, then use a sphere to carve a hole in its center."

**Why this priority**: This is a fundamental modeling technique that unlocks a vast range of hard-surface modeling possibilities, from architectural details to complex mechanical parts.

**Independent Test**: The AI can successfully generate and execute an `ActionPlan` that creates two intersecting objects and then uses one to subtract from the other.

**Acceptance Scenarios**:

1.  **Given** a user prompt "carve a hole in the cube with a cylinder", **When** the AI processes the request, **Then** it creates a cube and a cylinder, positions them to intersect, applies a boolean `DIFFERENCE` operation, and removes the cylinder, leaving a hole in the cube.

### User Story 2 - Geometric Union (Welding) (Priority: P1)
A designer wants to seamlessly merge two separate objects into a single, continuous mesh, asking the AI to "create a cube and a sphere next to it, then weld them together."

**Why this priority**: This allows for the creation of complex, organic, and solid shapes from simpler components.

**Independent Test**: The AI can successfully generate and execute an `ActionPlan` that creates two objects and merges them into one using a boolean `UNION` operation.

**Acceptance Scenarios**:

1.  **Given** a user prompt "join a cube and a sphere", **When** the AI processes the request, **Then** it creates a cube and a sphere, positions them to intersect, and applies a boolean `UNION` operation, resulting in a single, combined mesh.

### User Story 3 - Geometric Intersection (Priority: P2)
A modeler needs to create a complex shape that represents the common volume between two intersecting objects, asking the AI to "keep only the intersection of a cube and a sphere."

**Why this priority**: This operation is crucial for advanced modeling, enabling the creation of intricate shapes and components defined by overlapping geometries.

**Independent Test**: The AI can successfully generate and execute an `ActionPlan` that creates two intersecting objects and calculates their common volume using a boolean `INTERSECT` operation.

**Acceptance Scenarios**:

1.  **Given** a user prompt "find the intersection of a cube and a sphere", **When** the AI processes the request, **Then** it creates and intersects a cube and a sphere, applies a boolean `INTERSECT` operation, and removes the original objects, leaving only the new mesh representing their shared volume.

## Requirements *(mandatory)*

### Functional Requirements

-   **FR-001**: A new helper function MUST be created in the Controller to handle the multi-step logic of applying a boolean modifier.
-   **FR-002**: The `capabilities.yaml` file MUST be extended with a new tool, `object.apply_boolean`.
-   **FR-003**: The `object.apply_boolean` tool MUST accept parameters for the target object and the operation type (`'UNION'`, `'DIFFERENCE'`, `'INTERSECT'`).
-   **FR-004**: The Controller's command generation logic MUST be updated to correctly call the new boolean helper function.
-   **FR-005**: The AI must be able to select objects by name to specify the target for the boolean operation. A new capability `object.select_by_name` might be required.

### Key Entities

-   **Boolean Helper Function**: A new Python function in the Controller that encapsulates the `bpy` logic for boolean operations.
-   **Boolean Capability**: The new `object.apply_boolean` tool defined in `capabilities.yaml`.

## Success Criteria *(mandatory)*

### Measurable Outcomes

-   **SC-001**: The AI can successfully execute a prompt requiring a `DIFFERENCE` operation (e.g., "make a cube with a hole").
-   **SC-002**: The AI can successfully execute a prompt requiring a `UNION` operation (e.g., "merge two spheres").
-   **SC-003**: The new `object.apply_boolean` capability is exposed and correctly structured in the `/api/mcp/capabilities` endpoint response.
-   **SC-004**: The AI can successfully execute a prompt requiring an `INTERSECT` operation (e.g., "find the common area between a cube and sphere").