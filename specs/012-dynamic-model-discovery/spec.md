# Feature Specification: Dynamic Model Discovery

**Feature Branch**: `012-dynamic-model-discovery`  
**Created**: vendredi, 21 novembre 2025  
**Status**: Draft  
**Input**: User description: "récupération dynamique des modèles et mise à jour de l'UI de l'addon pour réfléter les réels modèles que peut utiliser l'utilisateur avec sa clef gemini enregistrer. il faut ajouter un point d'accès à l'API FastAPI du contrôleur."

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Dynamic Model Selection (Priority: P1)

As a Blender user, I want to select the Gemini model I wish to use from a list of available models associated with my API key, so that I can access the latest models or specific versions compatible with my needs without manually editing configuration files.

**Why this priority**: This is critical for usability and reliability. Hardcoded model names lead to errors (e.g., 404 Not Found) as APIs evolve. Users need flexibility to choose models they have access to.

**Independent Test**: Can be fully tested by opening the addon preferences, clicking "Refresh Models", seeing a dropdown populated with valid models, selecting one, and successfully running a command with the chosen model.

**Acceptance Scenarios**:

1. **Given** the Gemini API Key is configured, **When** the user clicks "Refresh Models" in the addon preferences, **Then** the addon fetches the list of available models from the controller and populates the "Model" dropdown.
2. **Given** the model list is populated, **When** the user selects a model (e.g., "gemini-1.5-pro-latest") from the dropdown, **Then** this selection is saved in the preferences.
3. **Given** a model is selected, **When** the user sends a chat message, **Then** the server uses the selected model for processing the request.
4. **Given** the API Key is invalid or network issues occur, **When** the user clicks "Refresh Models", **Then** an error message is displayed in the UI explaining the failure.
5. **Given** the user has a custom model not in the list, **When** the user selects "Custom" from the dropdown, **Then** a text field appears allowing manual entry of the model name.

### User Story 2 - Automatic Environment Variable Fallback (Priority: P2)

As a developer or power user, I want the addon to automatically use my system's `GEMINI_API_KEY` environment variable if I haven't entered one in the preferences, so that I can skip repetitive configuration steps.

**Why this priority**: Improves the "getting started" experience for developers and aligns with standard tool behaviors.

**Independent Test**: Can be tested by clearing the API Key field in preferences, ensuring `GEMINI_API_KEY` is set in the system, restarting Blender/Addon, and successfully connecting to the MCP.

**Acceptance Scenarios**:

1. **Given** the "Gemini API Key" field in preferences is empty and the `GEMINI_API_KEY` environment variable is set, **When** the addon initializes or connects, **Then** it uses the value from the environment variable.
2. **Given** both the preference field and environment variable are empty, **When** the user tries to connect, **Then** an error message prompts the user to configure the API Key.
3. **Given** both are present, **When** the addon connects, **Then** the preference field value takes precedence over the environment variable.

### Edge Cases

- What happens if the selected model is deprecated or removed by Google? The next API call should fail gracefully with an informative error, prompting the user to refresh the model list.
- What happens if the controller API endpoint `/api/models` is unreachable? The addon should handle the connection error and allow the user to manually enter a model name (fallback to Custom).
- How does the system handle models that do not support `generateContent` or tool calling? The controller's list endpoint should filter these out to prevent runtime errors.

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: The Controller MUST expose a new GET endpoint `/api/models` that returns a list of available Gemini models filtered by capability (must support `generateContent` and tool calling).
- **FR-002**: The Addon preferences UI MUST include a "Refresh Models" operator that queries `/api/models` and updates an `EnumProperty` with the results.
- **FR-003**: The Addon preferences UI MUST allow selecting a model from the list or entering a custom model name string.
- **FR-004**: The Addon MUST pass the selected model name to the Controller process upon connection or request (e.g., via `GEMINI_MODEL` environment variable or API parameter).
- **FR-005**: The Controller MUST initialize the Gemini client using the specified model name instead of a hardcoded default.
- **FR-006**: The Addon MUST check for the `GEMINI_API_KEY` environment variable if the preference field is empty.
- **FR-007**: The Addon UI MUST display the current connection status and explicit error messages if model fetching fails.

### Key Entities *(include if feature involves data)*

- **Model List**: A list of strings representing available model names (e.g., `["gemini-1.5-flash", "gemini-1.5-pro", ...]`).
- **Selected Model**: A string preference storing the user's choice.

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: Users can successfully fetch and view a list of at least one valid model within 5 seconds of clicking "Refresh Models" (network permitting).
- **SC-002**: Users can successfully execute a command using a non-default model (e.g., switching from Flash to Pro) without restarting Blender.
- **SC-003**: The system correctly identifies and uses the `GEMINI_API_KEY` from the environment variable in 100% of test cases where the preference field is empty.
- **SC-004**: Reduction of "404 Model Not Found" errors to 0% for users who use the "Refresh Models" feature.