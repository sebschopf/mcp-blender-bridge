# Implementation Plan: Integrated Blender Addon

**Branch**: `001-integrated-blender-addon` | **Date**: 2025-11-18 | **Spec**: [spec.md](./spec.md)
**Input**: Feature specification from `/specs/001-integrated-blender-addon/spec.md`

## Summary

This plan outlines the technical steps to refactor the existing Blender addon into a fully integrated, user-friendly tool. The addon will manage the lifecycle of the MCP FastAPI server from within Blender, handle API key configuration through Blender's preferences, and provide a seamless chat interface for the user.

## Technical Context

**Language/Version**: Python 3.11+
**Primary Dependencies**: Standard `subprocess` module for server management; `psutil` for process verification.
**Storage**: Blender Preferences (`bpy.types.AddonPreferences`) for API Key storage.
**Testing**: `unittest` suite run via `blender -b ... --python ...`; `psutil` for validating server process lifecycle.
**Target Platform**: Blender 3.0+
**Project Type**: Blender Addon
**Performance Goals**: Server startup in < 10 seconds; server shutdown in < 3 seconds.
**Constraints**: The addon MUST NOT block the Blender UI thread. All server management and communication must be asynchronous or run in separate threads.
**Scale/Scope**: Single-user, local server process.

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

-   ✅ **I. Strict MCP Architecture**: Compliant. The addon acts as the Peripheral, initiating and communicating with the Controller (FastAPI server), but not containing core logic.
-   ✅ **II. Conversational Interface**: Compliant. The addon will provide the primary chat UI for the user to interact with the AI.
-   ✅ **III. Granular & Secure Tools**: Compliant. The addon's role is to execute commands, not define them. It will securely handle the API key.
-   ✅ **IV. User-Centric Control**: Compliant. The user has explicit control over starting and stopping the server process via UI buttons.
-   ✅ **V. Blender-Native Integration**: Compliant. The feature is implemented as a standard Blender addon, using native UI panels and preference systems.
-   ✅ **VI. Continuous Validation Through Testing**: Compliant. Automated tests (`unittest` + `psutil`) verify server lifecycle and functionality.

## Project Structure

### Documentation (this feature)

```text
specs/001-integrated-blender-addon/
├── plan.md              # This file
├── research.md          # Phase 0 output
├── data-model.md        # Phase 1 output
├── quickstart.md        # Phase 1 output
├── contracts/           # Phase 1 output
└── tasks.md             # Phase 2 output (/speckit.tasks command)
```

### Source Code (repository root)

```text
blender_addon/
├── __init__.py          # Main addon registration, handles server lifecycle
├── ui.py                # Defines the UI Panel, buttons, and chat interface
├── operators.py         # Defines Blender operators (e.g., for buttons)
├── server_manager.py    # Logic for starting/stopping the FastAPI server process
├── preferences.py       # Defines the addon preferences for API key
└── tests/               # NEW: Directory for addon tests
    └── test_addon.py    # NEW: Test file for the addon
```

**Structure Decision**: The structure is dictated by the functional requirements (FR-001) in the specification. It separates concerns into distinct modules, making the addon more maintainable and testable. A new `tests` directory will be added to house the testing solution determined during research.

## Technical Decisions & Refinements

### Lazy Initialization of MCP Client
To prevent `KeyError` during Blender startup, the `MCPClient` instance and Preference access (Port configuration) must NOT occur during the `register()` phase.
- **Strategy**: The `MCPClient` is instantiated inside the `WM_OT_MCP_Connect` operator's `execute` method.
- **Rationale**: This ensures `bpy.context.preferences` is fully loaded and accessible. It also allows the Port to be changed in Preferences without needing to reload the addon; the next "Connect" action will pick up the new Port.

### Headless Testing Workarounds and Preference Access
Due to inconsistencies in how Blender's `bpy.context.preferences.addons` behaves in headless scripting mode (`blender -b`):
- **Test Preference Setting**: In `test_addon.py`, addon preferences are set directly on the `preferences.MCPAddonPreferences` class properties (e.g., `prefs_class.api_key = ...`) rather than through `bpy.context.preferences.addons["addon"].preferences`.
  - **Rationale**: Direct access to `bpy.context.preferences.addons["addon"].preferences` proved unreliable, often returning `None` or raising `KeyError` even after `addon_utils.enable()` and retry loops. Setting class properties directly ensures test configuration is applied.
- **Operator Preference Retrieval**: In `operators.py`, preference values (api_key, python_path, port) are now retrieved directly from the `preferences.MCPAddonPreferences` class (e.g., `preferences.MCPAddonPreferences.api_key`).
  - **Rationale**: This aligns the operator's access method with the reliable test setup, preventing `NoneType` errors during operator execution in headless Blender.
- **Addon Key Inconsistency**: Observed that `bpy.context.preferences.addons` uses the key `"addon"` (the directory name) instead of `"blender_addon"` (the package name) for our addon. This was corrected in `operators.py` and debugged in `test_addon.py`.

### Minor Code Enhancements
- **Missing Imports**: Added `import os` to `operators.py` and `import time` to `server_manager.py` to resolve `NameError` exceptions.

## Complexity Tracking

> **Fill ONLY if Constitution Check has violations that must be justified**

| Violation | Why Needed | Simpler Alternative Rejected Because |
|-----------|------------|-------------------------------------|
| N/A       | N/A        | N/A                                 |