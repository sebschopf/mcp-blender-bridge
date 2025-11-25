# Implementation Plan: Dynamic Model Discovery

**Branch**: `012-dynamic-model-discovery` | **Date**: 2025-11-21 | **Spec**: [spec.md](./spec.md)
**Input**: Feature specification from `/specs/012-dynamic-model-discovery/spec.md`

## Summary

This plan details the implementation of dynamic model discovery for the Gemini integration. It involves creating a new API endpoint in the controller to list available models, updating the Blender addon UI to fetch and display these models in a dropdown, and configuring the system to use the selected model. It also adds a fallback mechanism to use the `GEMINI_API_KEY` environment variable if not configured in the addon.

## Technical Context

**Language/Version**: Python 3.11+ (Addon & Controller)
**Primary Dependencies**: 
- Controller: `fastapi`, `google-generativeai`
- Addon: `bpy`, `requests`
**Storage**: Blender Preferences (`bpy.types.AddonPreferences`) for selected model and API key.
**Testing**: `pytest` for Controller, `unittest` (via Blender) for Addon.
**Target Platform**: Blender 3.0+ (Windows/macOS/Linux)
**Project Type**: Client-Server (Blender Addon <-> FastAPI Controller)
**Performance Goals**: Model list fetch < 5s.
**Constraints**: Non-blocking UI in Blender during network requests.
**Scale/Scope**: Single-user, local controller.

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

- ✅ **I. Strict MCP Architecture**: Compliant. The Addon requests the model list from the Controller; the Controller talks to Google API.
- ✅ **II. Conversational Interface**: N/A (Configuration feature).
- ✅ **III. Granular & Secure Tools**: Compliant. The new endpoint `list_models` is a read-only operation.
- ✅ **IV. User-Centric Control**: Compliant. The user explicitly selects the model or enters a custom one.
- ✅ **V. Blender-Native Integration**: Compliant. Uses native `EnumProperty` and `AddonPreferences`.
- ✅ **VI. Continuous Validation Through Testing**: Compliant. Tests will cover the new endpoint and preference logic.

## Project Structure

### Documentation (this feature)

```text
specs/012-dynamic-model-discovery/
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
│   ├── main.py          # Update: Add /api/models endpoint
│   └── gemini_client.py # Update: Add list_available_models method
└── tests/
    └── test_main.py     # Update: Test new endpoint

blender_addon/
├── preferences.py       # Update: Add model EnumProperty and refresh operator
├── server_manager.py    # Update: Pass GEMINI_MODEL env var
├── ui.py                # Update: Display model selector
└── operators.py         # Update: Handle refresh action
```

**Structure Decision**: Extending the existing modular structure. No new top-level directories required.

## Complexity Tracking

> **Fill ONLY if Constitution Check has violations that must be justified**

| Violation | Why Needed | Simpler Alternative Rejected Because |
|-----------|------------|-------------------------------------|
| N/A       | N/A        | N/A                                 |
