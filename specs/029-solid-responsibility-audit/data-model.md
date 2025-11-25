# Data Model: SOLID & Responsibility Audit

> **Note**: This feature focuses on *auditing* existing models, not creating new ones. This file documents the *expected* structure of key entities to be verified.

## Controller Entities

### `CommandRequest` (in `models.py`)
- **Responsibility**: API Data Transfer Object (DTO).
- **Layer**: Model.
- **Constraints**: Must NOT contain business logic methods (e.g., `execute()`).

### `CommandResponse` (in `models.py`)
- **Responsibility**: API DTO.
- **Layer**: Model.

### `GeminiClient` (in `gemini_client.py`)
- **Responsibility**: Infrastructure Wrapper.
- **Layer**: Infrastructure.
- **Constraint**: Must handle API keys and raw HTTP/GRPC calls. Must NOT handle business rules (e.g., "if intent is X, do Y").

### `ChatService` (in `services.py`)
- **Responsibility**: Business Logic Orchestrator.
- **Layer**: Service.
- **Constraint**:
    - Orchestrates `GeminiClient` and `KnowledgeEngine`.
    - Does NOT define API routes (`@app.post`).
    - Does NOT directly dependency on `bpy`.

## Blender Addon Entities

### `MCPClient` (in `mcp_client.py`)
- **Responsibility**: HTTP Client & State Management.
- **Layer**: Infrastructure (Client-side).

### `MCP_OT_*` (in `operators.py`)
- **Responsibility**: Blender Operator execution.
- **Layer**: Application (Client-side).
- **Constraint**: Should delegate complex logic to `mcp_client` or helper functions, not implement heavy networking logic inside `execute()`.
