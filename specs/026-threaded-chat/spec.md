# Feature Specification: Threaded Chat Execution

**Feature Branch**: `026-threaded-chat`  
**Created**: 2025-11-25  
**Status**: Draft  
**Input**: User description: "dans le MCP faire en sorte que l'appel au chat soit threadé afin d'éviter que le client attende une réponse du serveur qui ne viendra pas et que le serveur attende une réponse du client qui ne viendra pas."

## User Scenarios & Testing

### User Story 1 - Asynchronous Chat Processing (Priority: P1)

The Blender Addon must send chat requests to the MCP Controller without blocking Blender's Main Thread. This ensures that Blender remains responsive to execute intermediate commands (like `search_tools` or `execute_command`) sent by the Controller via the Bridge, preventing deadlock timeouts.

**Why this priority**: Critical fix. Currently, the synchronous chat request blocks Blender, preventing it from servicing the Controller's callbacks, causing the Controller to timeout and the entire operation to fail.

**Independent Test**:
- Initiate a chat request that requires the LLM to call a tool (e.g., "Create a cube").
- Monitor Blender's UI. It should NOT freeze completely.
- Verify in the logs that `execute_command` is processed *while* the chat request is still pending or just completing.
- Verify that the Controller does not timeout with a 504 error.

**Acceptance Scenarios**:

1. **Given** the user clicks "Send", **When** the request is sent, **Then** Blender's UI remains responsive (or at least processes internal timers).
2. **Given** the Controller sends a command via the Bridge while processing the chat, **When** the BridgeClient polls for it, **Then** Blender executes the command immediately and returns the result to the Controller.
3. **Given** the chat request completes, **When** the response arrives, **Then** the chat history is updated in the UI (safely from the main thread).

### Edge Cases

- **Multiple Requests**: If the user clicks Send multiple times rapidly, the system should either queue them or disable the button until the first request completes. (Decision: Disable button while processing).
- **Thread Safety**: Updating Blender UI/Data from a background thread crashes Blender. Updates must be scheduled back to the Main Thread using `bpy.app.timers`.

## Requirements

### Functional Requirements

- **FR-001**: The `WM_OT_MCP_Send_Chat` operator MUST NOT call `mcp_client.send_chat_message` synchronously on the main thread.
- **FR-002**: A new mechanism (e.g., `threading.Thread`) MUST be used to send the HTTP POST request.
- **FR-003**: The `MCPClient` MUST provide a callback mechanism or use a queue to handle the response when it arrives.
- **FR-004**: Updates to `bpy.context.scene` (like adding chat history) MUST happen on the main thread via `bpy.app.timers.register`.
- **FR-005**: The "Send" button MUST be disabled or show a "Sending..." state while a request is in progress to prevent double submission.

### Key Entities

- **AsyncChatWorker**: A thread or worker class responsible for the network IO.

## Success Criteria

### Measurable Outcomes

- **SC-001**: 0% of "Command execution timed out" (504) errors on the server when the LLM attempts to use a tool.
- **SC-002**: Blender UI refreshes (spinner or status text) while the AI is "thinking".