# Implementation Plan: SOLID & Responsibility Audit

**Branch**: `029-solid-responsibility-audit` | **Date**: 2025-11-25 | **Spec**: [spec.md](spec.md)
**Input**: Feature specification from `/specs/029-solid-responsibility-audit/spec.md`

**Note**: This template is filled in by the `/speckit.plan` command. See `.specify/templates/commands/plan.md` for the execution workflow.

## Summary

The goal is to audit the `controller/` codebase to ensure strict adherence to SOLID principles and a layered architecture (Service vs. Model vs. Router), preventing regression and tight coupling. The `blender_addon/` is exempted from strict pure-Python standards due to `bpy` dependencies but must still maintain internal consistency and not leak `bpy` into the controller.

## Technical Context

**Language/Version**: Python 3.11+ (as seen in `controller/pyproject.toml`)
**Primary Dependencies**: FastAPI, Pydantic, `google-genai`, `mcp` SDK (Controller); `bpy` (Addon).
**Storage**: N/A (In-memory state or YAML configs for capabilities).
**Testing**: `pytest` (Controller), `unittest` style inside Blender environment (Addon).
**Target Platform**: Cross-platform (Windows/macOS/Linux) where Blender runs.
**Project Type**: Client-Server (Blender Addon as Client, FastAPI as Controller).
**Performance Goals**: N/A (Code quality audit).
**Constraints**:
- `controller/` must NEVER import `bpy`.
- `blender_addon/` must manage UI/Operators separately.
**Scale/Scope**: Current codebase size (~4000 LOC).

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

### I. Strict MCP Architecture
- **Compliance**: The audit reinforces this by strictly separating Controller (FastAPI) from Peripheral (Blender Addon).
- **Status**: PASS

### II. Conversational Interface
- **Compliance**: N/A (Internal code structure).
- **Status**: PASS

### III. Granular & Secure Tools
- **Compliance**: N/A (Audit focus).
- **Status**: PASS

### IV. User-Centric Control
- **Compliance**: N/A.
- **Status**: PASS

### V. Blender-Native Integration
- **Compliance**: The exemption for `blender_addon/` respects this principle.
- **Status**: PASS

### VI. Continuous Validation Through Testing
- **Compliance**: The plan includes verifying code structure via tests/scripts.
- **Status**: PASS

## Project Structure

### Documentation (this feature)

```text
specs/029-solid-responsibility-audit/
├── plan.md              # This file
├── research.md          # Phase 0 output
├── data-model.md        # Phase 1 output (N/A for audit, but will verify models.py)
├── quickstart.md        # Phase 1 output
├── contracts/           # Phase 1 output (N/A)
└── tasks.md             # Phase 2 output
```

### Source Code (repository root)

```text
controller/
├── app/
│   ├── models.py        # Data Models (Pydantic)
│   ├── services.py      # Business Logic
│   ├── main.py          # API Router/Entrypoint
│   ├── mcp_server.py    # MCP Protocol logic
│   ├── bridge_api.py    # Internal Bridge logic
│   └── gemini_client.py # Infrastructure (External API)
└── tests/

blender_addon/
├── __init__.py
├── operators.py         # Blender Operators
├── ui.py                # UI Panels
├── mcp_client.py        # Client logic
└── introspection.py     # Blender Internal Logic
```

**Structure Decision**: The current structure already closely matches the desired layered architecture. The audit will verify that logical boundaries are respected (e.g., no business logic in `main.py`, no routing in `services.py`).

## Complexity Tracking

> **Fill ONLY if Constitution Check has violations that must be justified**

| Violation | Why Needed | Simpler Alternative Rejected Because |
|-----------|------------|-------------------------------------|
| N/A       |            |                                     |