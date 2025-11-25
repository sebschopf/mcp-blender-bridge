# Research: Migrate to Official MCP Standard

## 1. Unknowns & Clarifications

### 1.1 MCP SDK & Server Implementation
- **Question**: How to implement the server to support both MCP standard and the existing Blender Addon connection?
- **Finding**: The `mcp` Python SDK provides `FastMCP` for quick setup, but for this use case, we need a hybrid approach. The server must expose:
    1.  **MCP Endpoints** (SSE or Stdio) for the AI Client.
    2.  **Bridge Endpoints** (HTTP) for the Blender Addon (to poll/receive commands).
- **Decision**: Use `FastAPI` as the base application. Mount the MCP Server logic (using `mcp.server.Server` or `mcp.server.fastmcp.FastMCP` if it allows mounting) alongside custom routes for the Addon.
- **Rationale**: The Blender Addon acts as a "dumb" executor that needs to pull commands. A standard MCP server doesn't have a "poll for commands" endpoint for peripherals. We must build this bridge.

### 1.2 Transport Protocol
- **Question**: SSE vs Stdio?
- **Decision**: **SSE (Server-Sent Events)**.
- **Rationale**:
    - Easier to debug (standard HTTP).
    - Allows the Controller to run as a distinct process that the Addon can easily find (localhost port).
    - Consistent with the existing HTTP-based architecture of the Addon.

### 1.3 State Management & Resource Exposure
- **Question**: How to implement `blender://scene/objects`?
- **Approach**:
    - The MCP Server maintains a cache of the scene state.
    - The Blender Addon periodically pushes state updates (or pushes them after every operation) to the Controller's `/internal/sync_state` endpoint.
    - When the MCP Client requests `resources/read`, the Server returns the cached state.
- **Alternative**: Real-time fetch. When `resources/read` is called, the Server halts, waits for the Addon to poll, asks for state, gets it, and returns.
    - *Decision*: **Real-time fetch (Synchronous Bridge)**.
    - *Mechanism*: `CommandQueue` will support "Get State" commands. The MCP Server request will `await` until the Addon picks up the command and returns the data.

## 2. Technology Choices

### 2.1 Server Framework
- **Choice**: `FastAPI` + `mcp` SDK.
- **Reason**: We already use FastAPI. It handles async well (essential for the wait-for-addon logic).

### 2.2 Communication Pattern (Controller <-> Addon)
- **Pattern**: **Long Polling** or **Fast Polling**.
- **Flow**:
    1.  Addon loops: `POST /internal/get_command`.
    2.  Controller holds request open until a command is available (or timeout).
    3.  Controller returns command.
    4.  Addon executes.
    5.  Addon `POST /internal/post_result`.
- **Reason**: Avoids complex socket programming in Blender's restricted Python environment.

## 3. Architecture

### 3.1 Components
1.  **MCP Host (Gemini/Claude)**: The generic AI client.
2.  **MCP Server (Controller)**: The Python process.
    - `MCP Router`: Handles `tools/call`, `resources/read`.
    - `Bridge Router`: Handles `/internal/*`.
    - `Session Manager`: Matches commands to the correct Addon instance (if we support multiple).
3.  **Peripheral (Blender Addon)**:
    - `Poller`: Loops and asks for work.
    - `Executor`: Runs `bpy` commands.

### 3.2 Security
- The `/internal` endpoints should be protected (e.g., local loopback only, simple shared token) to prevent rogue processes from driving Blender.

## 4. Migration Steps
1.  Create new `controller/app/mcp_server.py`.
2.  Implement the Bridge endpoints.
3.  Port `capabilities` to MCP Tools.
4.  Update Addon to use new polling loop instead of the "Chat" endpoint.
