# Implementation Plan: Dynamic Command Generation

**Feature Branch**: `004-dynamic-command-generation`
**Feature Spec**: `specs/004-dynamic-command-generation/spec.md`
**Created**: 2025-11-16

## Phase 0: Outline & Research

### Technical Context

-   **Controller**: The existing FastAPI application (`controller/app/main.py`) will be modified. It's built on Python with Pydantic for data modeling.
-   **Blender Addon**: The existing addon (`blender_addon/`) will require minimal changes, primarily to ensure it correctly reports success/failure for each command, but the core logic of receiving and executing commands remains the same.
-   **AI Model (Gemini)**: The core prompt engineering will need to be updated to incorporate the new dynamic capability discovery workflow. This is a configuration change, not a code change.
-   **Communication**: The communication between the addon and the controller is synchronous HTTP requests. This will be maintained for the sequential execution of the action plan.

### Constitution Check & Gate Evaluation

A review of the feature spec against the `constitution.md` confirms the following:

-   ✅ **I. Strict MCP Architecture**: The proposed design strengthens this principle. The AI generates a plan, but the Controller retains full authority over validation and translation into safe, low-level commands. The AI never gains direct execution privileges.
-   ✅ **II. Conversational Interface**: This feature is a direct enhancement of the conversational interface, allowing the AI to have a more informed "dialogue" with the MCP to understand its capabilities before presenting a plan to the user.
-   ✅ **III. Granular & Secure Tools**: This is the core of the feature. We are moving from high-level tools to a curated list of granular, low-level `bpy` operations, which increases both security and flexibility.
-   ✅ **IV. User-Centric Control**: The user will see the step-by-step execution of the plan, providing greater transparency and control over the creative process.
-   ✅ **V. Blender-Native Integration**: All generated commands will continue to be executed through the `bpy` API, ensuring full compliance.

**Gate Evaluation**: The feature plan is fully compliant with the project's constitution.

### Research Tasks

No significant research is required. The plan involves extending existing patterns within the established technology stack (FastAPI, Python, Blender's `bpy` API). The core challenge is in the implementation logic, not in technology selection. A `research.md` file will be created but will state that no research was necessary.

## Phase 1: Design & Contracts

### Data Model (`data-model.md`)

The primary data structures to be formalized are the `CapabilityPalette` and the `ActionPlan`.

-   **CapabilityPalette**: A JSON object. The top-level keys will be the allowed `bpy` operations (e.g., `"bpy.ops.mesh.primitive_uv_sphere_add"`). The value for each key will be an object detailing the allowed parameters and their expected types (e.g., `{"radius": "float", "location": "tuple"}`).
-   **ActionPlan**: A JSON array of `ActionStep` objects.
-   **ActionStep**: A JSON object with two keys:
    -   `operation`: A string that must match a key in the `CapabilityPalette`.
    -   `params`: A dictionary of parameter names and values for the given operation.

### API Contracts (`contracts/openapi.yaml`)

The existing `/api/chat` endpoint will be modified, and a new `/api/mcp/capabilities` endpoint will be added.

-   **`GET /api/mcp/capabilities`**:
    -   **Description**: Allows the AI Model to discover the available low-level `bpy` operations.
    -   **Response (200 OK)**: `application/json` containing the `CapabilityPalette` object.
-   **`POST /api/chat`**:
    -   **Description**: Receives a user prompt and, in subsequent turns, an `ActionPlan` from the AI for execution.
    -   **Request Body**: The `CommandRequest` model will be updated to include an optional `action_plan` field (an array of `ActionStep` objects).
    -   **Response (200 OK)**: The `CommandResponse` will be adapted. For an incoming `ActionPlan`, the response will be a stream of updates as each step is executed, or a final confirmation/error message.

### Quickstart Guide (`quickstart.md`)

The quickstart guide will be updated to reflect the new workflow for developers or advanced users:
1.  Explain the purpose of the `/api/mcp/capabilities` endpoint.
2.  Detail the new structure of the `ActionPlan` that the `/api/chat` endpoint expects.
3.  Provide an example `curl` command for both endpoints.

### Agent Context Update

The `GEMINI.md` or equivalent agent context file will be updated to include:
-   Instructions for the AI to query `/api/mcp/capabilities` first.
-   The expected structure for the `ActionPlan`.
-   An example of a full interaction flow (User Prompt -> AI queries capabilities -> AI builds plan -> AI sends plan).