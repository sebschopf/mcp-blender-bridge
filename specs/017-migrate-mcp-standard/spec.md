# Specification: Migrate to Official MCP Standard

## 1. Overview

### 1.1 Goal
Migrate the existing custom FastAPI controller architecture to a fully compliant **Model Context Protocol (MCP)** Server using the official Python SDK. This transformation will standardize how Blender capabilities are exposed to AI clients (like Gemini or Claude Desktop), replacing custom REST endpoints with the standardized JSON-RPC protocol defined by MCP.

### 1.2 Core Value
- **Interoperability**: By adopting the standard, the Blender controller becomes a generic MCP server. Any MCP-compliant client (Claude Desktop, Cursor, etc.) can instantly control Blender without custom integration code.
- **Standardization**: Replaces custom "discovery" and "execution" logic with well-defined `tools/list`, `tools/call`, and `resources/list` capabilities.
- **Future-Proofing**: Aligns the project with the broader AI ecosystem standards.

### 1.3 Success Criteria
- [ ] The Controller application is replaced or heavily refactored to use the official `mcp` Python SDK.
- [ ] Blender capabilities (e.g., `create_cube`) are exposed as **MCP Tools**.
- [ ] Blender scene state (e.g., list of objects) is exposed as **MCP Resources**.
- [ ] Custom REST endpoints (`/api/discover_capabilities`, `/api/chat`, `/api/event`) are removed or replaced by the MCP transport (Stdio or SSE).
- [ ] The Gemini Client is updated to communicate via the MCP protocol (or via a bridge if Gemini doesn't support MCP natively yet - *Note: Gemini supports function calling, so we act as an MCP Client to the MCP Server*).
- [ ] Legacy code (old `internal_tools.py`, `plan_executor.py`) is identified and slated for removal.
- [ ] The system passes the "Constitution Check" for security and architecture.

## 2. User Stories

### 2.1 As a Platform Developer
I want to expose Blender tools via the standard MCP protocol
So that any MCP-compliant AI assistant can control Blender without specific plugins.

**Acceptance Criteria:**
- An MCP Server is running and serving Blender tools.
- `tools/list` returns the available Blender operators.
- `tools/call` successfully triggers the operator in Blender (via the existing Addon bridge).

### 2.2 As a Maintainer
I want to remove custom, non-standard communication logic
So that the codebase is cleaner, adheres to SOLID principles, and relies on maintained standards.

**Acceptance Criteria:**
- Custom Pydantic models for "Action Plans" are replaced or adapted to MCP Tool Calls.
- The custom `KnowledgeEngine` is adapted to provide data to the MCP Server.
- A cleanup list of obsolete files is generated and executed.

## 3. Functional Requirements

### 3.1 MCP Server Implementation
- **FR 3.1.1**: Implement an MCP Server using `mcp.server.FastMCP` (or low-level server).
- **FR 3.1.2**: Configure the server to communicate via **SSE (Server-Sent Events)** for web compatibility or **Stdio** for local desktop integration. *Decision: SSE is likely better for the existing architecture where Controller and Addon communicate over HTTP/WebSocket.*

### 3.2 Tool Exposure
- **FR 3.2.1**: Map existing `capabilities` (from YAML/KnowledgeEngine) to MCP Tool definitions.
- **FR 3.2.2**: Implement the execution handler for these tools to forward commands to the Blender Addon (keeping the Peripheral/Addon relatively unchanged or adapting its listener).

### 3.3 Resource Exposure
- **FR 3.3.1**: Implement an MCP Resource `blender://scene/objects` that returns the current list of objects in the Blender scene (fetched from the Addon).

### 3.4 Cleanup
- **FR 3.4.1**: Identify obsolete files (`internal_tools.py`, old REST routes).
- **FR 3.4.2**: Remove them after verification.

## 4. Technical Considerations

### 4.1 Architecture Shift
- **Current**: Client -> REST API -> Controller -> Action Plan -> Addon.
- **New**: Client (MCP Host) -> MCP Protocol -> MCP Server (Controller) -> Addon.
- **Challenge**: The "Client" here is Gemini. Does Gemini speak MCP natively? No.
    - **Solution**: The "Gemini Client" in our app becomes an **MCP Host**. It instantiates the MCP Client to talk to our MCP Server (Controller), discovers tools, and passes them to Gemini's Function Calling API. This aligns perfectly with the "Client" role in MCP architecture.

### 4.2 Transport
- **SSE**: Preferred for HTTP-based communication between distinct processes (Controller <-> Addon might stay HTTP, Controller <-> Gemini Client via in-memory or loopback).

## 5. Assumptions
- The official `mcp` python SDK is installed and available.
- The Blender Addon's core execution logic (`bpy` execution) remains valid, but its communication method might need adjustment if the Controller no longer exposes the exact same REST endpoints (e.g., `/api/chat` might disappear if the Chat UI moves to an MCP Host app, OR our Controller maintains a "Chat Endpoint" that internally acts as an MCP Host).

## 6. Out of Scope
- Rewriting the Blender Addon entirely (we strictly want to standardize the *Controller* layer).
- Adding new Blender features during migration.