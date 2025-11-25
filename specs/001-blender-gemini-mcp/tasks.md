# Implementation Tasks: Blender-Gemini MCP Integration

**Feature Branch**: `001-blender-gemini-mcp`  
**Feature Spec**: `specs/001-blender-gemini-mcp/spec.md`  
**Implementation Plan**: `specs/001-blender-gemini-mcp/plan.md`  
**Created**: 2025-11-16

## Phase 1: Setup & Project Initialization

- [X] T001 Create root project directories: `controller/` and `blender_addon/`
- [X] T002 Initialize Python virtual environment for Controller: `controller/.venv`
- [X] T003 Create `controller/requirements.txt` with `fastapi`, `uvicorn`, `python-dotenv`, `google-generativeai`
- [X] T004 Create `controller/.env` for `GEMINI_API_KEY`
- [X] T005 Create `blender_addon/__init__.py` with basic Blender addon registration info

## Phase 2: Foundational Components (Blocking Prerequisites)

- [X] T006 [P] Implement Pydantic models for `ChatMessage`, `ToolCall`, `BpyCommand`, `CommandRequest`, `CommandResponse` in `controller/app/models.py`
- [X] T007 [P] Create FastAPI application instance in `controller/app/main.py`
- [X] T008 [P] Implement `/api/chat` endpoint in `controller/app/main.py` to receive `CommandRequest` and return `CommandResponse` (stubbed AI interaction)
- [X] T009 [P] Implement `/api/event/{event_type}` endpoint in `controller/app/main.py` to handle `undo`, `connect`, `disconnect` events
- [X] T010 [P] Implement basic HTTP client in `blender_addon/mcp_client.py` to send requests to Controller
- [X] T011 [P] Create Blender UI panel in `blender_addon/ui.py` with a "Connect" button and a placeholder chat area
- [X] T012 [P] Integrate `mcp_client.py` and `ui.py` into `blender_addon/__init__.py`

## Phase 3: User Story 1 - Connect Blender to the MCP (P1)

**Goal**: A Blender artist can connect their Blender instance to the Gemini-powered MCP.
**Independent Test**: The Blender Addon successfully registers and shows a "Connected" status to the MCP Controller. The Controller logs the connection from the Blender Peripheral.

- [X] T013 [US1] Implement "Connect" button logic in `blender_addon/ui.py` to send `connect` event to Controller
- [X] T014 [US1] Implement "Disconnect" button logic in `blender_addon/ui.py` to send `disconnect` event to Controller
- [X] T015 [US1] Implement connection status display in `blender_addon/ui.py`
- [X] T016 [US1] Implement Controller-side logic for `connect` event to register session in `controller/app/main.py`
- [X] T017 [US1] Implement Controller-side logic for `disconnect` event to unregister session in `controller/app/main.py`
- [X] T018 [US1] Implement periodic polling from Blender Addon to Controller to check for commands/status updates in `blender_addon/mcp_client.py`
- [X] T019 [US1] Implement error handling and retry logic for connection loss in `blender_addon/mcp_client.py`

## Phase 4: User Story 2 - Generate a Simple Object via Conversation (P2)

**Goal**: A user can create a simple 3D object by conversing with Gemini.
**Independent Test**: A user can type a simple command, answer clarifying questions, and see the corresponding object appear in their Blender scene.

- [X] T020 [P] [US2] Implement chat input field and display area in `blender_addon/ui.py`
- [X] T021 [P] [US2] Implement sending user prompts from Blender Addon to `/api/chat` in `blender_addon/mcp_client.py`
- [X] T022 [P] Integrate Gemini API client in `controller/app/gemini_client.py`
- [X] T023 [P] [US2] Implement initial AI conversation flow in `controller/app/main.py` (receive prompt, send to Gemini, get response)
- [X] T024 [P] [US2] Implement tool definition for `create_cube` in `controller/app/tools.py` (e.g., `create_cube(size: float, material: str) -> BpyCommand`)
- [X] T025 [P] [US2] Implement tool calling logic in `controller/app/main.py` to parse Gemini's tool calls and generate `BpyCommand`
- [X] T026 [P] [US2] Implement `BpyCommand` execution in Blender Addon in `blender_addon/command_executor.py`
- [X] T027 [P] [US2] Implement displaying AI responses and chat history in `blender_addon/ui.py`
- [X] T028 [P] [US2] Implement validation of incoming `ToolCall` parameters in `controller/app/main.py`

## Phase 5: User Story 3 - Execute a Multi-Step Creation (P3)

**Goal**: A designer can create a more complex scene with multiple, sequential operations.
**Independent Test**: The user can issue a multi-part request, and the system correctly sequences the operations to produce the final desired scene in Blender.

- [X] T029 [P] [US3] Implement tool definition for `create_sphere`, `create_cone`, `move_object`, `set_material` in `controller/app/tools.py`
- [X] T030 [P] [US3] Enhance AI conversation flow in `controller/app/main.py` to handle multi-turn clarifications and sequential tool calls
- [X] T031 [P] [US3] Implement object identification and modification logic in `controller/app/main.py` for `move_object`, `set_material`
- [X] T032 [P] [US3] Implement `bpy` commands for `create_sphere`, `create_cone`, `move_object`, `set_material` in `blender_addon/command_executor.py`
- [X] T033 [P] [US3] Implement undo event detection in `blender_addon/__init__.py` using `bpy.app.handlers.undo_post`
- [X] T034 [P] [US3] Send undo event to Controller via `/api/event/undo` in `blender_addon/mcp_client.py`
- [X] T035 [P] [US3] Implement Controller-side logic to synchronize state on `undo` event in `controller/app/main.py`

## Phase 6: Polish & Cross-Cutting Concerns

- [X] T036 Implement comprehensive logging for Controller and Blender Addon
- [X] T037 Implement robust error handling and user feedback for all components
- [X] T038 Add unit tests for Controller's Pydantic models and tool validation logic
- [X] T039 Add unit tests for Blender Addon's client communication and command execution
- [X] T040 Update `quickstart.md` with detailed setup and usage instructions
- [X] T041 Review and refine security measures (input validation, API key handling)
- [X] T042 Create `README.md` for the project with overview, setup, and usage.

## Dependencies

- Phase 1 must be completed before Phase 2.
- Phase 2 must be completed before Phase 3, Phase 4, and Phase 5.
- User Story 1 (Phase 3) is foundational for all other user stories.
- User Story 2 (Phase 4) can be developed in parallel with User Story 3 (Phase 5) after Phase 2 is complete, but User Story 2 is a prerequisite for a fully functional conversational flow.
- Phase 6 can begin once core functionality from Phases 3, 4, and 5 is stable.

## Parallel Execution Examples

- **After Phase 2**: 
    - T013, T014, T015 (US1 UI) can be done in parallel with T016, T017 (US1 Controller logic).
    - T020, T021 (US2 UI) can be done in parallel with T022, T023 (US2 Controller/Gemini integration).
    - T029, T030, T031 (US3 Controller logic) can be done in parallel with T032 (US3 Blender commands).

## Implementation Strategy

This project will follow an incremental delivery approach, prioritizing core functionality first:

1.  **Minimum Viable Product (MVP)**: Focus on completing Phase 1, Phase 2, and User Story 1 (Phase 3). This will establish the basic connection between Blender and the MCP Controller.
2.  **Core Conversational Flow**: Implement User Story 2 (Phase 4) to enable simple object creation via natural language.
3.  **Advanced Interactions**: Implement User Story 3 (Phase 5) for multi-step creations and undo synchronization.
4.  **Refinement**: Address Phase 6 tasks for polish, robustness, and comprehensive documentation.
