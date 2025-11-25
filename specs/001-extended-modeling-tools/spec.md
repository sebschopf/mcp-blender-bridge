# Feature Specification: Extended Modeling Tools

**Feature Branch**: `001-extended-modeling-tools`
**Created**: 2025-11-17
**Status**: Draft
**Input**: User description: "Ajouter les capacités object.rename, object.apply_bevel, object.apply_subsurf, et object.join."

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Scene Organization (Priority: P1)
An artist wants to rename objects to maintain a clean and understandable scene hierarchy, telling the AI, "create a cube and rename it to 'building_base'."

**Why this priority**: Clear naming is fundamental for any complex project, making it easier to target specific objects for modification, animation, or material assignment.

**Independent Test**: The AI can successfully generate and execute an `ActionPlan` that renames the currently active object.

**Acceptance Scenarios**:

1.  **Given** a user prompt "rename the active object to 'MyCustomName'", **When** the AI processes the request, **Then** the active object's name is changed to "MyCustomName".

### User Story 2 - Realistic Hard-Surface Models (Priority: P1)
A modeler wants to add realism to a mechanical part by rounding its sharp edges, asking the AI to "create a cube and apply a bevel to it."

**Why this priority**: Beveling is a core technique in hard-surface modeling to catch light on edges and mimic real-world manufacturing imperfections, drastically improving visual quality.

**Independent Test**: The AI can successfully apply a bevel modifier to an object.

**Acceptance Scenarios**:

1.  **Given** a user prompt "bevel the cube", **When** the AI processes the request, **Then** a bevel modifier is added and applied to the active cube, rounding its edges.

### User Story 3 - Organic Shape Creation (Priority: P1)
A designer wants to create a smooth, organic shape from a simple primitive, instructing the AI to "create a cube and apply a subdivision surface modifier to smooth it out."

**Why this priority**: Subdivision is the primary method for creating high-quality, smooth surfaces for characters, creatures, and complex organic forms. It's a gateway to more advanced modeling.

**Independent Test**: The AI can successfully apply a subdivision surface modifier.

**Acceptance Scenarios**:

1.  **Given** a user prompt "smooth the sphere", **When** the AI processes the request, **Then** a subdivision surface modifier is added and applied, increasing the geometric density and smoothness of the object.

### User Story 4 - Object Management (Priority: P2)
An artist has created several separate objects that form a single logical entity (like parts of a chair) and wants to combine them, telling the AI, "select the 'chair_leg' and 'chair_seat' and join them together."

**Why this priority**: Joining objects simplifies scene management, animation, and modification by treating multiple meshes as a single unit.

**Independent Test**: The AI can successfully join two or more specified objects into a single object.

**Acceptance Scenarios**:

1.  **Given** a user prompt "join 'ObjectA' and 'ObjectB'", **When** the AI processes the request, **Then** it first uses `object.select_multiple` to select both objects, and then calls `object.join` to merge them into a single mesh.

## Requirements *(mandatory)*

### Functional Requirements

-   **FR-001**: A new capability `object.rename` MUST be added to the `capabilities.yaml` file to allow renaming the active object.
-   **FR-002**: A new capability `object.apply_bevel` MUST be added to apply a bevel modifier with a configurable segment count and width.
-   **FR-003**: A new capability `object.apply_subsurf` MUST be added to apply a subdivision surface modifier with a configurable number of subdivision levels.
-   **FR-004**: A new capability `object.join` MUST be added. It will merge all currently selected objects into the active object.
-   **FR-005**: To support the `object.join` command and other future multi-object operations, a new capability `object.select_multiple` MUST be created. This tool will accept a list of object names to select.

### Key Entities

-   **Rename Capability**: `object.rename` tool in `capabilities.yaml`.
-   **Bevel Capability**: `object.apply_bevel` tool in `capabilities.yaml`.
-   **Subdivision Capability**: `object.apply_subsurf` tool in `capabilities.yaml`.
-   **Join Capability**: `object.join` tool in `capabilities.yaml`.

## Success Criteria *(mandatory)*

### Measurable Outcomes

-   **SC-001**: The AI can successfully execute a prompt requiring an object to be renamed.
-   **SC-002**: The AI can successfully execute a prompt requiring a bevel modifier to be applied.
-   **SC-003**: The AI can successfully execute a prompt requiring a subdivision surface modifier to be applied.
-   **SC-004**: The AI can successfully execute a prompt requiring two or more objects to be joined.