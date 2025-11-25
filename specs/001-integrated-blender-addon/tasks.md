# Implementation Tasks: Integrated Blender Addon

**Feature Branch**: `001-integrated-blender-addon`
**Feature Spec**: `specs/001-integrated-blender-addon/spec.md`
**Implementation Plan**: `specs/001-integrated-blender-addon/plan.md`
**Created**: 2025-11-18

## Phase 1: Foundational - Code Refactoring and Configuration

**Goal**: Refactor the addon into a modular structure and implement the preferences panel for configuration.
**Independent Test**: The addon can be enabled, the preferences panel is accessible, and API key/path settings can be saved.

- [x] T001 [US1] Create the new directory structure with empty files: `blender_addon/operators.py`, `blender_addon/server_manager.py`, `blender_addon/preferences.py`.
- [x] T002 [US1] Move the existing UI panel code from `blender_addon/__init__.py` to `blender_addon/ui.py`.
- [x] T003 [US1] Create the addon preferences class in `blender_addon/preferences.py` with `api_key`, `controller_python_path`, and `port` (default: 8000) properties.
- [x] T004 [US1] In `blender_addon/__init__.py`, register the new modules (`ui`, `operators`, `preferences`) and the preferences class.
- [x] T005 [US1] In `blender_addon/ui.py`, add logic to display a message guiding the user to the preferences if the API key or Python path is not set.

## Phase 2: User Story 1 - Server Lifecycle Management

**Goal**: Implement the core logic to start, stop, and manage the FastAPI server subprocess from the addon.
**Independent Test**: The "Activate MCP" button starts the server process, and the "Deactivate MCP" button stops it. The server is also terminated when Blender closes.

- [x] T006 [US1] In `blender_addon/server_manager.py`, implement the `start_server()` function using `subprocess.Popen`, passing the configured port from preferences.
- [x] T007 [US1] In `blender_addon/server_manager.py`, implement the `stop_server()` function to terminate the stored subprocess handle.
- [x] T008 [US1] In `blender_addon/operators.py`, create a `MCP_OT_StartServer` operator that calls `start_server()`.
- [x] T009 [US1] In `blender_addon/operators.py`, create a `MCP_OT_StopServer` operator that calls `stop_server()`.
- [x] T010 [US1] In `blender_addon/ui.py`, add the "Activate MCP" and "Deactivate MCP" buttons to the panel and link them to the new operators.
- [x] T011 [US1] In `blender_addon/__init__.py`, use the `atexit` module to register a cleanup function that calls `stop_server()` on Blender exit.
- [x] T012 [US1] In `blender_addon/server_manager.py`, ensure the API key from preferences is passed as an environment variable to the subprocess.

## Phase 3: User Story 1 - UI and Chat Interaction

**Goal**: Build the chat interface and connect it to the MCP client.
**Independent Test**: A user can type a message, send it to the running MCP server, and see the response displayed in the chat history.

- [x] T013 [US1] In `blender_addon/ui.py`, create the UI layout for the chat history box and the text input field, visible only when the server is active.
- [x] T014 [US1] In `blender_addon/operators.py`, create an operator `MCP_OT_SendMessage` to handle sending the chat message.
- [x] T015 [US1] In `blender_addon/mcp_client.py`, refactor the client to be a class that can be instantiated and used by the operator.
- [x] T016 [US1] In the `MCP_OT_SendMessage` operator, use the `mcp_client` to send the user's message to the `127.0.0.1:{port}` endpoint (port from preferences).
- [x] T017 [US1] Implement a mechanism (e.g., a modal timer operator) in `blender_addon/ui.py` to periodically poll for new messages from the server and update the chat history.

## Phase 4: Testing

**Goal**: Create an automated test suite to validate the addon's core functionality.
**Independent Test**: The test suite can be run from the command line and successfully verifies that the server can be started and stopped by the addon.

- [x] T018 [US1] Create the `blender_addon/tests/` directory and an empty `blender_addon/tests/test_addon.py` file.
- [x] T019 [US1] In `blender_addon/tests/test_addon.py`, write a test function that enables the addon, sets preferences, and calls the `MCP_OT_StartServer` operator.
- [x] T020 [US1] In `blender_addon/tests/test_addon.py`, use the `psutil` library to verify that the server process was created successfully.
- [x] T021 [US1] In `blender_addon/tests/test_addon.py`, write a subsequent test to call the `MCP_OT_StopServer` operator and verify the process is terminated.
- [x] T022 [US1] Update the main `run_tests.bat` script to include a new step that runs the addon tests using `blender -b --python blender_addon/tests/test_addon.py`.

## Phase 5: Polish & Cross-Cutting Concerns

- [x] T023 Review all UI text for clarity and user-friendliness.
- [x] T024 Add error handling for common issues, such as the port being in use or an invalid Python path, and display clear error messages in the UI.
- [x] T025 Manually test the complete user flow as described in the `quickstart.md`.

## Dependencies

- **Phase 1** must be completed before all other phases.
- **Phase 2** must be completed before Phase 3 and 4.
- **Phase 3** and **Phase 4** can be worked on in parallel.
- **Phase 5** should be completed last.

## Implementation Strategy

1.  **MVP**: Complete Phases 1 and 2. This delivers the core, robust functionality of managing the server from within Blender.
2.  **Expansion**: Complete Phase 3 to build the user-facing chat interface.
3.  **Validation**: Complete Phase 4 to ensure the solution is stable and reliable.
4.  **Finalization**: Complete Phase 5 to ensure a polished user experience.
