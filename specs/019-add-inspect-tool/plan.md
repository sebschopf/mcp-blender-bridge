# Implementation Plan: Add Inspect Tool & Save Recipe

**Branch**: `019-add-inspect-tool` | **Date**: 2025-11-23 | **Spec**: /specs/019-add-inspect-tool/spec.md
**Input**: Feature specification from `/specs/019-add-inspect-tool/spec.md`

**Note**: This template is filled in by the `/speckit.plan` command. See `.specify/templates/commands/plan.md` for the execution workflow.

## Summary

Implement `inspect_tool` to allow the AI to query Blender for tool parameters at runtime, and `save_recipe` to allow the AI to persist successful action sequences. This closes the "Search -> Inspect -> Execute" loop.

## Technical Context

**Language/Version**: Python 3.11+
**Primary Dependencies**: FastAPI, mcp SDK, Pydantic
**Storage**: YAML files for recipes
**Testing**: pytest, blender integration tests
**Target Platform**: Linux/Windows server + Blender
**Project Type**: Single (Blender Addon + Python Controller)
**Performance Goals**: Introspection < 200ms
**Constraints**: Must handle Blender operator name mapping safely.
**Scale/Scope**: Single user.

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

- **I. Strict MCP Architecture**: Adheres.
- **II. Conversational Interface**: Adheres.
- **III. Granular & Secure Tools**: Adheres. `save_recipe` is restricted to internal knowledge base.
- **IV. User-Centric Control**: Adheres.
- **V. Blender-Native Integration**: Adheres. Uses `bl_rna`.
- **VI. Continuous Validation Through Testing**: Adheres.

## Project Structure

### Documentation (this feature)

```text
specs/019-add-inspect-tool/
├── plan.md              # This file
├── research.md          # Phase 0 output
├── data-model.md        # Phase 1 output
├── quickstart.md        # Phase 1 output
├── contracts/           # Phase 1 output
└── tasks.md             # Phase 2 output
```

### Source Code (repository root)

```text
controller/
├── app/
│   ├── mcp_server.py      # Modified: Add inspect_tool, save_recipe
│   ├── bridge_models.py   # Modified: Update BridgeCommand type
│   ├── knowledge_engine.py # Modified: Add recipe registration method
│   └── utils.py           # New: Maybe move sanitization here?
blender_addon/
├── mcp_client.py          # Modified: Handle get_rna_info command
└── introspection.py       # New: Logic for extracting RNA info
```

**Structure Decision**: Add `blender_addon/introspection.py` to keep the introspection logic clean and separate from the main client loop.

## Complexity Tracking

| Violation | Why Needed | Simpler Alternative Rejected Because |
|-----------|------------|-------------------------------------|
| N/A | N/A | N/A |

