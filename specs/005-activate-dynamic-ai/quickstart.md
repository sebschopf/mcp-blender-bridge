# Quickstart: Activate Dynamic AI Logic

This feature refactors the internal conversational logic of the Controller. The external API contract for the Blender addon and other clients remains unchanged.

## End-to-End Internal Conversational Flow

From a developer's perspective, the system now follows an intelligent, two-step internal process orchestrated by the `GeminiClient` to respond to a user's creative prompt.

1.  **User Prompt**: A user sends a message to the `/api/chat` endpoint (e.g., "build a snowman"). The endpoint receives the request and passes it to the `GeminiClient`.

2.  **Internal Step 1: Capability Discovery**:
    -   The `GeminiClient` instructs the Gemini model to use the `discover_capabilities` internal tool.
    -   This tool makes a `GET` request to the Controller's own `/api/mcp/capabilities` endpoint.
    -   The resulting `CapabilityPalette` is sent back to the Gemini model as the result of the tool call.

3.  **Internal Step 2: Action Plan Formulation**:
    -   The `GeminiClient` continues the conversation, now with the `CapabilityPalette` in the context.
    -   It instructs the Gemini model to use the `submit_action_plan` internal tool.
    -   The Gemini model generates the `ActionPlan` based on the user's prompt and the palette.
    -   The `submit_action_plan` tool makes a `POST` request to the Controller's own `/api/chat` endpoint, this time including the `action_plan`.

4.  **Execution**:
    -   The `/api/chat` endpoint receives the request with the `action_plan`.
    -   It validates the plan and returns a `CommandResponse` with the list of `BpyCommands` for the Blender addon to execute.

This entire internal loop is abstracted from the end-user, who simply provides a prompt and sees the final result.
