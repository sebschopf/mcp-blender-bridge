# Feature Specification: Dynamic Command Generation

**Feature Branch**: `004-dynamic-command-generation`
**Created**: 2025-11-16
**Status**: Draft
**Input**: User description: "Je veux faire évoluer l'architecture du projet MCP-Blender-Gemini pour passer d'un système d'outils statiques pré-définis à un système de génération de commandes dynamiques et interactives. Le LLM (Gemini) ne doit plus être limité à une liste d'outils finis comme 'create_cube'. À la place, le MCP (le Contrôleur) doit exposer une 'palette' d'opérations 'bpy' de bas niveau qui sont considérées comme sûres. Face à une demande complexe de l'utilisateur (ex: 'fais un bonhomme de neige'), le LLM doit d'abord demander au MCP quelles sont les opérations autorisées. Ensuite, le LLM doit utiliser cette palette pour construire un plan d'action multi-étapes. Ce plan est envoyé au MCP, qui le valide étape par étape et l'exécute séquentiellement dans Blender. L'objectif est que l'utilisateur voie sa création se construire progressivement, et que le système puisse gérer des demandes créatives sans avoir besoin de définir à l'avance un outil pour chaque scénario possible. Cette approche s'inspire du dialogue entre le modèle et le contrôleur décrit par Anthropic dans leur article sur le MCP."

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Dynamic Capability Discovery (Priority: P1)

The AI Model (Gemini) needs to fulfill a complex user request that requires operations not available in a pre-defined toolset. It must dynamically discover the low-level capabilities of the MCP to build a new, valid sequence of commands.

**Why this priority**: This is the foundational step for a flexible system. Without it, the AI is limited to a static list of tools and cannot handle creative, complex requests.

**Independent Test**: The AI can successfully query the MCP for its allowed low-level `bpy` operations and receive a structured list of available functions and their parameters.

**Acceptance Scenarios**:

1.  **Given** the Controller is running, **When** the AI sends a "discover_capabilities" request to a new MCP endpoint, **Then** the Controller returns a JSON object detailing the allowed `bpy` operations (e.g., `bpy.ops.mesh.primitive_cube_add`, `object.location`, `bpy.ops.object.mode_set`).

---

### User Story 2 - Step-by-Step Complex Task Execution (Priority: P1)

A Blender artist issues a complex, multi-step command like "make a snowman". The system engages in a dialogue between the AI and the MCP to construct a plan, and then executes that plan step-by-step, showing the artist the gradual creation of the object.

**Why this priority**: This provides transparency to the user and allows for the execution of creative tasks that go beyond single-tool actions.

**Independent Test**: A user can type "build a snowman" and see a sphere appear, then a smaller sphere on top, then a cone for the nose, demonstrating sequential execution of a dynamically generated plan.

**Acceptance Scenarios**:

1.  **Given** a user requests a "snowman", **When** the AI has discovered the MCP's capabilities, **Then** the AI constructs and sends a multi-step plan to the Controller (e.g., `[{"operation": "bpy.ops.mesh.primitive_uv_sphere_add", "params": {"radius": 1}}, {"operation": "object.location.z.add", "params": {"value": 1}}, {"operation": "bpy.ops.mesh.primitive_uv_sphere_add", "params": {"radius": 0.5}}]`).
2.  **Given** the Controller receives a valid multi-step plan, **When** it begins execution, **Then** it sends the first command to Blender, waits for it to complete, then the second, and so on, in sequence.
3.  **Given** any step in the plan contains an operation not in the MCP's capability list, **Then** the Controller must halt execution before starting, reject the entire plan, and report an error back to the AI.

### Edge Cases

-   **Invalid Operation in Plan**: If the AI generates a plan containing an operation that is not in the MCP's allowed list, the Controller must reject the entire plan before execution.
-   **Execution Failure in Blender**: If a valid step in the plan fails to execute correctly within Blender (e.g., due to an invalid context), the Controller must halt execution of the rest of the plan and report the failure.
-   **Connection Loss Mid-Plan**: If the connection to Blender is lost during the execution of a plan, the system should halt and notify the user that the process was interrupted.

## Requirements *(mandatory)*

### Functional Requirements

-   **FR-001**: The Controller MUST expose a new endpoint (e.g., `/api/mcp/capabilities`) that returns the list of allowed low-level `bpy` operations.
-   **FR-002**: The definition of available tools MUST be refactored from high-level functions (e.g., `create_cube`) to a data structure (e.g., a dictionary or list) that defines the allowed low-level, granular `bpy` operations and their parameter constraints.
-   **FR-003**: The AI's core prompt MUST be updated to instruct it to first query the capabilities endpoint to understand its available actions before attempting to build a plan for any non-trivial request.
-   **FR-004**: The main chat API endpoint MUST be modified to accept a multi-step "Action Plan" from the AI instead of a single tool call.
-   **FR-005**: The Controller MUST validate each step of the received Action Plan against the allowed operations before executing anything.
-   **FR-006**: The Controller MUST execute the Action Plan sequentially, sending one command at a time to the Blender addon and waiting for a success confirmation before sending the next.

### Key Entities

-   **Capability Palette**: A JSON object returned by the Controller that lists all allowed `bpy` operations. Each entry should detail the operation's name and the types of parameters it accepts.
-   **Action Plan**: A JSON array of steps sent from the AI to the Controller. Each step is an object containing the `operation` to be performed and a dictionary of `params` for that operation.

## Success Criteria *(mandatory)*

### Measurable Outcomes

-   **SC-001**: The system can successfully generate a composite 3D object requiring at least 3 sequential steps (e.g., a snowman) from a single natural language prompt.
-   **SC-002**: 100% of attempts to execute a `bpy` operation not explicitly defined in the Capability Palette are rejected by the Controller.
-   **SC-003**: For a 3-step plan, the user sees the first visual change in the Blender scene in under 3 seconds after the AI confirms the plan.
-   **SC-004**: The AI successfully constructs a valid Action Plan for 90% of creative prompts that can be reasonably achieved with the available low-level `bpy` operations.