# Tasks: Dynamic Tool Retrieval (RAG)

**Phase**: Implementation | **Feature**: 018-dynamic-tool-retrieval

## Phase 1: Setup & Dependencies
*Setup environment and project structure.*

- [x] T001 Create `controller/app/tool_index.py` skeleton
- [x] T002 [P] Define `ToolMetadata` and `ToolSearchResult` models in `controller/app/models.py`
- [x] T003 [P] Define `ExecuteCommandRequest` model in `controller/app/models.py`

## Phase 2: Foundational - Tool Indexing
*Implement the in-memory search engine.*

- [x] T004 Implement `ToolIndex` class in `controller/app/tool_index.py` with `build_index` and `search` methods
- [x] T005 Implement simple keyword-based scoring (name > tags > description) in `ToolIndex`
- [x] T006 Create unit tests for `ToolIndex` in `controller/tests/test_tool_index.py` covering search relevance
- [x] T007 [P] Update `controller/app/knowledge_engine.py` to initialize `ToolIndex` and populate it from loaded capabilities
- [x] T008 Update `controller/app/knowledge_engine.py` to support generating usage signatures for `ToolMetadata`

## Phase 3: User Story 1 - AI-Driven Tool Discovery
*Expose search and generic execution to the AI.*

- [x] T009 [US1] Implement `search_tools` MCP tool in `controller/app/mcp_server.py` that calls `KnowledgeEngine.search_tools`
- [x] T010 [US1] Implement `execute_command` MCP tool in `controller/app/mcp_server.py` that acts as a safe wrapper for internal tools
- [x] T011 [US1] Refactor `register_tools` in `controller/app/mcp_server.py` to ONLY register meta-tools (`search_tools`, `execute_command`, `get_scene_state`) by default
- [x] T012 [US1] Update `controller/app/gemini_client.py` system prompt to explain the "Search -> Execute" workflow
- [x] T013 [US1] Test the full flow: Mock an AI request for "chair", verify search call, result, and subsequent execution call

## Phase 4: User Story 2 - Massive Tool Indexing
*Ensure scalability and performance.*

- [x] T014 [US2] Verify `ToolIndex` performance with 1000+ dummy tools (create a benchmark test in `tests/test_tool_index.py`)
- [x] T015 [US2] Optimize `search_tools` output format to ensure it stays compact (e.g., concise usage strings)

## Phase 5: Polish
*Documentation and final checks.*

- [x] T016 Update `README.md` with the new RAG architecture explanation
- [x] T017 Run full suite of tests including `test_tool_index.py` and `test_mcp_server.py`

## Dependencies

- Phase 2 (Indexing) MUST complete before Phase 3 (MCP Exposure).
- `KnowledgeEngine` updates (T007) depend on `ToolIndex` implementation (T004).

## Implementation Strategy

1.  **MVP**: Implement `ToolIndex` and `search_tools`. Verify search relevance manually.
2.  **Integration**: Switch `mcp_server.py` to expose only meta-tools.
3.  **Verification**: Use the Gemini Client to drive the system via the new workflow.
