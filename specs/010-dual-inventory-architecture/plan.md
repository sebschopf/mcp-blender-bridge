# Implementation Plan: Dual Inventory Architecture

**Branch**: `010-dual-inventory-architecture` | **Date**: 2025-11-17 | **Spec**: [spec.md](./spec.md)
**Input**: Feature specification from `/specs/010-dual-inventory-architecture/spec.md`

**Note**: This template is filled in by the `/speckit.plan` command. See `.specify/templates/commands/plan.md` for the execution workflow.

## Summary

This plan outlines the technical steps to implement the Dual Inventory Architecture. The core of this effort is to refactor the current monolithic `capabilities.yaml` into a structured, hierarchical file system and to build a new "Knowledge Engine" that can load, index, and execute both granular tools and high-level recipes. This foundational work will enable future features like AI-driven recipe learning and a vast, scalable library of creative capabilities.

## Technical Context

**Language/Version**: Python 3.11+
**Primary Dependencies**: FastAPI, PyYAML, Pydantic
**Storage**: Filesystem (YAML files)
**Testing**: pytest
**Target Platform**: Controller (FastAPI Server)
**Project Type**: Single project (Controller)
**Performance Goals**: System startup time with 500 inventory files should not degrade by more than 50% compared to baseline.
**Constraints**: The new architecture must be backward-compatible in the sense that all existing tool functionalities must be preserved after refactoring.
**Scale/Scope**: This feature covers the architectural refactoring and the creation of the inventory loading/execution engine. It does not include the population of the inventories with a large number of tools or recipes.

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

-   ✅ **I. Strict MCP Architecture**: Compliant. The new architecture reinforces this principle by providing a structured, validated, and secure way to manage and expose capabilities.
-   ✅ **II. Conversational Interface**: Compliant. This architecture is a key enabler for more advanced and efficient conversational creation.
-   ✅ **III. Granular & Secure Tools**: Compliant. The `capabilities/` inventory maintains the principle of granularity, while the `knowledge_base/` provides a secure execution path for complex operations.
-   ✅ **IV. User-Centric Control**: Compliant. The system remains deterministic, and the learning mechanism (`save_recipe`) is initiated by the user.
-   ✅ **V. Blender-Native Integration**: Compliant. All executed commands will still resolve to the `bpy` API.
-   ✅ **VI. Continuous Validation Through Testing**: Compliant. The refactoring will require extensive testing to ensure no regressions are introduced.

## Project Structure

### Documentation (this feature)

```text
specs/010-dual-inventory-architecture/
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
│   ├── knowledge_engine.py  # NEW: Handles loading, indexing, and execution
│   └── ...
├── capabilities/            # NEW: Directory for granular tools
│   └── (subdirectories...)
├── knowledge_base/          # NEW: Directory for recipes
│   └── (subdirectories...)
├── resources/               # NEW: Directory for assets
│   └── (subdirectories...)
├── config/
│   └── capabilities.yaml    # DEPRECATED: To be removed after migration
└── tests/
    └── test_knowledge_engine.py # NEW: Unit tests for the new engine
```

**Structure Decision**: The implementation will introduce new directories (`capabilities`, `knowledge_base`, `resources`) and a new core module (`knowledge_engine.py`) to encapsulate the new logic. The existing `capabilities.yaml` will be phased out.