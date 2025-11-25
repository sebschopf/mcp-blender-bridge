# Tasks: Migrate to Official MCP Standard

**Phase**: Implementation | **Feature**: 017-migrate-mcp-standard

## Phase 1: Setup & Dependencies
*Setup environment and project structure.*

- [x] T001 Install `mcp` SDK and update `controller/requirements.txt`
- [x] T002 Create `controller/app/mcp_server.py` skeleton
- [x] T003 Create `controller/app/bridge_api.py` skeleton
- [x] T004 Create `controller/app/bridge_models.py` for BridgeCommand/Result schemas

## Phase 2: Foundational - Bridge Protocol
*Establish the synchronous communication bridge between Controller and Addon.*

- [x] T005 Define `BridgeCommand` and `BridgeResult` Pydantic models in `controller/app/bridge_models.py`
- [x] T006 [P] Implement `BridgeManager` class in `controller/app/bridge_api.py` with in-memory `PendingCommandQueue` and `PendingResultMap`
- [x] T007 Implement `POST /internal/get_command` endpoint in `controller/app/bridge_api.py` (Long Polling)
- [x] T008 Implement `POST /internal/post_result` endpoint in `controller/app/bridge_api.py`
- [x] T009 [P] Update `blender_addon/mcp_client.py` to implement the polling loop (fetching commands)
- [x] T010 Update `blender_addon/mcp_client.py` to execute received scripts and POST results back
- [x] T011 Verify Bridge: Create a test script to push a command to `BridgeManager` and verify Addon executes it

## Phase 3: User Story 1 - Expose Blender Tools via MCP
*Implement the MCP Server and map Blender capabilities.*

- [x] T012 [US1] Initialize `FastMCP` server instance in `controller/app/mcp_server.py`
- [x] T013 [US1] Create a utility in `controller/app/mcp_server.py` to dynamically register MCP tools from existing `capabilities`
- [x] T014 [US1] Implement the generic tool execution handler in `mcp_server.py` that pushes to `BridgeManager` and awaits result
- [x] T015 [US1] Implement `blender://scene/objects` resource in `mcp_server.py` (triggers "get_state" command to Bridge)
- [x] T016 [US1] Configure SSE transport for MCP Server and mount/integrate with main FastAPI app in `controller/app/main.py`
- [x] T017 [US1] Test MCP: Use an MCP Inspector (or script) to list tools and call a simple tool (e.g., create_cube)

## Phase 4: User Story 2 - Cleanup & Standardization
*Remove legacy logic and update the Gemini Client.*

- [x] T018 [P] [US2] Update `controller/app/gemini_client.py` to act as an MCP Host (or use MCP tools definitions for prompt)
- [x] T019 [US2] Update `controller/app/gemini_client.py` to execute function calls via the MCP Server/Bridge
- [x] T020 [US2] Remove legacy `controller/app/plan_executor.py`
- [x] T021 [US2] Remove legacy `controller/app/internal_tools.py` (if fully superseded)
- [x] T022 [US2] Remove legacy `/api/chat` and `/api/discover_capabilities` endpoints from `controller/app/main.py`
- [x] T023 [US2] Remove legacy `blender_addon/server_manager.py` logic related to old chat endpoints (if any)

## Phase 5: Polish
*Documentation and final checks.*

- [x] T024 Update project README.md with MCP connection details
- [x] T025 Run final full-system test (Gemini -> MCP -> Blender)

## Dependencies

- Phase 2 (Bridge) MUST complete before Phase 3 (MCP Server).
- Phase 3 (MCP Server) MUST complete before Phase 4 (Cleanup).

## Implementation Strategy

1.  **MVP**: Complete Phase 1 & 2. Verify we can "drive" Blender from a simple Python script calling the Bridge API.
2.  **MCP Beta**: Complete Phase 3. Verify we can "drive" Blender from Claude Desktop or a generic MCP client.
3.  **Migration**: Complete Phase 4. Switch the internal Gemini Client to use the new pipes and delete old code.
