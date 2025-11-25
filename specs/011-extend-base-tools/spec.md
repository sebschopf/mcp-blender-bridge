# Feature Specification: Extend Base Modeling Tools

**Feature Branch**: `011-extend-base-tools`  
**Created**: 2025-11-17  
**Status**: Draft  
**Input**: User description: "J'aimerais que la liste d'outils de base (tool) soit plus complètes. https://docs.blender.org/manual/fr/dev/modeling/index.html"

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Comprehensive Mesh Editing (Priority: P1)

As a 3D artist, I want the AI to have access to a complete suite of mesh editing tools so that I can perform complex modeling operations (like extruding, beveling, and subdividing) on any part of my mesh using natural language.

**Why this priority**: This is the absolute foundation of modeling. Without a rich set of mesh manipulation tools, the AI's ability to create anything beyond simple primitives is severely limited.

**Independent Test**: The AI can successfully generate and execute an Action Plan to create a complex shape (e.g., a stylized archway) that requires a sequence of creation, selection, extrusion, and beveling operations.

**Acceptance Scenarios**:

1. **Given** a simple cube, **When** I ask "extrude the top face upwards and then bevel its edges", **Then** the AI generates a plan using `mesh.extrude` and `mesh.bevel` tools, and Blender executes it correctly.
2. **Given** a plane, **When** I ask "subdivide it three times", **Then** the AI uses a `mesh.subdivide` tool, and the plane's geometry is correctly subdivided.

---

### User Story 2 - Advanced Organic Modeling (Priority: P2)

As a character artist, I want the AI to be able to use sculpting and retopology tools so that I can create and refine organic shapes like characters, creatures, or natural landscapes.

**Why this priority**: This unlocks a completely new domain of creation that is impossible with basic mesh editing alone. It allows for more artistic and less mechanical modeling workflows.

**Independent Test**: The AI can execute a plan to create a basic organic form. For example, starting with a sphere, applying a sculpting brush to create a simple head shape, and then using a retopology tool to create a cleaner, low-poly mesh over the sculpt.

**Acceptance Scenarios**:

1. **Given** a sphere, **When** I ask "sculpt a simple nose on the front of this sphere", **Then** the AI generates a plan that activates sculpt mode and uses a sculpting tool (e.g., `sculpt.draw_brush`) to modify the sphere's shape.
2. **Given** a high-poly sculpted mesh, **When** I ask "create a clean, low-poly version of this model", **Then** the AI generates a plan that uses a retopology tool (e.g., `mesh.retopology.create_quads`) to generate a new, simplified mesh.

---

### User Story 3 - Full Modifier Stack Access (Priority: P3)

As a hard-surface modeler, I want the AI to be able to add, configure, and apply any modifier from Blender's modifier stack so that I can perform non-destructive modeling workflows and create complex objects efficiently.

**Why this priority**: Modifiers are a cornerstone of efficient modeling in Blender. Giving the AI full access to them dramatically increases its power and flexibility, allowing it to create objects that would be tedious to model by hand.

**Independent Test**: The AI can successfully create an object that relies on a combination of modifiers. For example, creating a chain link by using an `Array` modifier on a torus, followed by a `Curve` modifier to make it follow a path.

**Acceptance Scenarios**:

1. **Given** a cube, **When** I ask "add a wireframe modifier to it and make the wires thicker", **Then** the AI generates a plan that adds a `Wireframe` modifier and then modifies its `thickness` parameter.
2. **Given** a plane, **When** I ask "make it look like a wavy flag", **Then** the AI adds a `Wave` modifier to the plane.

---

### Edge Cases

- What happens if a tool from the documentation has no direct equivalent in the `bpy.ops` API? The tool should be omitted, and a note should be made for potential future implementation via a custom script.
- How does the system handle tools that require interactive user input (e.g., drawing a curve)? These tools will be marked as such and may require a different execution model or be deferred.

## Clarifications

### Session 2025-11-17
- Q: Comment l'IA doit-elle obtenir la liste des catégories d'outils disponibles ? → A: Créer un nouvel endpoint dédié, par exemple `/discover_categories`, qui retourne simplement la liste des noms de catégories (ex: `["mesh", "sculpt", "modifiers"]`).

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: The system MUST expand its `capabilities/` inventory to include a comprehensive set of tools based on the Blender manual's "Modeling" section.
- **FR-002**: The new tools MUST be organized into a logical, hierarchical structure within the `capabilities/` directory, following the existing data models (e.g., `mesh/`, `sculpt/`, `modifiers/`).
- **FR-003**: Each new tool definition in the YAML files MUST conform to the `Tool` Pydantic model, including a clear `name`, `description`, and a full definition of its `params`.
- **FR-004**: The expansion MUST include tools for basic mesh editing (e.g., extrude, inset, bevel, loop cut, subdivide).
- **FR-005**: The expansion MUST include tools for organic modeling, covering basic sculpting brushes (e.g., draw, clay, grab) and retopology operations.
- **FR-006**: The expansion MUST include tools for adding, configuring, and applying all major geometry modifiers (e.g., Array, Bevel, Boolean, Solidify, Subdivision Surface, Wireframe, Wave).
- **FR-007**: The `description` for each tool MUST be clear and descriptive enough for the AI to understand its purpose and when to use it.
- **FR-008**: The system MUST provide a new endpoint `/discover_categories` that returns a simple JSON list of all available tool category names.
- **FR-009**: When the `/discover_capabilities` endpoint is called with a `category` parameter that does not correspond to an existing category, the system MUST return an HTTP 200 (OK) response with an empty list `[]`.
- **FR-010**: The AI's default strategy for tool discovery MUST be to first call `/discover_categories` to get available categories, then select relevant categories, and finally call `/discover_capabilities?category=X` for specific tools.

### Key Entities *(include if feature involves data)*

- **Tool**: Represents a single, atomic operation the AI can perform. The new tools will be added as instances of this existing entity.
- **ToolCategory**: Represents a logical grouping of tools. New categories (e.g., `sculpt`, `retopology`) will be created.

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: At least 80% of the distinct modeling operations listed in the Blender manual's "Modeling", "Sculpting", and "Modifiers" sections are represented as tools in the `capabilities/` inventory.
- **SC-002**: The AI can successfully generate and execute an Action Plan for at least 3 distinct, complex modeling tasks that were impossible with the previous, limited toolset (e.g., creating a detailed piece of furniture, sculpting a simple character head, creating a procedural object with modifiers).
- **SC-003**: A review of the new tool descriptions by a human expert confirms that at least 95% are clear, accurate, and sufficient for an AI to make correct decisions.
- **SC-004**: The startup time of the Controller MUST NOT increase by more than 20% after adding the new, comprehensive set of tool files.
- **SC-005**: The average token usage for tool discovery (from initial user request to final Action Plan generation) MUST be reduced by at least 50% compared to a full `/discover_capabilities` call without filtering.