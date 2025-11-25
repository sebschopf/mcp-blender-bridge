# Implementation Plan: Dynamic Tool Retrieval (RAG)

**Branch**: `018-dynamic-tool-retrieval` | **Date**: 2025-11-23 | **Spec**: /specs/018-dynamic-tool-retrieval/spec.md
**Input**: Feature specification from `/specs/018-dynamic-tool-retrieval/spec.md`

**Note**: This template is filled in by the `/speckit.plan` command. See `.specify/templates/commands/plan.md` for the execution workflow.

## Summary

Implement a Retrieval-Augmented Generation (RAG) system for MCP Tools to scale to thousands of Blender operators without context overflow. This involves creating a searchable "Tool Index" in the KnowledgeEngine, implementing `search_tools` and `execute_command` meta-tools, and refactoring the MCP server to expose only these core tools initially.

## Technical Context

**Language/Version**: Python 3.11+
**Primary Dependencies**: FastAPI, mcp SDK, Pydantic (no new heavy ML deps)
**Storage**: In-memory Inverted Index
**Testing**: pytest
**Target Platform**: Linux/Windows server + Blender
**Project Type**: Single (Blender Addon + Python Controller)
**Performance Goals**: Search < 200ms, Context < 2000 tokens
**Constraints**: Must adhere to MCP standard; generic execution wrapper required.
**Scale/Scope**: Single user, support for 1000+ tools in library.

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

- **I. Strict MCP Architecture**: Adheres. The Controller still mediates. `execute_command` validates against the allowlist.
- **II. Conversational Interface**: Adheres. The AI discovers tools conversationally.
- **III. Granular & Secure Tools**: Adheres. Only allowlisted tools in `capabilities` can be executed.
- **IV. User-Centric Control**: Adheres.
- **V. Blender-Native Integration**: Adheres.
- **VI. Continuous Validation Through Testing**: Adheres. New tests for Indexer and Search.

## Project Structure

### Documentation (this feature)

```text
specs/018-dynamic-tool-retrieval/
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
│   ├── __init__.py
│   ├── mcp_server.py      # Modified: Expose only meta-tools
│   ├── knowledge_engine.py # Modified: Add Indexing & Search logic
│   ├── tool_index.py      # New: ToolIndex class implementation
│   └── models.py          # Modified: Add ToolMetadata models
└── tests/
    ├── test_tool_index.py # New: Tests for search logic
    └── test_mcp_server.py # Updated
```

**Structure Decision**: We will add a dedicated `tool_index.py` to keep the search logic separate from the main loading logic in `knowledge_engine.py`.

## Complexity Tracking

| Violation | Why Needed | Simpler Alternative Rejected Because |
|-----------|------------|-------------------------------------|
| Generic Executor | MCP clients can't dynamic-load tools mid-turn | Registering all 1000 tools blows up token limits |

