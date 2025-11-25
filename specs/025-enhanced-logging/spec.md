# Feature Specification: Enhanced Debug Logging

**Feature Branch**: `025-enhanced-logging`  
**Created**: 2025-11-25  
**Status**: Draft  
**Input**: User description: "Implémenter un système de loggin détaillé et structuré côté serveur et cleitn pour tracer la perfomrance et le flux d'exécution. Chaque étape clé (réception requête, appel LLM, exécution outil, réponse) doit être loggé avec un timestramp précis. Il faut absolument qu'on puisse suivre tout ce qui se passe et voir où sont les goulots d'étranglement, les latence réseau, les boucles ou les fonctions qui foirent."

## User Scenarios & Testing

### User Story 1 - End-to-End Performance Tracing (Priority: P1)

Developers need to trace the entire lifecycle of a request from the Blender Addon to the Gemini API and back, with precise timestamps, to identify bottlenecks (e.g., slow LLM response vs slow tool execution vs network lag).

**Why this priority**: Critical for debugging timeouts and performance issues reported in production.

**Independent Test**:
- Send a request "Create a cube" from Blender.
- Open the `mcp_server_log.txt`.
- Verify entries exist for: `[REQ_START]`, `[ROUTER_START]`, `[ROUTER_END]`, `[LLM_CALL_START]`, `[LLM_CALL_END]`, `[TOOL_EXEC_START]`, `[TOOL_EXEC_END]`, `[REQ_END]`.
- Verify each entry has a timestamp and duration delta where applicable.

**Acceptance Scenarios**:

1. **Given** a user sends a chat message, **When** the server receives it, **Then** a log entry `[REQ_START] SessionID: ...` is written immediately.
2. **Given** the LLM decides to call a tool, **When** the tool execution begins and ends, **Then** log entries `[TOOL_EXEC_START]` and `[TOOL_EXEC_END]` are written with the tool name and execution time.
3. **Given** the request completes, **Then** a summary log `[REQ_END]` is written with total processing time.

### User Story 2 - Client-Side Timeout Configuration (Priority: P2)

Users need a way to configure the connection timeout in Blender preferences to accommodate slower models or complex tasks without hard crashes.

**Why this priority**: To mitigate `Request to chat timed out` errors immediately while performance tuning happens.

**Independent Test**:
- Go to Addon Preferences.
- Change "Timeout" from 30 to 60.
- Send a request.
- Verify that the client waits 60s before timing out.

**Acceptance Scenarios**:

1. **Given** the addon preferences, **When** the user looks for timeout settings, **Then** they find a "Request Timeout (s)" slider.
2. **Given** a long-running task, **When** it exceeds the configured timeout, **Then** the client logs a specific timeout warning but handles it gracefully (no crash).

## Requirements

### Functional Requirements

- **FR-001**: The Server MUST implement a structured logging format (e.g., `[TAG] Timestamp - Message - Duration`) for all key lifecycle events.
- **FR-002**: Key events to log: Request Received, Intent Classification (Start/End), Gemini API Call (Start/End), Tool Execution (Start/End), Response Sent.
- **FR-003**: The Blender Addon Preferences MUST include a `request_timeout` property (Int, default 30, min 5, max 300).
- **FR-004**: The `MCPClient` in the addon MUST use this preference value for all HTTP requests to the `/chat` endpoint.

### Key Entities

- **PerformanceLogger**: A utility class or wrapper in Python to handle timing and formatted log output easily.

## Success Criteria

### Measurable Outcomes

- **SC-001**: 100% of requests produce a log trace allowing calculation of time spent in LLM vs Tools vs System overhead.
- **SC-002**: Users can increase timeout to 60s+ to resolve timeout errors on their local machine.