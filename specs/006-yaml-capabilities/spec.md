# Feature Specification: YAML Capabilities Management

**Feature Branch**: `006-yaml-capabilities`
**Created**: 2025-11-16
**Status**: Draft
**Input**: User description: "Je veux refactoriser la gestion des capacités pour les stocker dans un fichier YAML structuré par catégories au lieu d'un dictionnaire Python."

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Structured Capability Discovery (Priority: P1)

A developer wants to easily understand and extend the MCP's capabilities by reading a human-readable, categorized list of available `bpy` operations.

**Why this priority**: This directly addresses the maintainability and extensibility of the system, making it easier for future development and for the AI to reason about capabilities.

**Independent Test**: The Controller successfully loads capabilities from a YAML file, and the `/api/mcp/capabilities` endpoint returns a JSON representation of these structured, categorized capabilities.

**Acceptance Scenarios**:

1.  **Given** a `capabilities.yaml` file exists in the Controller's configuration directory, **When** the Controller starts, **Then** it successfully loads and parses the YAML file into an internal data structure.
2.  **Given** the Controller has loaded the YAML capabilities, **When** the `/api/mcp/capabilities` endpoint is called, **Then** it returns a JSON object that reflects the categorized structure and descriptions defined in the YAML file.

---

### User Story 2 - AI-Enhanced Capability Reasoning (Priority: P2)

The AI Model can leverage the categorized and described capabilities to make more informed decisions when formulating `ActionPlans`.

**Why this priority**: This enhances the intelligence of the AI, allowing it to better understand the context of tools and generate more relevant plans.

**Independent Test**: The AI, when presented with a complex prompt, demonstrates an improved ability to select appropriate tools based on their categories and descriptions, as evidenced by its generated `ActionPlan`.

**Acceptance Scenarios**:

1.  **Given** the AI receives the structured `CapabilityPalette` (from the YAML), **When** it processes a prompt requiring a specific type of action (e.g., "change the material"), **Then** its internal reasoning (as observed through logs or simulated responses) prioritizes tools from the relevant category (e.g., "materials").

### Edge Cases

-   **Invalid YAML Structure**: If the `capabilities.yaml` file contains syntax errors or an invalid structure, the Controller must fail to start with a clear error message.
-   **Missing YAML File**: If the `capabilities.yaml` file is not found, the Controller must fail to start with a clear error message.
-   **Empty Categories/Tools**: The system should gracefully handle empty categories or tool lists within the YAML.

## Requirements *(mandatory)*

### Functional Requirements

-   **FR-001**: The Controller MUST load its `CapabilityPalette` from a YAML file (e.g., `controller/config/capabilities.yaml`) at startup.
-   **FR-002**: The YAML file MUST support a hierarchical structure with categories (e.g., `modeling`, `transform`, `materials`) and descriptions for each category and tool.
-   **FR-003**: The `/api/mcp/capabilities` endpoint MUST return the `CapabilityPalette` in a JSON format that reflects the categorized structure loaded from the YAML.
-   **FR-004**: The Controller MUST include `PyYAML` as a dependency to parse the YAML file.
-   **FR-005**: The Controller MUST validate the loaded YAML structure against a predefined schema to ensure correctness before use.

### Key Entities

-   **Capability YAML File**: A new configuration file (`capabilities.yaml`) storing the structured `bpy` operations.
-   **Categorized Capability Palette**: The in-memory representation of the capabilities, organized by thematic categories.

## Success Criteria *(mandatory)*

### Measurable Outcomes

-   **SC-001**: The Controller successfully starts with a valid `capabilities.yaml` file.
-   **SC-002**: The `/api/mcp/capabilities` endpoint responds with the categorized JSON structure in under 100ms.
-   **SC-003**: A new tool added to the `capabilities.yaml` file is immediately available via the `/api/mcp/capabilities` endpoint after a Controller restart.