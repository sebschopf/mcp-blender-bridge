# Implementation Plan - 026-threaded-chat

**Feature**: Threaded Chat Execution
**Status**: DRAFT

## Technical Context

### Architecture Overview

This feature addresses the critical deadlock issue where the Blender UI freezes while waiting for the LLM response, preventing the server from executing callbacks (tools) via the Bridge.
We will make the chat request asynchronous by offloading the blocking `requests.post` call to a background thread, freeing up the Main Thread to process `execute_command` requests from the server.

**Existing Components:**
- `blender_addon/operators.py`: `WM_OT_MCP_Send_Chat` calls `mcp_client.send_chat_message` synchronously.
- `blender_addon/mcp_client.py`: Contains the blocking `send_chat_message` method. Also contains `BridgeClient` which already demonstrates correct threading usage.

### Libraries & Dependencies

- **Python Standard Library**: `threading` (for the worker), `queue` (optional, but simple callback is enough).
- **Blender API**: `bpy.app.timers` to schedule UI updates back onto the Main Thread.

### Project Structure

```text
blender_addon/
  mcp_client.py        # Update: Add async_send_chat_message with threading logic
  operators.py         # Update: Update operator to use async method and handle callback
```

## Constitution Check

### Privacy & Security
- **Data Handling**: Same data, just async transport.
- **Safety**: Thread safety is paramount. NO `bpy.data` or `bpy.context` access is allowed in the background thread. All UI updates MUST be marshaled back to the main thread.

### Technical Constraints
- **SOLID Principle Exception**: The user explicitly requested keeping the addon logic somewhat consolidated (or at least not splitting into too many new files if unnecessary). We will implement the threading logic *inside* `MCPClient` as a new method, respecting the Single Responsibility of "managing network communication", but handling the thread orchestration there. The Operator will just provide the callback.

## Phase 0: Research & Decisions

### Design Decisions

1.  **Where to Thread?**: Inside `MCPClient`. This keeps `operators.py` cleaner and encapsulates the complexity of threading/callbacks within the network layer.
2.  **Callback Mechanism**: `MCPClient.async_send_chat_message(message, mode, on_complete)`
    - `on_complete` is a function `(response_data) -> None` that will be called on the **Main Thread**.
3.  **Thread Logic**:
    - Create `threading.Thread`.
    - In `run()`: Call `_send_request` (blocking).
    - When done: Use `bpy.app.timers.register(lambda: on_complete(response))` to schedule the callback.

## Phase 1: Design & Contracts

### API Changes

- `MCPClient` API: Add `async_send_chat_message(self, message, mode, on_complete_callback)`.

## Phase 2: Implementation

### Dependencies

- None.

### Strategy

1.  **Client**: Implement `async_send_chat_message` in `mcp_client.py`. It starts a thread.
2.  **Operator**: Modify `WM_OT_MCP_Send_Chat` in `operators.py`.
    - Set "Sending..." state (e.g., updating a property or log).
    - Define a `handle_response` local function.
    - Call `async_send_chat_message` with `handle_response`.
    - `handle_response` updates chat history and clears input.

## Phase 3: Polish

- Verify the UI doesn't freeze.
- Verify the "Sending" state is clear to the user (maybe via the connection status or a log message).