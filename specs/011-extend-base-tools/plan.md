# Implementation Plan: Extend Base Modeling Tools (with Token Optimization)

**Branch**: `011-extend-base-tools` | **Date**: 2025-11-17 | **Spec**: [spec.md](./spec.md)
**Input**: Feature specification from `/specs/011-extend-base-tools/spec.md`

## Summary

This plan outlines the technical steps to significantly expand the range of modeling tools available to the AI, while simultaneously implementing a token optimization strategy to reduce costs and improve performance. The core of this strategy is a two-step tool discovery process: the AI will first request a list of tool categories, and then request the specific tools for the relevant categories.

## Technical Context

**Language/Version**: Python 3.11+
**Primary Dependencies**: FastAPI, PyYAML, Pydantic
**Storage**: Filesystem (YAML files)
**Testing**: pytest
**Target Platform**: Controller (FastAPI Server)
**Performance Goals**: Startup time must not increase by more than 20%. Token usage for tool discovery must be reduced by at least 50%.
**Constraints**: All new tools must conform to the existing `Tool` Pydantic model.
**Unknowns**: All previous unknowns have been resolved in the `research.md` file. No new unknowns are identified.

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

-   ✅ **I. Strict MCP Architecture**: Compliant. The new endpoints and logic will be added to the Controller, respecting the MCP separation.
-   ✅ **II. Conversational Interface**: Compliant. This change enhances the machine-to-machine conversation, making it more efficient.
-   ✅ **III. Granular & Secure Tools**: Compliant. The new endpoints are for discovery and do not execute any code in Blender.
-   ✅ **IV. User-Centric Control**: Compliant. No changes to the user-facing workflow.
-   ✅ **V. Blender-Native Integration**: Compliant. All modeling tools will still map to `bpy` API calls.
-   ✅ **VI. Continuous Validation Through Testing**: Compliant. New tests will be required for the new endpoint and the modified endpoint logic.

## Project Structure

### Documentation (this feature)

```text
specs/011-extend-base-tools/
├── plan.md              # This file
├── research.md          # (Existing)
├── data-model.md        # (Existing)
├── contracts/
│   └── openapi.yaml       # NEW
├── quickstart.md        # To be updated
└── tasks.md             # To be updated
```

### Source Code (repository root)
```text
controller/
├── app/
│   ├── main.py              # MODIFIED: Add /discover_categories, modify /discover_capabilities
│   └── knowledge_engine.py  # MODIFIED: Add method to get categories
├── capabilities/
│   ├── mesh/
│   │   └── editing.yaml       # NEW
│   ├── sculpt/              # NEW
│   │   └── brushes.yaml       # NEW
│   └── modifiers/           # NEW
│       ├── generate.yaml      # NEW
│       └── deform.yaml        # NEW
└── tests/
    ├── test_main.py         # MODIFIED: Add tests for new/modified endpoints
    └── test_new_tools.py    # NEW: Tests for the expanded toolset
```

**Structure Decision**: The implementation will now involve modifications to core application files (`main.py`, `knowledge_engine.py`) to support the new discovery mechanism, in addition to adding the new tool files in `capabilities/`. A new API contract will be generated, and the quickstart guide will be updated.