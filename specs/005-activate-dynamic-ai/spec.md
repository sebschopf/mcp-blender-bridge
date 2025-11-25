# Feature Specification: Activate Dynamic AI Logic

**Feature Branch**: `005-activate-dynamic-ai`
**Created**: 2025-11-16
**Status**: Draft
**Input**: User description: "Je veux finaliser l'intégration de la génération de commandes dynamiques. Il faut maintenant mettre à jour la logique de conversation principale dans le contrôleur pour qu'elle utilise le nouveau système. Le processus doit être le suivant : face à une requête utilisateur, le système doit d'abord instruire Gemini d'appeler un outil interne pour découvrir les capacités disponibles (via l'endpoint `/api/mcp/capabilities`). Ensuite, avec cette liste de capacités, le système doit demander à Gemini de construire un 'ActionPlan' détaillé. Finalement, cet ActionPlan est reçu par le contrôleur pour être validé et exécuté. Cela active pleinement l'architecture définie dans la fonctionnalité 004 et remplace l'ancienne logique de 'tool calling' statique."

## User Scenarios & Testing *(mandatory)*

### User Story 1 - AI-Driven Capability Discovery (Priority: P1)

The AI Model, when presented with a user's creative request, needs to autonomously decide to query the MCP's capabilities before attempting to build a plan.

**Why this priority**: This is the first and most critical step in the new dynamic workflow. The AI cannot create a valid plan without first knowing what tools it is allowed to use.

**Independent Test**: When the Controller receives a user prompt, it successfully guides the AI to call an internal `discover_capabilities` tool, which in turn calls the `GET /api/mcp/capabilities` endpoint.

**Acceptance Scenarios**:

1.  **Given** a user sends a new creative prompt (e.g., "build a simple car"), **When** the Controller processes the prompt, **Then** the system's internal logs show that the AI's first action is to call the `discover_capabilities` tool.
2.  **Given** the `discover_capabilities` tool is called, **When** it completes, **Then** the AI receives the `CapabilityPalette` as context for its next step.

---

### User Story 2 - AI-Driven Action Plan Formulation (Priority: P1)

After discovering the available capabilities, the AI Model must use this information to construct a valid, multi-step `ActionPlan` and submit it for execution.

**Why this priority**: This is the second critical step that completes the core AI logic loop, turning the discovered capabilities into an executable strategy.

**Independent Test**: After the `discover_capabilities` tool has been successfully called, the AI's next action is to call an internal `submit_action_plan` tool with a plan that is valid against the discovered capabilities.

**Acceptance Scenarios**:

1.  **Given** the AI has received the `CapabilityPalette`, **When** it processes the user's original prompt again, **Then** it formulates an `ActionPlan` as a JSON object.
2.  **Given** the AI has formulated a plan, **When** it submits this plan via the `submit_action_plan` tool, **Then** the Controller receives the plan on its `/api/chat` endpoint for validation and execution.

### Edge Cases

-   **AI Fails to Discover**: If the AI hallucinates a plan without first calling `discover_capabilities`, the system should guide it back to the correct first step.
-   **AI Creates Invalid Plan**: If the AI creates a plan using operations not listed in the `CapabilityPalette`, the `submit_action_plan` tool should return a validation error, prompting the AI to correct its plan.

## Requirements *(mandatory)*

### Functional Requirements

-   **FR-001**: The Controller's conversational logic MUST be updated to manage a multi-step AI workflow (discover, then plan).
-   **FR-002**: The system MUST provide the AI with a set of internal tools, including at least `discover_capabilities` and `submit_action_plan`.
-   **FR-003**: The `discover_capabilities` tool, when called by the AI, MUST make an HTTP GET request to the `/api/mcp/capabilities` endpoint and return the result to the AI.
-   **FR-004**: The `submit_action_plan` tool, when called by the AI with a plan, MUST make an HTTP POST request to the `/api/chat` endpoint, sending the plan for execution.
-   **FR-005**: The core AI prompt MUST be updated to explicitly instruct the AI to follow the "discover, then plan" sequence.
-   **FR-006**: The system MUST maintain the conversation history, including the results of the capability discovery, so the AI has the necessary context to build the plan.

### Key Entities

-   **Internal AI Tools**: Functions defined within the Controller that are exposed to the Gemini model, such as `discover_capabilities` and `submit_action_plan`. These are distinct from the `bpy` operations.
-   **Conversational State**: The memory of the conversation, which must now track whether capability discovery has been completed.

## Success Criteria *(mandatory)*

### Measurable Outcomes

-   **SC-001**: For a novel, multi-step user prompt, the system's logs show a call to `discover_capabilities` followed by a call to `submit_action_plan`.
-   **SC-002**: 90% of valid user prompts result in the AI successfully generating and submitting a valid `ActionPlan` without human intervention.
-   **SC-003**: The end-to-end process, from user prompt to the Controller receiving a valid `ActionPlan`, takes less than 10 seconds for a simple 3-step plan.