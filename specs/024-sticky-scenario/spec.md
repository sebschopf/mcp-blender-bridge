# Feature Specification: Sticky Scenario Routing

**Feature Branch**: `024-sticky-scenario`  
**Created**: 2025-11-25  
**Status**: Draft  
**Input**: User description: "Le système de routage de scénarios doit être 'collant' (sticky). Une fois qu'une session est entrée dans un scénario spécifique (ex: 'character', 'prop'), elle doit y rester pour les messages suivants, à moins que le routeur ne détecte explicitement une intention de changement de contexte fort ou une demande d'annulation. Cela évite de repasser en mode 'contextual' par défaut lors des réponses de clarification de l'utilisateur."

## User Scenarios & Testing

### User Story 1 - Scenario Persistence (Priority: P1)

Users need the system to remember the current task context (e.g., "creating a prop") across multiple turns of conversation, even if subsequent messages are short or ambiguous (e.g., "make it blue", "go").

**Why this priority**: Solves the critical bug where the system "forgets" it is in a specialized workflow and falls back to a generic, less capable mode, breaking multi-step interactions.

**Independent Test**:
- Send "Create a prop" -> Verify system enters `prop` scenario.
- Send "Make it red" -> Verify system STAYS in `prop` scenario (and doesn't switch to `contextual`).
- Send "Cancel" or "Start over" -> Verify system resets to `contextual` or re-evaluates.

**Acceptance Scenarios**:

1. **Given** a user is in the `prop` scenario, **When** they send a follow-up instruction like "add texture", **Then** the system processes it using the `prop` scenario prompt.
2. **Given** a user is in the `character` scenario, **When** they send "change style to cartoon", **Then** the system remains in `character` scenario.
3. **Given** a user is in any scenario, **When** they explicitly say "Stop" or "New task", **Then** the system resets the sticky state and re-routes.

### Edge Cases

- **Ambiguous Switch**: If the user says something that *could* be a new task but is ambiguous, prefer staying in the current scenario until a clear break is detected.
- **Long Sessions**: The sticky state should persist for the duration of the session or until explicitly cleared.

## Requirements

### Functional Requirements

- **FR-001**: The `ChatService` MUST maintain a `current_scenario` state per session.
- **FR-002**: The `IntentRouter` logic MUST take the `current_scenario` into account.
    - If `current_scenario` is set, the router should bias towards keeping it unless the new intent is essentially "exit" or "new task".
    - Alternatively, bypass routing for follow-up messages and only re-route on explicit triggers (to be decided in design).
- **FR-003**: A new intent type or keyword (e.g., `reset`, `cancel`) MUST be detectable to clear the sticky scenario.
- **FR-004**: When a scenario is active, the system prompt loaded MUST be the one for that scenario, regardless of the specific content of the latest user message (unless it triggers a reset).

### Key Entities

- **SessionState**: Updated to include `active_scenario` (string, nullable).

## Success Criteria

### Measurable Outcomes

- **SC-001**: 100% of follow-up messages in a task flow (e.g., "continue", "yes", "blue") retain the initial scenario.
- **SC-002**: Users can successfully exit a scenario with natural language (e.g., "stop", "let's do something else").