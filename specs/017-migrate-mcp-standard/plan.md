# Implementation Plan: Migrate to Official MCP Standard

**Branch**: `017-migrate-mcp-standard` | **Date**: 2025-11-23 | **Spec**: /specs/017-migrate-mcp-standard/spec.md
**Input**: Feature specification from `/specs/017-migrate-mcp-standard/spec.md`

**Note**: This template is filled in by the `/speckit.plan` command. See `.specify/templates/commands/plan.md` for the execution workflow.

## Summary

Migrate the existing custom FastAPI controller architecture to a fully compliant Model Context Protocol (MCP) Server using the official Python SDK. This will standardize how Blender capabilities are exposed to AI clients, replacing custom REST endpoints with the standardized JSON-RPC protocol defined by MCP, and implementing a synchronous bridge for command execution and state retrieval.

## Technical Context

**Language/Version**: Python 3.11+
**Primary Dependencies**: FastAPI, mcp SDK, uvicorn
**Storage**: N/A (in-memory queues/maps for bridge communication)
**Testing**: pytest
**Target Platform**: Linux/Windows server (running the controller) + Blender (running the addon)
**Project Type**: Single (Blender Addon + Python Controller application)
**Performance Goals**: Responsive command execution (< 500ms for simple operations)
**Constraints**: Must adhere to MCP standard; Blender Addon environment limitations.
**Scale/Scope**: Single user, single Blender instance.

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

- **I. Strict MCP Architecture**: Adheres. The Controller becomes an MCP Server, and the Addon remains a 'dumb' executor.
- **II. Conversational Interface**: Adheres. The MCP Host (Gemini Client) will handle this, the Controller's role is execution.
- **III. Granular & Secure Tools**: Adheres. The migration adopts MCP Tools, which are designed to be granular. Validation will be enforced by Pydantic models for MCP.
- **IV. User-Centric Control**: Adheres. The MCP Host will handle user confirmation.
- **V. Blender-Native Integration**: Adheres. The Peripheral (Addon) will continue to use `bpy` API.
- **VI. Continuous Validation Through Testing**: Adheres. New tests will be added for the MCP server and bridge.

## Project Structure

### Documentation (this feature)

```text
specs/017-migrate-mcp-standard/
├── plan.md              # This file (/speckit.plan command output)
├── research.md          # Phase 0 output (/speckit.plan command)
├── data-model.md        # Phase 1 output (/speckit.plan command)
├── quickstart.md        # Phase 1 output (/speckit.plan command)
├── contracts/           # Phase 1 output (/speckit.plan command)
└── tasks.md             # Phase 2 output (/speckit.tasks command - NOT created by /speckit.plan)
```

### Source Code (repository root)

```text
controller/
├── app/
│   ├── __init__.py
│   ├── bpy_utils.py
│   ├── gemini_client.py
│   ├── globals.py
│   ├── internal_tools.py
│   ├── knowledge_engine.py
│   ├── main.py
│   ├── models.py
│   ├── mcp_server.py      # New: MCP Server implementation
│   ├── bridge_api.py      # New: Internal API for Addon communication (long polling)
│   ├── plan_executor.py
│   └── services.py
├── capabilities/
├── config/
├── knowledge_base/
├── mcp_controller.egg-info/
├── resources/
└── tests/
    ├── __init__.py
    ├── test_config.py
    ├── test_knowledge_engine.py
    ├── test_main.py
    ├── test_models.py
    ├── test_new_tools.py
    └── test_mcp_server.py # New: Tests for MCP server and bridge

blender_addon/
├── __init__.py
├── command_executor.py
├── mcp_client.py        # Modified: To use long polling for commands
├── operators.py
├── preferences.py
├── server_manager.py
├── ui.py
└── tests/
    └── test_addon.py
```

**Structure Decision**: The existing project structure will largely be maintained, with new files added within `controller/app` for the MCP server and bridge logic, and modifications to `blender_addon` for the new communication pattern.

## Complexity Tracking

| Violation | Why Needed | Simpler Alternative Rejected Because |
|-----------|------------|-------------------------------------|
| N/A | N/A | N/A |
