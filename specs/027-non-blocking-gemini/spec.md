# Feature Specification: Non-Blocking Gemini API Calls

**Feature Branch**: `027-non-blocking-gemini`  
**Created**: 2025-11-25  
**Status**: Draft  
**Input**: User description: "Rendre l'appel à l'API Gemini (chat.send_message) non bloquant dans le Client du controleur. l'appel synchrone bloque le thread Uvicorn. Cela empèche le serveur de traiter les requêtes Bridge de Blender et cause des timeouts."

## User Scenarios & Testing

### User Story 1 - Concurrent Request Handling (Priority: P1)

The MCP Controller must be able to handle incoming requests (like polling from Blender's BridgeClient) *while* it is waiting for a response from the Gemini API.

**Why this priority**: Critical bug fix. Currently, the synchronous Gemini call blocks the single Uvicorn worker, causing a deadlock where the server waits for Blender to execute a tool, but cannot receive Blender's polling request for that tool.

**Independent Test**:
- Start the server.
- Initiate a long-running chat request that triggers a tool execution.
- Simultaneously (while the chat is processing), attempt to hit the `/internal/get_command` endpoint (simulating Blender polling).
- Verify that `/internal/get_command` returns immediately (or within its timeout) and is not blocked until the chat request completes.

**Acceptance Scenarios**:

1. **Given** the server is processing a `chat.send_message` call to Gemini, **When** a new HTTP request arrives at `/internal/get_command`, **Then** the server handles it immediately without waiting for Gemini.
2. **Given** Gemini requests a tool execution via the Bridge, **When** the command is queued, **Then** the next polling request from Blender successfully retrieves it.

## Requirements

### Functional Requirements

- **FR-001**: The `GeminiClient` MUST use `asyncio.to_thread` (or `run_in_executor`) to wrap all blocking network calls to the Google GenAI library (specifically `chat.send_message` and `models.generate_content`).
- **FR-002**: The `run_dynamic_conversation` method in `GeminiClient` MUST remain `async` but must yield control to the event loop during the API call.
- **FR-003**: The `simple_generate` method MUST also be non-blocking.

### Key Entities

- **GeminiClient**: The class wrapping the Google GenAI SDK.

## Success Criteria

### Measurable Outcomes

- **SC-001**: Elimination of "Command execution timed out" (504) errors caused by the server being unresponsive to polling during LLM generation.
- **SC-002**: Server logs show interleaving of `[LLM_CALL_START]` ... `Bridge: Sending command` ... `[LLM_CALL_END]`.