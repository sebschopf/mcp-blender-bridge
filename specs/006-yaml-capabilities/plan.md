# Implementation Plan: YAML Capabilities Management

**Feature Branch**: `006-yaml-capabilities`
**Feature Spec**: `specs/006-yaml-capabilities/spec.md`
**Created**: 2025-11-16

## Phase 0: Outline & Research

### Technical Context

-   **Controller**: The changes will be focused on the FastAPI application. We will introduce a new configuration module to handle the loading and validation of the YAML file.
-   **Dependencies**: The `PyYAML` library will be added to `controller/requirements.txt` to handle YAML parsing.
-   **Configuration**: A new directory `controller/config/` will be created to store the `capabilities.yaml` file, separating configuration from application code.
-   **Validation**: We will use Pydantic models to define a schema and validate the structure of the loaded YAML data, ensuring its integrity at startup.

### Constitution Check & Gate Evaluation

-   ✅ **I. Strict MCP Architecture**: This change improves the maintainability of the Controller's validation logic but does not alter the core MCP flow.
-   ✅ **II. Conversational Interface**: By providing a richer, structured context to the AI, this change enhances its ability to engage in more intelligent conversations.
-   ✅ **III. Granular & Secure Tools**: This refactoring makes the definition and management of granular tools cleaner and more robust. Security is maintained as the Controller is still the sole authority for validation.
-   ✅ **IV. User-Centric Control**: No direct impact, but a more capable AI can lead to better user outcomes.
-   ✅ **V. Blender-Native Integration**: No impact.

**Gate Evaluation**: The feature plan is fully compliant with the project's constitution.

### Research Tasks

No research is required. The use of `PyYAML` for parsing and Pydantic for validation are standard, well-documented practices in the Python ecosystem. A `research.md` file will be created to document this.

## Phase 1: Design & Contracts

### Data Model (`data-model.md`)

-   **Pydantic Validation Models**: New Pydantic models will be created (e.g., in `controller/config/schema.py`) to define the expected structure of the `capabilities.yaml` file. This will include models for `Parameter`, `Tool`, and `Category`.
-   **Capability YAML File**: The structure of the `capabilities.yaml` file itself will be the primary data model artifact.

### API Contracts (`contracts/openapi.yaml`)

No changes are required to the API contract. The `/api/mcp/capabilities` endpoint will still return the same JSON structure, but the source of that data will now be the YAML file instead of a hardcoded Python dictionary.

### Quickstart Guide (`quickstart.md`)

The quickstart guide will be updated to:
1.  Explain the new `controller/config/capabilities.yaml` file and its purpose.
2.  Show an example of how to add a new tool to the YAML file.
3.  Mention the new `PyYAML` dependency.

### Agent Context Update

No changes are required to the agent context. The AI will continue to receive the same JSON structure from the capabilities endpoint; the change is purely internal to the Controller.