# Implementation Plan: Extended Modeling Tools

**Branch**: `001-extended-modeling-tools` | **Date**: 2025-11-17 | **Spec**: [spec.md](./spec.md)
**Input**: Feature specification from `/specs/001-extended-modeling-tools/spec.md`

**Note**: This template is filled in by the `/speckit.plan` command. See `.specify/templates/commands/plan.md` for the execution workflow.

## Summary

This feature extends the MCP's modeling capabilities by adding five new granular tools: `object.rename`, `object.apply_bevel`, `object.apply_subsurf`, `object.select_multiple`, and `object.join`. These tools will allow the AI to perform more complex and realistic modeling tasks by manipulating object names, rounding edges, smoothing surfaces, and managing multiple objects as a single unit. The implementation will follow the existing architecture by adding new entries to `capabilities.yaml` and corresponding `bpy` script snippets to `bpy_utils.py`.

## Technical Context

**Language/Version**: Python 3.11+
**Primary Dependencies**: FastAPI
**Storage**: N/A
**Testing**: pytest
**Target Platform**: Blender Addon Environment
**Project Type**: Single project (Controller/Addon)
**Performance Goals**: N/A
**Constraints**: All operations must be executed via the `bpy` API.
**Scale/Scope**: This feature adds five distinct, granular tools.

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

-   ✅ **I. Strict MCP Architecture**: Compliant. The new tools are granular and encapsulate `bpy` logic within the Controller.
-   ✅ **II. Conversational Interface**: Compliant. These tools enrich the conversational capabilities of the AI.
-   ✅ **III. Granular & Secure Tools**: Compliant. Each new tool represents a single, well-defined, and secure action.
-   ✅ **IV. User-Centric Control**: Compliant. The new operations are deterministic and directly reflect user intent.
-   ✅ **V. Blender-Native Integration**: Compliant. All operations use the standard `bpy` API.

## Project Structure

### Documentation (this feature)

```text
specs/001-extended-modeling-tools/
├── plan.md              # This file (/speckit.plan command output)
├── research.md          # Phase 0 output (/speckit.plan command)
├── data-model.md        # Phase 1 output (/speckit.plan command)
├── quickstart.md        # Phase 1 output (/speckit.plan command)
├── contracts/           # Phase 1 output (/speckit.plan command)
└── tasks.md             # Phase 2 output (/speckit.tasks command - NOT created by /speckit.plan)
```

### Source Code (repository root)
```text
# Single project (DEFAULT)
controller/
├── app/
│   ├── bpy_utils.py   # Add new script snippets here
│   └── ...
├── config/
│   └── capabilities.yaml # Add new tool definitions here
└── tests/
    └── test_main.py     # Add new unit tests here
```

**Structure Decision**: The implementation will modify existing files within the established `controller` directory structure. No new files or directories are needed outside of the spec folder.
