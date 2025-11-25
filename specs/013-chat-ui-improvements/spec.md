# Feature Specification: Chat UI Improvements

**Feature Branch**: `013-chat-ui-improvements`  
**Created**: vendredi, 21 novembre 2025  
**Status**: Draft  
**Input**: User description: "Améliorer l'interface de chat de l'addon pour afficher dès le début le chat avec l'IA et les états de l'IA, lecture des tools, en attente d'une demande de l'utilisateurice"

## Clarifications

### Session 2025-11-21
- Q: Confirmez-vous la stratégie de refactoring pour résoudre l'interblocage du contrôleur, impliquant la création de `controller/app/globals.py` pour une instance partagée de `KnowledgeEngine` et la modification de `controller/app/internal_tools.py` pour un accès direct à cette instance ? → A: Yes, this refactoring is required to ensure backend stability and prevent timeouts that would degrade the UI experience.

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Always-Visible Chat Interface (Priority: P1)

As a Blender user, I want to see the chat interface and history immediately after the server process starts (even if the AI hasn't responded yet), so that I can see the connection progress and enter commands without delay.

**Why this priority**: Currently, the chat UI is hidden until a specific "CONNECTED" state is reached, which can be delayed by AI initialization or network latency, leaving the user unsure if the system is working.

**Independent Test**: Can be fully tested by clicking "Connect", and immediately verifying that the chat input field and history box are visible while the status is still "Connecting...".

**Acceptance Scenarios**:

1. **Given** the server is stopped, **When** the user clicks "Connect", **Then** the chat history panel and input field appear immediately.
2. **Given** the connection is being established, **When** the UI refreshes, **Then** the chat area remains visible and usable.
3. **Given** the connection fails, **When** the status changes to "Connection Failed", **Then** the chat history remains visible (to show error logs) but the input field might be disabled or show a warning.

### User Story 2 - Explicit AI Status Feedback (Priority: P2)

As a user, I want to see explicit status messages in the chat history indicating what the AI is doing (e.g., "Discovering tools...", "Awaiting instructions"), so that I know the system is active and ready for my input.

**Why this priority**: Users need confirmation that the AI is ready to receive complex commands, especially after the initial connection.

**Independent Test**: Can be tested by connecting and observing the chat history for system messages like "System: Connected. Waiting for AI..." followed by "AI: Ready. I have access to [X] tools. How can I help?".

**Acceptance Scenarios**:

1. **Given** the server connects, **When** the handshake is complete, **Then** a message "System: Connected to MCP Controller" appears in the chat.
2. **Given** the AI is initializing, **When** it is ready, **Then** a message from the AI (e.g., "I'm ready") appears in the chat history.
3. **Given** the chat history is empty, **When** the panel is drawn, **Then** a placeholder message "Waiting for instructions..." is displayed in the list.

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: The Addon UI MUST display the chat history and input field whenever the connection status is `CONNECTING` or `CONNECTED`.
- **FR-002**: The Addon MUST insert a local system message into the chat history upon successful HTTP connection to the Controller.
- **FR-003**: The Controller MUST send an initial "greeting" or status update via the `poll_for_commands` loop once the Gemini client is initialized and tools are loaded.
- **FR-004**: The Addon UI MUST display a "Waiting for instructions..." placeholder in the chat box if the history is empty.
- **FR-005**: The Addon MUST visually distinguish between system messages (connection status), user messages, and AI responses in the chat history (e.g., using prefixes like "System:", "You:", "AI:").

### Non-Functional Requirements

- **NFR-001 (Architecture)**: The Controller MUST be refactored to use a shared `KnowledgeEngine` instance (via a new `globals.py` module) to allow `internal_tools.py` to access tool definitions directly without making blocking HTTP requests to `localhost`. This prevents deadlocks during tool discovery.

### Key Entities *(include if feature involves data)*

- **Chat Message**: Extended to include a `type` or `source` field that supports "SYSTEM" in addition to "USER" and "AI".

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: The time between clicking "Connect" and seeing the chat interface is < 0.1 seconds (immediate UI update).
- **SC-002**: 100% of successful connections result in a visible "System: Connected" message in the chat history.
- **SC-003**: The "Waiting for instructions..." placeholder appears in 100% of cases where the chat history is cleared or empty.
- **SC-004**: System stability: Zero HTTP timeouts caused by internal tool calls (verified by NFR-001 implementation).
